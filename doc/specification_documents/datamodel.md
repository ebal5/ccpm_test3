# データモデル仕様書

## 1. エンティティ定義

### 1.1 Project（プロジェクト）
- **目的**: プロジェクトの基本情報と進捗状況の管理
- **属性**:
  ```python
  {
    "id": "UUID",                    # プロジェクト一意識別子
    "name": "string",                # プロジェクト名
    "description": "string",         # 説明
    "start_date": "datetime",        # 開始日
    "planned_end_date": "datetime",  # 予定終了日
    "actual_end_date": "datetime",   # 実際の終了日
    "status": "enum",                # ステータス(未着手/進行中/完了)
    "buffer_size": "float",          # プロジェクトバッファサイズ（時間）
    "buffer_consumed": "float",      # 消費済みバッファ量
    "critical_chain": "Task[]",      # クリティカルチェーンを構成するタスクリスト
    "created_at": "datetime",        # 作成日時
    "updated_at": "datetime"         # 更新日時
  }
  ```

### 1.2 Task（タスク）
- **目的**: 個別タスクの管理と進捗追跡
- **属性**:
  ```python
  {
    "id": "UUID",                    # タスク一意識別子
    "project_id": "UUID",            # 所属プロジェクトID
    "name": "string",                # タスク名
    "description": "string",         # 説明
    "status": "enum",                # ステータス(未着手/進行中/完了)
    "priority": "integer",           # 優先度
    "estimated_hours": "float",      # 50%確率見積り工数
    "actual_hours": "float",         # 実績工数
    "dependencies": "UUID[]",        # 依存タスクIDリスト
    "start_date": "datetime",        # 開始日
    "end_date": "datetime",          # 終了日
    "category": "string",            # カテゴリ
    "tags": "string[]",              # タグリスト
    "created_at": "datetime",        # 作成日時
    "updated_at": "datetime"         # 更新日時
  }
  ```

### 1.3 TimeRecord（時間記録）
- **目的**: タスクの作業時間記録
- **属性**:
  ```python
  {
    "id": "UUID",                    # 記録一意識別子
    "task_id": "UUID",              # 関連タスクID
    "start_time": "datetime",        # 開始時刻
    "end_time": "datetime",          # 終了時刻
    "duration": "float",             # 作業時間（時間）
    "description": "string",         # 作業内容メモ
    "created_at": "datetime"         # 作成日時
  }
  ```

### 1.4 RegularTask（定常タスク）
- **目的**: 定例会議やレビューなどの定常的な作業の記録
- **属性**:
  ```python
  {
    "id": "UUID",                    # 定常タスク一意識別子
    "project_id": "UUID",            # 関連プロジェクトID
    "type": "enum",                  # タイプ(会議/レビュー/調査など)
    "title": "string",               # タイトル
    "description": "string",         # 説明
    "duration": "float",             # 所要時間
    "tags": "string[]",              # タグリスト
    "is_buffer_consuming": "boolean", # バッファ消費フラグ
    "created_at": "datetime"         # 作成日時
  }
  ```

### 1.5 EstimationHistory（見積り履歴）
- **目的**: タスクの見積り精度追跡と分析
- **属性**:
  ```python
  {
    "id": "UUID",                    # 履歴一意識別子
    "task_id": "UUID",              # 対象タスクID
    "estimated_hours": "float",      # 見積り工数
    "actual_hours": "float",         # 実績工数
    "variance_reason": "string",     # 差異理由
    "variance_category": "enum",     # 差異カテゴリ
    "created_at": "datetime"         # 作成日時
  }
  ```

## 2. リレーション定義

### 2.1 Project - Task
- 1対多の関係
- プロジェクトは複数のタスクを持つ
- タスクは1つのプロジェクトに属する

### 2.2 Task - TimeRecord
- 1対多の関係
- タスクは複数の時間記録を持つ
- 時間記録は1つのタスクに紐づく

### 2.3 Task - EstimationHistory
- 1対多の関係
- タスクは1つの見積り履歴を持つ
- 見積り履歴は1つのタスクに紐づく

### 2.4 Project - RegularTask
- 1対多の関係
- プロジェクトは複数の定常タスクを持つ
- 定常タスクは1つのプロジェクトに紐づく（オプション）

## 3. データ制約

### 3.1 一意性制約
- Project.id
- Task.id
- TimeRecord.id
- RegularTask.id
- EstimationHistory.id

### 3.2 必須項目
- Project: name, start_date
- Task: name, project_id, estimated_hours
- TimeRecord: task_id, start_time
- RegularTask: type, title, duration
- EstimationHistory: task_id, estimated_hours, actual_hours

### 3.3 データ型制約
- 日時項目: ISO 8601形式
- 工数: 0以上の浮動小数点数
- 優先度: 1-5の整数

## 4. インデックス定義

### 4.1 プライマリキー
- 全テーブルのid列

### 4.2 外部キー
- Task.project_id → Project.id
- TimeRecord.task_id → Task.id
- EstimationHistory.task_id → Task.id
- RegularTask.project_id → Project.id

### 4.3 検索用インデックス
- Project: name, status
- Task: name, status, project_id
- TimeRecord: task_id, start_time
- RegularTask: type, project_id
- EstimationHistory: task_id

## 5. データマイグレーション

### 5.1 バージョン管理
- セマンティックバージョニングの採用
- マイグレーションスクリプトの命名規則: YYYYMMDDHHMMSS_description.sql

### 5.2 ロールバック戦略
- 各マイグレーションに対応するロールバックスクリプトの用意
- データのバックアップポリシーとの連携

### 5.3 データ整合性
- マイグレーション実行前後のデータ検証
- 整合性チェックのための単体テスト実装

## 6. バックアップ戦略

### 6.1 定期バックアップ
- SQLiteデータベースファイルの定期的なバックアップ
- バックアップファイルの命名規則: ccpm_backup_YYYYMMDDHHMMSS.db

### 6.2 リストア手順
- バックアップファイルからのリストア手順の文書化
- リストア後の整合性チェック手順の定義
