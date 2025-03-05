"""
クリティカルチェーン計算サービス
"""
from typing import Dict, List, Set, Tuple
from uuid import UUID

import networkx as nx

from ccpm.domain.entities.project import Project
from ccpm.domain.entities.task import Task

class CriticalChainService:
    """
    クリティカルチェーンの識別と管理を担当するドメインサービス
    """
    
    def identify_critical_chain(self, tasks: List[Task]) -> List[UUID]:
        """
        タスクリストからクリティカルチェーンを識別
        
        タスクの依存関係からグラフを構築し、最長パス（クリティカルパス）を
        クリティカルチェーンとして識別します。
        
        Args:
            tasks: プロジェクト内のタスクリスト
            
        Returns:
            List[UUID]: クリティカルチェーンを構成するタスクIDのリスト
        """
        if not tasks:
            return []
        
        # タスクIDをキー、タスクを値とする辞書を作成
        task_dict = {task.id: task for task in tasks}
        
        # 有向グラフを作成
        G = nx.DiGraph()
        
        # ノードを追加（タスクID、属性として見積り工数を設定）
        for task in tasks:
            G.add_node(task.id, weight=task.estimated_hours)
        
        # エッジを追加（依存関係）
        for task in tasks:
            for dep_id in task.dependencies:
                if dep_id in task_dict:
                    # 依存タスク → タスク の方向にエッジを追加
                    G.add_edge(dep_id, task.id)
        
        # 閉路がある場合はエラー（依存関係の循環）
        if not nx.is_directed_acyclic_graph(G):
            raise ValueError("依存関係に循環があります。クリティカルチェーンを識別できません。")
        
        # 開始タスク（入次数が0のノード）と終了タスク（出次数が0のノード）を特定
        start_tasks = [n for n in G.nodes() if G.in_degree(n) == 0]
        end_tasks = [n for n in G.nodes() if G.out_degree(n) == 0]
        
        # 開始タスクまたは終了タスクがない場合は空のリストを返す
        if not start_tasks or not end_tasks:
            return []
        
        # 最長パス（クリティカルパス）を見つける
        critical_chain = []
        max_length = 0
        
        for start in start_tasks:
            for end in end_tasks:
                try:
                    # 開始タスクから終了タスクへのすべてのパスを見つける
                    for path in nx.all_simple_paths(G, start, end):
                        # パスの長さ（タスクの見積り工数の合計）を計算
                        path_length = sum(G.nodes[task_id]["weight"] for task_id in path)
                        
                        # より長いパスが見つかった場合、クリティカルチェーンを更新
                        if path_length > max_length:
                            max_length = path_length
                            critical_chain = path
                except nx.NetworkXNoPath:
                    # パスが存在しない場合は次の組み合わせを試す
                    continue
        
        return list(critical_chain)
    
    def update_project_critical_chain(self, project: Project, tasks: List[Task]) -> Project:
        """
        プロジェクトのクリティカルチェーンを更新
        
        Args:
            project: 更新するプロジェクト
            tasks: プロジェクト内のタスクリスト
            
        Returns:
            Project: 更新されたプロジェクト
        """
        critical_chain = self.identify_critical_chain(tasks)
        project.critical_chain = critical_chain
        return project
    
    def get_critical_chain_tasks(self, project: Project, tasks: List[Task]) -> List[Task]:
        """
        プロジェクトのクリティカルチェーン上のタスクを取得
        
        Args:
            project: プロジェクト
            tasks: プロジェクト内のタスクリスト
            
        Returns:
            List[Task]: クリティカルチェーン上のタスクリスト
        """
        task_dict = {task.id: task for task in tasks}
        return [task_dict[task_id] for task_id in project.critical_chain if task_id in task_dict]
    
    def calculate_project_completion(self, project: Project, tasks: List[Task]) -> float:
        """
        プロジェクトの完了率を計算
        
        クリティカルチェーン上のタスクの完了状況に基づいて、
        プロジェクト全体の完了率を計算します。
        
        Args:
            project: プロジェクト
            tasks: プロジェクト内のタスクリスト
            
        Returns:
            float: プロジェクトの完了率（0.0〜1.0）
        """
        critical_chain_tasks = self.get_critical_chain_tasks(project, tasks)
        
        if not critical_chain_tasks:
            return 0.0
        
        # クリティカルチェーン上のタスクの合計見積り工数
        total_estimated = sum(task.estimated_hours for task in critical_chain_tasks)
        
        if total_estimated <= 0:
            return 0.0
        
        # 完了したタスクの合計見積り工数
        completed_estimated = sum(
            task.estimated_hours for task in critical_chain_tasks if task.is_completed
        )
        
        # 進行中のタスクの貢献分を計算（実績時間 / 見積り時間の比率、ただし1.0を超えない）
        in_progress_contribution = sum(
            min(task.actual_hours / task.estimated_hours, 1.0) * task.estimated_hours
            for task in critical_chain_tasks
            if task.status == "進行中" and task.estimated_hours > 0
        )
        
        # 完了率を計算
        completion_rate = (completed_estimated + in_progress_contribution) / total_estimated
        
        return min(1.0, max(0.0, completion_rate))