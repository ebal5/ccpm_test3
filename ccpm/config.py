"""
CCPM アプリケーション設定モジュール
"""
import logging
import os
from pathlib import Path
from typing import Any, Dict

# アプリケーションのルートディレクトリ
ROOT_DIR = Path(__file__).parent.parent.absolute()

# データベース設定
DB_DIR = ROOT_DIR / "data"
DB_FILE = DB_DIR / "ccpm.db"
DB_URL = f"sqlite:///{DB_FILE}"

# バックアップディレクトリ
BACKUP_DIR = ROOT_DIR / "backups"

# ロギング設定
LOG_DIR = ROOT_DIR / "logs"
LOG_FILE = LOG_DIR / "ccpm.log"
LOG_LEVEL = logging.INFO
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# アプリケーション設定
APP_NAME = "CCPM Task Manager"
APP_VERSION = "0.1.0"
DEBUG = True

# バッファ設定
DEFAULT_PROJECT_BUFFER_RATIO = 0.5  # クリティカルチェーン長の50%
BUFFER_STATUS_THRESHOLDS = {
    "green": 0.33,  # 0-33%: 緑（安全）
    "yellow": 0.67,  # 34-67%: 黄（注意）
    "red": 1.0,  # 68-100%: 赤（危険）
}

# 必要なディレクトリの作成
def ensure_directories() -> None:
    """アプリケーションに必要なディレクトリを作成します"""
    for directory in [DB_DIR, BACKUP_DIR, LOG_DIR]:
        directory.mkdir(parents=True, exist_ok=True)

# ロギング設定
def setup_logging() -> None:
    """アプリケーションのロギング設定を行います"""
    ensure_directories()
    
    logging.basicConfig(
        level=LOG_LEVEL,
        format=LOG_FORMAT,
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler()
        ]
    )

# 設定の読み込み
def load_config() -> Dict[str, Any]:
    """環境変数から設定を読み込みます"""
    config = {
        "app_name": os.environ.get("CCPM_APP_NAME", APP_NAME),
        "app_version": os.environ.get("CCPM_APP_VERSION", APP_VERSION),
        "debug": os.environ.get("CCPM_DEBUG", DEBUG),
        "db_url": os.environ.get("CCPM_DB_URL", DB_URL),
        "log_level": os.environ.get("CCPM_LOG_LEVEL", LOG_LEVEL),
    }
    return config