"""
タスクエンティティの定義
"""
from datetime import datetime
from typing import List, Optional, Dict, Any, Set
from uuid import UUID, uuid4

class Task:
    """
    タスクを表すエンティティクラス
    
    タスクはプロジェクト内の作業単位であり、見積り工数と実績工数を管理します。
    """
    
    def __init__(
        self,
        name: str,
        project_id: UUID,
        description: str = "",
        status: str = "未着手",
        priority: int = 3,
        estimated_hours: float = 0.0,
        actual_hours: float = 0.0,
        dependencies: Optional[List[UUID]] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        category: str = "",
        tags: Optional[List[str]] = None,
        id: Optional[UUID] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        """
        タスクの初期化
        
        Args:
            name: タスク名
            project_id: 所属プロジェクトID
            description: タスクの説明
            status: ステータス（未着手/進行中/完了）
            priority: 優先度（1-5）
            estimated_hours: 50%確率見積り工数
            actual_hours: 実績工数
            dependencies: 依存タスクIDリスト
            start_date: 開始日
            end_date: 終了日
            category: カテゴリ
            tags: タグリスト
            id: タスクID（指定しない場合は自動生成）
            created_at: 作成日時
            updated_at: 更新日時
        """
        self.id = id if id else uuid4()
        self.name = name
        self.project_id = project_id
        self.description = description
        self.status = status
        self.priority = priority
        self.estimated_hours = estimated_hours
        self.actual_hours = actual_hours
        self.dependencies = dependencies if dependencies else []
        self.start_date = start_date
        self.end_date = end_date
        self.category = category
        self.tags = tags if tags else []
        self.created_at = created_at if created_at else datetime.now()
        self.updated_at = updated_at if updated_at else datetime.now()
    
    @property
    def is_started(self) -> bool:
        """タスクが開始されているかどうか"""
        return self.status == "進行中" or self.status == "完了"
    
    @property
    def is_completed(self) -> bool:
        """タスクが完了しているかどうか"""
        return self.status == "完了"
    
    @property
    def variance(self) -> float:
        """
        予実差異を計算
        
        Returns:
            float: 実績工数 - 見積り工数
        """
        return self.actual_hours - self.estimated_hours
    
    @property
    def variance_ratio(self) -> float:
        """
        予実比率を計算
        
        Returns:
            float: 実績工数 / 見積り工数（見積りが0の場合は1.0）
        """
        if self.estimated_hours <= 0:
            return 1.0
        return self.actual_hours / self.estimated_hours
    
    def start(self) -> None:
        """タスクを開始状態に変更"""
        if self.status == "未着手":
            self.status = "進行中"
            self.start_date = datetime.now()
            self.updated_at = datetime.now()
    
    def complete(self) -> None:
        """タスクを完了状態に変更"""
        if self.status != "完了":
            self.status = "完了"
            self.end_date = datetime.now()
            self.updated_at = datetime.now()
    
    def add_dependency(self, task_id: UUID) -> None:
        """
        依存タスクを追加
        
        Args:
            task_id: 依存タスクのID
        """
        if task_id not in self.dependencies:
            self.dependencies.append(task_id)
            self.updated_at = datetime.now()
    
    def remove_dependency(self, task_id: UUID) -> None:
        """
        依存タスクを削除
        
        Args:
            task_id: 削除する依存タスクのID
        """
        if task_id in self.dependencies:
            self.dependencies.remove(task_id)
            self.updated_at = datetime.now()
    
    def add_tag(self, tag: str) -> None:
        """
        タグを追加
        
        Args:
            tag: 追加するタグ
        """
        if tag not in self.tags:
            self.tags.append(tag)
            self.updated_at = datetime.now()
    
    def remove_tag(self, tag: str) -> None:
        """
        タグを削除
        
        Args:
            tag: 削除するタグ
        """
        if tag in self.tags:
            self.tags.remove(tag)
            self.updated_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        辞書形式に変換
        
        Returns:
            Dict[str, Any]: タスクの辞書表現
        """
        return {
            "id": str(self.id),
            "project_id": str(self.project_id),
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "priority": self.priority,
            "estimated_hours": self.estimated_hours,
            "actual_hours": self.actual_hours,
            "dependencies": [str(dep) for dep in self.dependencies],
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "category": self.category,
            "tags": self.tags,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "variance": self.variance,
            "variance_ratio": self.variance_ratio,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Task":
        """
        辞書からタスクを作成
        
        Args:
            data: タスクデータの辞書
            
        Returns:
            Task: 作成されたタスクインスタンス
        """
        task = cls(
            name=data["name"],
            project_id=UUID(data["project_id"]),
            description=data.get("description", ""),
            status=data.get("status", "未着手"),
            priority=int(data.get("priority", 3)),
            estimated_hours=float(data.get("estimated_hours", 0.0)),
            actual_hours=float(data.get("actual_hours", 0.0)),
            dependencies=[UUID(dep) for dep in data.get("dependencies", [])],
            start_date=datetime.fromisoformat(data["start_date"]) if data.get("start_date") else None,
            end_date=datetime.fromisoformat(data["end_date"]) if data.get("end_date") else None,
            category=data.get("category", ""),
            tags=data.get("tags", []),
            id=UUID(data["id"]) if data.get("id") else None,
            created_at=datetime.fromisoformat(data["created_at"]) if data.get("created_at") else None,
            updated_at=datetime.fromisoformat(data["updated_at"]) if data.get("updated_at") else None,
        )
        return task