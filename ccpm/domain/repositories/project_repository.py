"""
プロジェクトリポジトリのインターフェース定義
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from ccpm.domain.entities.project import Project


class ProjectRepository(ABC):
    """
    プロジェクトエンティティの永続化と取得を担当するリポジトリインターフェース
    """
    
    @abstractmethod
    def save(self, project: Project) -> Project:
        """
        プロジェクトを保存
        
        Args:
            project: 保存するプロジェクト
            
        Returns:
            Project: 保存されたプロジェクト
        """
        pass
    
    @abstractmethod
    def find_by_id(self, project_id: UUID) -> Optional[Project]:
        """
        IDによるプロジェクトの検索
        
        Args:
            project_id: 検索するプロジェクトID
            
        Returns:
            Optional[Project]: 見つかったプロジェクト、存在しない場合はNone
        """
        pass
    
    @abstractmethod
    def find_all(self) -> List[Project]:
        """
        すべてのプロジェクトを取得
        
        Returns:
            List[Project]: プロジェクトのリスト
        """
        pass
    
    @abstractmethod
    def find_by_status(self, status: str) -> List[Project]:
        """
        ステータスによるプロジェクトの検索
        
        Args:
            status: 検索するステータス
            
        Returns:
            List[Project]: 条件に一致するプロジェクトのリスト
        """
        pass
    
    @abstractmethod
    def delete(self, project_id: UUID) -> bool:
        """
        プロジェクトの削除
        
        Args:
            project_id: 削除するプロジェクトID
            
        Returns:
            bool: 削除に成功した場合はTrue
        """
        pass