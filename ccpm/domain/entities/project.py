"""
プロジェクトエンティティの定義
"""
from datetime import datetime
from typing import List, Optional, Dict, Any
from uuid import UUID, uuid4

class Project:
    """
    プロジェクトを表すエンティティクラス
    
    プロジェクトはタスクの集合体であり、クリティカルチェーンとバッファを管理します。
    """
    
    def __init__(
        self,
        name: str,
        description: str = "",
        start_date: Optional[datetime] = None,
        planned_end_date: Optional[datetime] = None,
        actual_end_date: Optional[datetime] = None,
        status: str = "未着手",
        buffer_size: float = 0.0,
        buffer_consumed: float = 0.0,
        id: Optional[UUID] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        """
        プロジェクトの初期化
        
        Args:
            name: プロジェクト名
            description: プロジェクトの説明
            start_date: 開始日
            planned_end_date: 予定終了日
            actual_end_date: 実際の終了日
            status: ステータス（未着手/進行中/完了）
            buffer_size: プロジェクトバッファサイズ（時間）
            buffer_consumed: 消費済みバッファ量
            id: プロジェクトID（指定しない場合は自動生成）
            created_at: 作成日時
            updated_at: 更新日時
        """
        self.id = id if id else uuid4()
        self.name = name
        self.description = description
        self.start_date = start_date if start_date else datetime.now()
        self.planned_end_date = planned_end_date
        self.actual_end_date = actual_end_date
        self.status = status
        self.buffer_size = buffer_size
        self.buffer_consumed = buffer_consumed
        self.created_at = created_at if created_at else datetime.now()
        self.updated_at = updated_at if updated_at else datetime.now()
        self._critical_chain: List[UUID] = []
    
    @property
    def critical_chain(self) -> List[UUID]:
        """クリティカルチェーンを構成するタスクIDのリスト"""
        return self._critical_chain
    
    @critical_chain.setter
    def critical_chain(self, task_ids: List[UUID]) -> None:
        """クリティカルチェーンを設定"""
        self._critical_chain = task_ids
    
    @property
    def buffer_consumption_rate(self) -> float:
        """
        バッファ消費率を計算
        
        Returns:
            float: バッファ消費率（0.0〜1.0）
        """
        if self.buffer_size <= 0:
            return 0.0
        return min(1.0, self.buffer_consumed / self.buffer_size)
    
    def start(self) -> None:
        """プロジェクトを開始状態に変更"""
        if self.status == "未着手":
            self.status = "進行中"
            self.start_date = datetime.now()
            self.updated_at = datetime.now()
    
    def complete(self) -> None:
        """プロジェクトを完了状態に変更"""
        if self.status != "完了":
            self.status = "完了"
            self.actual_end_date = datetime.now()
            self.updated_at = datetime.now()
    
    def consume_buffer(self, hours: float) -> None:
        """
        バッファを消費
        
        Args:
            hours: 消費するバッファ時間
        """
        self.buffer_consumed += hours
        self.updated_at = datetime.now()
    
    def release_buffer(self, hours: float) -> None:
        """
        バッファを解放
        
        Args:
            hours: 解放するバッファ時間
        """
        self.buffer_consumed = max(0.0, self.buffer_consumed - hours)
        self.updated_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        辞書形式に変換
        
        Returns:
            Dict[str, Any]: プロジェクトの辞書表現
        """
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "planned_end_date": self.planned_end_date.isoformat() if self.planned_end_date else None,
            "actual_end_date": self.actual_end_date.isoformat() if self.actual_end_date else None,
            "status": self.status,
            "buffer_size": self.buffer_size,
            "buffer_consumed": self.buffer_consumed,
            "buffer_consumption_rate": self.buffer_consumption_rate,
            "critical_chain": [str(task_id) for task_id in self.critical_chain],
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Project":
        """
        辞書からプロジェクトを作成
        
        Args:
            data: プロジェクトデータの辞書
            
        Returns:
            Project: 作成されたプロジェクトインスタンス
        """
        project = cls(
            name=data["name"],
            description=data.get("description", ""),
            start_date=datetime.fromisoformat(data["start_date"]) if data.get("start_date") else None,
            planned_end_date=datetime.fromisoformat(data["planned_end_date"]) if data.get("planned_end_date") else None,
            actual_end_date=datetime.fromisoformat(data["actual_end_date"]) if data.get("actual_end_date") else None,
            status=data.get("status", "未着手"),
            buffer_size=float(data.get("buffer_size", 0.0)),
            buffer_consumed=float(data.get("buffer_consumed", 0.0)),
            id=UUID(data["id"]) if data.get("id") else None,
            created_at=datetime.fromisoformat(data["created_at"]) if data.get("created_at") else None,
            updated_at=datetime.fromisoformat(data["updated_at"]) if data.get("updated_at") else None,
        )
        
        if "critical_chain" in data:
            project.critical_chain = [UUID(task_id) for task_id in data["critical_chain"]]
            
        return project