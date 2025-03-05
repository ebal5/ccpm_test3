"""
バッファステータスの値オブジェクト
"""
from enum import Enum
from typing import Any, Dict, Tuple


class BufferStatusColor(Enum):
    """バッファステータスの色を表す列挙型"""
    GREEN = "green"   # 安全
    YELLOW = "yellow" # 注意
    RED = "red"       # 危険

class BufferStatus:
    """
    バッファの状態を表す値オブジェクト
    
    バッファの消費率に基づいて、状態（緑/黄/赤）を判定します。
    """
    
    def __init__(
        self,
        consumption_rate: float,
        thresholds: Dict[str, float] = None
    ):
        """
        バッファステータスの初期化
        
        Args:
            consumption_rate: バッファ消費率（0.0〜1.0）
            thresholds: 閾値設定（デフォルト: {"green": 0.33, "yellow": 0.67, "red": 1.0}）
        """
        self.consumption_rate = max(0.0, min(1.0, consumption_rate))
        self.thresholds = thresholds or {
            "green": 0.33,
            "yellow": 0.67,
            "red": 1.0
        }
    
    @property
    def color(self) -> BufferStatusColor:
        """
        バッファステータスの色を判定
        
        Returns:
            BufferStatusColor: バッファステータスの色
        """
        if self.consumption_rate <= self.thresholds["green"]:
            return BufferStatusColor.GREEN
        elif self.consumption_rate <= self.thresholds["yellow"]:
            return BufferStatusColor.YELLOW
        else:
            return BufferStatusColor.RED
    
    @property
    def is_safe(self) -> bool:
        """バッファが安全な状態（緑）かどうか"""
        return self.color == BufferStatusColor.GREEN
    
    @property
    def is_warning(self) -> bool:
        """バッファが注意状態（黄）かどうか"""
        return self.color == BufferStatusColor.YELLOW
    
    @property
    def is_danger(self) -> bool:
        """バッファが危険状態（赤）かどうか"""
        return self.color == BufferStatusColor.RED
    
    def get_color_hex(self) -> str:
        """
        バッファステータスの色をHEX形式で取得
        
        Returns:
            str: 色のHEX値
        """
        color_map = {
            BufferStatusColor.GREEN: "#28a745",  # 緑
            BufferStatusColor.YELLOW: "#ffc107", # 黄
            BufferStatusColor.RED: "#dc3545"     # 赤
        }
        return color_map[self.color]
    
    def get_display_info(self) -> Tuple[str, str, str]:
        """
        表示用の情報を取得
        
        Returns:
            Tuple[str, str, str]: (色名, 色のHEX値, 説明テキスト)
        """
        color_name = self.color.value
        color_hex = self.get_color_hex()
        
        descriptions = {
            BufferStatusColor.GREEN: "安全: バッファ消費は計画内です",
            BufferStatusColor.YELLOW: "注意: バッファ消費が増加しています",
            BufferStatusColor.RED: "危険: バッファ消費が計画を超過しています"
        }
        
        description = descriptions[self.color]
        return (color_name, color_hex, description)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        辞書形式に変換
        
        Returns:
            Dict[str, Any]: バッファステータスの辞書表現
        """
        color_name, color_hex, description = self.get_display_info()
        return {
            "consumption_rate": self.consumption_rate,
            "color": color_name,
            "color_hex": color_hex,
            "description": description,
            "is_safe": self.is_safe,
            "is_warning": self.is_warning,
            "is_danger": self.is_danger,
        }
    
    def __eq__(self, other: object) -> bool:
        """
        等価性の比較
        
        Args:
            other: 比較対象
            
        Returns:
            bool: 等しい場合はTrue
        """
        if not isinstance(other, BufferStatus):
            return False
        return (
            self.consumption_rate == other.consumption_rate and
            self.thresholds == other.thresholds
        )
    
    def __str__(self) -> str:
        """
        文字列表現
        
        Returns:
            str: バッファステータスの文字列表現
        """
        color_name, _, description = self.get_display_info()
        return f"BufferStatus({self.consumption_rate:.2f}, {color_name}, '{description}')"