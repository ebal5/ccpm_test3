"""
タスクリポジトリのインターフェース定義
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from ccpm.domain.entities.task import Task


class TaskRepository(ABC):
    """
    タスクエンティティの永続化と取得を担当するリポジトリインターフェース
    """
    
    @abstractmethod
    def save(self, task: Task) -> Task:
        """
        タスクを保存
        
        Args:
            task: 保存するタスク
            
        Returns:
            Task: 保存されたタスク
        """
        pass
    
    @abstractmethod
    def find_by_id(self, task_id: UUID) -> Optional[Task]:
        """
        IDによるタスクの検索
        
        Args:
            task_id: 検索するタスクID
            
        Returns:
            Optional[Task]: 見つかったタスク、存在しない場合はNone
        """
        pass
    
    @abstractmethod
    def find_all(self) -> List[Task]:
        """
        すべてのタスクを取得
        
        Returns:
            List[Task]: タスクのリスト
        """
        pass
    
    @abstractmethod
    def find_by_project_id(self, project_id: UUID) -> List[Task]:
        """
        プロジェクトIDによるタスクの検索
        
        Args:
            project_id: 検索するプロジェクトID
            
        Returns:
            List[Task]: 条件に一致するタスクのリスト
        """
        pass
    
    @abstractmethod
    def find_by_status(self, status: str) -> List[Task]:
        """
        ステータスによるタスクの検索
        
        Args:
            status: 検索するステータス
            
        Returns:
            List[Task]: 条件に一致するタスクのリスト
        """
        pass
    
    @abstractmethod
    def find_by_project_and_status(self, project_id: UUID, status: str) -> List[Task]:
        """
        プロジェクトIDとステータスによるタスクの検索
        
        Args:
            project_id: 検索するプロジェクトID
            status: 検索するステータス
            
        Returns:
            List[Task]: 条件に一致するタスクのリスト
        """
        pass
    
    @abstractmethod
    def delete(self, task_id: UUID) -> bool:
        """
        タスクの削除
        
        Args:
            task_id: 削除するタスクID
            
        Returns:
            bool: 削除に成功した場合はTrue
        """
        pass