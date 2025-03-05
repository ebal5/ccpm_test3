"""
CCPM アプリケーションのエントリーポイント
"""
import logging
from taipy.gui import Gui

from ccpm.config import setup_logging, load_config
from ccpm.presentation.pages.dashboard import create_dashboard_page

# ロガーの設定
logger = logging.getLogger(__name__)

def create_app() -> Gui:
    """
    Taipy GUIアプリケーションを作成します
    
    Returns:
        Gui: 設定済みのTaipy GUIインスタンス
    """
    # 設定の読み込み
    config = load_config()
    
    # Taipy GUIの初期化
    gui = Gui(page=create_dashboard_page())
    
    # アプリケーション設定
    gui.title = config["app_name"]
    gui.debug = config["debug"]
    
    logger.info(f"Application {config['app_name']} v{config['app_version']} initialized")
    return gui

def main() -> None:
    """
    アプリケーションのメインエントリーポイント
    """
    # ロギングの設定
    setup_logging()
    
    # アプリケーションの作成
    app = create_app()
    
    # アプリケーションの起動
    logger.info("Starting application...")
    app.run(debug=True, host="0.0.0.0", port=51604, use_reloader=True)
    
if __name__ == "__main__":
    main()