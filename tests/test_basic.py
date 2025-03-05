"""
基本的なテスト
"""

def test_import():
    """基本的なインポートテスト"""
    import ccpm
    assert ccpm is not None

def test_config_import():
    """設定モジュールのインポートテスト"""
    from ccpm import config
    assert config is not None
    assert hasattr(config, 'APP_NAME')
    assert config.APP_NAME == "CCPM Task Manager"