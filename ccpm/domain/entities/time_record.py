"""
時間記録エンティティの定義
"""
from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID, uuid4


class TimeRecord:
    """
    時間記録を表すエンティティクラス
    
    タスクの作業時間を記録します。
    """
    
    def __init__(
        self,
        task_id: UUID,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        duration: Optional[float] = None,
        description: str = "",
        id: Optional[UUID] = None,
        created_at: Optional[datetime] = None
    ):
        """
        時間記録の初期化
        
        Args:
            task_id: 関連タスクID
            start_time: 開始時刻
            end_time: 終了時刻
            duration: 作業時間（時間）- start_timeとend_timeから自動計算される場合は不要
            description: 作業内容メモ
            id: 記録ID（指定しない場合は自動生成）
            created_at: 作成日時
        """
        self.id = id if id else uuid4()
        self.task_id = task_id
        self.start_time = start_time if start_time else datetime.now()
        self.end_time = end_time
        self._duration = duration
        self.description = description
        self.created_at = created_at if created_at else datetime.now()
    
    @property
    def duration(self) -> float:
        """
        作業時間を計算（時間単位）
        
        明示的に設定された場合はその値を返し、
        そうでない場合はstart_timeとend_timeから計算します。
        end_timeが設定されていない場合は0を返します。
        
        Returns:
            float: 作業時間（時間）
        """
        if self._duration is not None:
            return self._duration
        
        if self.end_time is None:
            return 0.0
        
        delta = self.end_time - self.start_time
        return delta.total_seconds() / 3600  # 秒を時間に変換
    
    @duration.setter
    def duration(self, hours: float) -> None:
        """
        作業時間を直接設定
        
        Args:
            hours: 作業時間（時間）
        """
        self._duration = hours
    
    def stop(self) -> None:
        """
        時間記録を停止
        
        end_timeを現在時刻に設定し、durationを計算します。
        """
        if self.end_time is None:
            self.end_time = datetime.now()
            self._duration = None  # durationを再計算させる
    
    def is_active(self) -> bool:
        """
        時間記録がアクティブ（記録中）かどうかを確認
        
        Returns:
            bool: 記録中の場合はTrue
        """
        return self.end_time is None
    
    def to_dict(self) -> Dict[str, Any]:
        """
        辞書形式に変換
        
        Returns:
            Dict[str, Any]: 時間記録の辞書表現
        """
        return {
            "id": str(self.id),
            "task_id": str(self.task_id),
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration": self.duration,
            "description": self.description,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TimeRecord":
        """
        辞書から時間記録を作成
        
        Args:
            data: 時間記録データの辞書
            
        Returns:
            TimeRecord: 作成された時間記録インスタンス
        """
        time_record = cls(
            task_id=UUID(data["task_id"]),
            start_time=datetime.fromisoformat(data["start_time"]) if data.get("start_time") else None,
            end_time=datetime.fromisoformat(data["end_time"]) if data.get("end_time") else None,
            duration=float(data["duration"]) if "duration" in data else None,
            description=data.get("description", ""),
            id=UUID(data["id"]) if data.get("id") else None,
            created_at=datetime.fromisoformat(data["created_at"]) if data.get("created_at") else None,
        )
        return time_record