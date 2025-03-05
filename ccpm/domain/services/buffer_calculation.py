"""
バッファ計算サービス
"""
from typing import List, Dict, Any

from ccpm.domain.entities.project import Project
from ccpm.domain.entities.task import Task
from ccpm.domain.value_objects.buffer_status import BufferStatus

class BufferCalculationService:
    """
    プロジェクトバッファの計算と管理を担当するドメインサービス
    """
    
    def __init__(self, buffer_ratio: float = 0.5):
        """
        バッファ計算サービスの初期化
        
        Args:
            buffer_ratio: プロジェクトバッファ比率（デフォルト: 0.5 = クリティカルチェーン長の50%）
        """
        self.buffer_ratio = buffer_ratio
    
    def calculate_project_buffer(self, critical_chain_tasks: List[Task]) -> float:
        """
        プロジェクトバッファのサイズを計算
        
        クリティカルチェーン上のタスクの見積り工数合計の一定割合（デフォルト50%）を
        プロジェクトバッファとして計算します。
        
        Args:
            critical_chain_tasks: クリティカルチェーン上のタスクリスト
            
        Returns:
            float: 計算されたプロジェクトバッファサイズ（時間）
        """
        if not critical_chain_tasks:
            return 0.0
        
        # クリティカルチェーン長（タスクの見積り工数合計）を計算
        critical_chain_length = sum(task.estimated_hours for task in critical_chain_tasks)
        
        # プロジェクトバッファを計算（クリティカルチェーン長 × バッファ比率）
        project_buffer = critical_chain_length * self.buffer_ratio
        
        return project_buffer
    
    def calculate_buffer_consumption_rate(self, project: Project, completed_percentage: float) -> float:
        """
        バッファ消費率を計算
        
        プロジェクトの進捗率に対するバッファ消費率を計算します。
        
        Args:
            project: プロジェクト
            completed_percentage: プロジェクトの完了率（0.0〜1.0）
            
        Returns:
            float: バッファ消費率（0.0〜1.0、1.0を超える場合はバッファ超過）
        """
        if project.buffer_size <= 0:
            return 0.0
        
        # 理想的なバッファ消費率は完了率に比例
        ideal_consumption = completed_percentage
        
        # 実際のバッファ消費率
        actual_consumption = project.buffer_consumed / project.buffer_size
        
        # 相対的なバッファ消費率（理想に対する実際の比率）
        # 完了率が0の場合は、バッファ消費率をそのまま返す
        if completed_percentage <= 0:
            return min(1.0, actual_consumption)
        
        relative_consumption = actual_consumption / ideal_consumption
        
        return min(1.0, relative_consumption)
    
    def get_buffer_status(self, project: Project, completed_percentage: float) -> BufferStatus:
        """
        プロジェクトのバッファステータスを取得
        
        Args:
            project: プロジェクト
            completed_percentage: プロジェクトの完了率（0.0〜1.0）
            
        Returns:
            BufferStatus: バッファステータス
        """
        consumption_rate = self.calculate_buffer_consumption_rate(project, completed_percentage)
        return BufferStatus(consumption_rate)
    
    def calculate_buffer_impact(self, task: Task) -> float:
        """
        タスクの予実差異がバッファに与える影響を計算
        
        タスクの実績工数が見積り工数を超過した場合、その差分がバッファを消費します。
        逆に、実績工数が見積り工数より少なかった場合、その差分がバッファを解放します。
        
        Args:
            task: タスク
            
        Returns:
            float: バッファへの影響（正の値はバッファ消費、負の値はバッファ解放）
        """
        return task.variance