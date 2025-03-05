# アーキテクチャ設計書

## 1. システム概要
（既存の内容を維持）

## 2. アプリケーション層設計

### 2.1 レイヤー構成
- **ドメイン層**:
  - エンティティ
  - 値オブジェクト
  - ドメインサービス
  - リポジトリインターフェース
- **アプリケーション層**:
  - ユースケース実装
  - サービスオーケストレーション
  - トランザクション管理
- **インフラストラクチャ層**:
  - リポジトリ実装
  - データベースアクセス
  - 外部サービス連携
- **プレゼンテーション層**:
  - Taipy GUIページ定義
  - ビジュアルコンポーネント
  - イベントハンドラ

### 2.2 モジュール構成
```
ccpm/
├── app.py                  # アプリケーションエントリーポイント
├── config.py               # 設定ファイル
├── domain/                 # ドメイン層
│   ├── entities/           # エンティティ
│   │   ├── project.py
│   │   ├── task.py
│   │   ├── time_record.py
│   │   └── regular_task.py
│   ├── value_objects/      # 値オブジェクト
│   │   ├── buffer_status.py
│   │   ├── estimation_accuracy.py
│   │   └── task_dependency.py
│   ├── services/           # ドメインサービス
│   │   ├── buffer_calculation.py
│   │   ├── critical_chain.py
│   │   ├── estimation_correction.py
│   │   └── variance_analysis.py
│   └── repositories/       # リポジトリインターフェース
│       ├── project_repository.py
│       ├── task_repository.py
│       └── time_repository.py
├── application/            # アプリケーション層
│   ├── use_cases/          # ユースケース
│   │   ├── project_management.py
│   │   ├── task_management.py
│   │   ├── time_tracking.py
│   │   ├── regular_task_management.py
│   │   └── analysis.py
│   └── services/           # アプリケーションサービス
│       ├── project_service.py
│       ├── task_service.py
│       ├── buffer_service.py
│       ├── critical_chain_service.py
│       ├── time_service.py
│       ├── regular_task_service.py
│       ├── estimation_service.py
│       └── analysis_service.py
├── infrastructure/         # インフラストラクチャ層
│   ├── repositories/       # リポジトリ実装
│   │   ├── sqlite_project_repository.py
│   │   ├── sqlite_task_repository.py
│   │   └── sqlite_time_repository.py
│   ├── db/                 # データベース関連
│   │   ├── db_manager.py
│   │   ├── migrations/
│   │   └── backup/
│   └── external/           # 外部サービス連携
│       ├── export_service.py
│       └── import_service.py
├── presentation/           # プレゼンテーション層
│   ├── pages/              # Taipy GUIページ定義
│   │   ├── dashboard.py
│   │   ├── projects.py
│   │   ├── tasks.py
│   │   ├── time_tracking.py
│   │   ├── regular_tasks.py
│   │   └── analysis.py
│   ├── components/         # 再利用可能なUIコンポーネント
│   │   ├── buffer_status_indicator.py
│   │   ├── task_dependency_graph.py
│   │   ├── time_tracker.py
│   │   └── estimation_accuracy_chart.py
│   └── event_handlers/     # イベントハンドラ
│       ├── project_handlers.py
│       ├── task_handlers.py
│       └── time_handlers.py
├── analysis/               # 分析専用モジュール
│   ├── estimation_analyzer.py
│   ├── buffer_analyzer.py
│   ├── workload_analyzer.py
│   └── variance_analyzer.py
└── utils/                  # ユーティリティ
    ├── date_utils.py
    ├── estimation_utils.py
    └── visualization_utils.py
```

## 3. ドメイン駆動設計の適用

### 3.1 ドメインモデル
- **集約ルート**:
  - Project: プロジェクト全体を管理する集約
  - Task: タスクとその時間記録を管理する集約
- **エンティティ**:
  - Project, Task, TimeRecord, RegularTask
- **値オブジェクト**:
  - BufferStatus: バッファの状態（緑/黄/赤）と消費率
  - EstimationAccuracy: 見積り精度と傾向
  - TaskDependency: タスク間の依存関係

### 3.2 ドメインサービス
- **BufferCalculation**: バッファサイズ計算とバッファ消費の計算
  - プロジェクトバッファの自動計算（クリティカルチェーン長の50%）
  - バッファ消費率の計算（進捗に対する消費率）
  - バッファステータスの判定（緑/黄/赤）

- **CriticalChain**: クリティカルチェーンの識別と管理
  - 依存関係グラフの構築
  - クリティカルパスの計算
  - フィーディングバッファの計算

- **EstimationCorrection**: 見積り精度分析と補正
  - 過去の見積り傾向分析
  - 見積り補正係数の計算
  - 類似タスクの実績参照

- **VarianceAnalysis**: 予実差異の分析
  - 差異要因のカテゴリ化
  - 共通パターンの識別
  - 改善提案の生成

### 3.3 リポジトリ
- ドメインオブジェクトの永続化と取得を担当
- インターフェースはドメイン層で定義
- 実装はインフラストラクチャ層で提供

## 4. ユースケース実装

### 4.1 プロジェクト管理ユースケース
- プロジェクト作成
- バッファ設定
- 進捗監視
- 完了予測

### 4.2 タスク管理ユースケース
- タスク作成と見積り
- 依存関係設定
- タスク実行と完了
- 予実記録と分析

### 4.3 定常タスク管理ユースケース
- 定常タスク記録
- プロジェクト紐付け
- 定常タスク分析
- テンプレート管理

### 4.4 分析ユースケース
- 見積り精度分析
- バッファ消費分析
- 作業負荷分析
- 予実乖離要因分析

## 5. 技術的詳細

### 5.1 Taipyフレームワーク活用
（既存の内容を維持）

### 5.2 データベース設計
（既存の内容を維持）

### 5.3 非同期処理
（既存の内容を維持）

## 6. セキュリティ設計
（既存の内容を維持）

## 7. 拡張性と保守性

### 7.1 拡張ポイント
- **プラグイン機構**:
  - カスタム分析モジュール
  - 外部サービス連携
- **設定のカスタマイズ**:
  - ユーザー設定ファイル
  - テーマとレイアウトのカスタマイズ
- **ドメインルールの拡張**:
  - 新しいバッファ計算アルゴリズムの追加
  - カスタム予測モデルの統合

### 7.2 コード品質維持
（既存の内容を維持）

## 8. 段階的実装計画

### 8.1 MVP第1弾アーキテクチャ
- **コア機能のみ実装**:
  - 基本的なドメインモデル
  - 主要ユースケース
  - シンプルなGUIページ
- **技術的制約**:
  - 単一ユーザー
  - ローカルデータベースのみ
  - 基本的な可視化

### 8.2 MVP第2弾アーキテクチャ拡張
- **追加機能**:
  - 拡張分析機能
  - 高度なバッファ管理
  - データエクスポート/インポート
- **ドメインモデル拡張**:
  - 詳細な値オブジェクト
  - 高度なドメインサービス

### 8.3 MVP第3弾アーキテクチャ拡張
- **追加機能**:
  - 定常タスク管理の完全実装
  - 高度な予実管理
  - 詳細レポート
- **アーキテクチャ完成**:
  - 完全なDDDアプローチ
  - 高度な分析機能
  - カスタマイズ機能