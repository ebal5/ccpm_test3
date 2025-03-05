"""
ダッシュボードページの実装
"""
from taipy.gui import Markdown


def create_dashboard_page() -> str:
    """
    ダッシュボードページのMarkdownを作成します
    
    Returns:
        str: ダッシュボードページのMarkdown
    """
    return Markdown(
        """
        # CCPM タスク管理ツール
        
        ## ダッシュボード
        
        *このページは開発中です。MVP第1弾の実装が進行中です。*
        
        ### 今後実装予定の機能:
        
        - プロジェクト管理
        - タスク管理
        - 時間トラッキング
        - バッファ管理
        - クリティカルチェーン表示
        """
    )