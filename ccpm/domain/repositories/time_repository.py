"""
時間記録リポジトリのインターフェース定義
"""
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from ccpm.domain.entities.time_record import TimeRecord


class TimeRepository(ABC):
    """
    時間記録エンティティの永続化と取得を担当するリポジトリインターフェース
    """
    
    @abstractmethod
    def save(self, time_record: TimeRecord) -> TimeRecord:
        """
        時間記録を保存
        
        Args:
            time_record: 保存する時間記録
            
        Returns:
            TimeRecord: 保存された時間記録
        """
        pass
    
    @abstractmethod
    def find_by_id(self, record_id: UUID) -> Optional[TimeRecord]:
        """
        IDによる時間記録の検索
        
        Args:
            record_id: 検索する記録ID
            
        Returns:
            Optional[TimeRecord]: 見つかった時間記録、存在しない場合はNone
        """
        pass
    
    @abstractmethod
    def find_all(self) -> List[TimeRecord]:
        """
        すべての時間記録を取得
        
        Returns:
            List[TimeRecord]: 時間記録のリスト
        """
        pass
    
    @abstractmethod
    def find_by_task_id(self, task_id: UUID) -> List[TimeRecord]:
        """
        タスクIDによる時間記録の検索
        
        Args:
            task_id: 検索するタスクID
            
        Returns:
            List[TimeRecord]: 条件に一致する時間記録のリスト
        """
        pass
    
    @abstractmethod
    def find_active_record(self, task_id: UUID) -> Optional[TimeRecord]:
        """
        タスクIDによるアクティブな（終了していない）時間記録の検索
        
        Args:
            task_id: 検索するタスクID
            
        Returns:
            Optional[TimeRecord]: 見つかったアクティブな時間記録、存在しない場合はNone
        """
        pass
    
    @abstractmethod
    def find_by_date_range(self, start_date: datetime, end_date: datetime) -> List[TimeRecord]:
        """
        日付範囲による時間記録の検索
        
        Args:
            start_date: 検索開始日
            end_date: 検索終了日
            
        Returns:
            List[TimeRecord]: 条件に一致する時間記録のリスト
        """
        pass
    
    @abstractmethod
    def delete(self, record_id: UUID) -> bool:
        """
        時間記録の削除
        
        Args:
            record_id: 削除する記録ID
            
        Returns:
            bool: 削除に成功した場合はTrue
        """
        pass