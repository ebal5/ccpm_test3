# API仕様書

## 1. ドメインAPI

### 1.1 Project API
- **createProject(name, description, start_date, planned_end_date)**
  - 目的: 新しいプロジェクトを作成
  - パラメータ:
    - name: プロジェクト名
    - description: 説明
    - start_date: 開始日
    - planned_end_date: 予定終了日
  - 戻り値: 作成されたプロジェクトID

- **calculateBufferSize(project_id)**
  - 目的: プロジェクトバッファサイズを計算
  - パラメータ:
    - project_id: プロジェクトID
  - 戻り値: 計算されたバッファサイズ（時間）

- **calculateBufferConsumption(project_id)**
  - 目的: バッファ消費率を計算
  - パラメータ:
    - project_id: プロジェクトID
  - 戻り値: バッファ消費率（%）とステータス（緑/黄/赤）

### 1.2 Task API
- **createTask(project_id, name, description, estimated_hours)**
  - 目的: 新しいタスクを作成
  - パラメータ:
    - project_id: 所属プロジェクトID
    - name: タスク名
    - description: 説明
    - estimated_hours: 50%確率見積り工数
  - 戻り値: 作成されたタスクID

- **setTaskDependencies(task_id, dependency_ids)**
  - 目的: タスクの依存関係を設定
  - パラメータ:
    - task_id: タスクID
    - dependency_ids: 依存タスクIDのリスト
  - 戻り値: 成功/失敗

- **startTask(task_id)**
  - 目的: タスクの作業を開始
  - パラメータ:
    - task_id: タスクID
  - 戻り値: 作成された時間記録ID

- **completeTask(task_id, actual_hours, variance_reason)**
  - 目的: タスクを完了し実績を記録
  - パラメータ:
    - task_id: タスクID
    - actual_hours: 実績工数
    - variance_reason: 差異理由（オプション）
  - 戻り値: 成功/失敗

### 1.3 TimeTracking API
- **startTimeRecord(task_id, description)**
  - 目的: 時間記録を開始
  - パラメータ:
    - task_id: タスクID
    - description: 作業内容メモ
  - 戻り値: 作成された時間記録ID

- **stopTimeRecord(record_id)**
  - 目的: 時間記録を停止
  - パラメータ:
    - record_id: 時間記録ID
  - 戻り値: 記録された時間（時間）

- **recordRegularTask(type, title, duration, project_id)**
  - 目的: 定常タスクを記録
  - パラメータ:
    - type: 定常タスクタイプ
    - title: タイトル
    - duration: 所要時間
    - project_id: 関連プロジェクトID（オプション）
  - 戻り値: 作成された定常タスクID

## 2. 分析API

### 2.1 EstimationAnalysis API
- **analyzeEstimationAccuracy(task_id)**
  - 目的: タスクの見積り精度を分析
  - パラメータ:
    - task_id: タスクID
  - 戻り値: 見積り精度情報

- **calculateCorrectionFactor(user_id, category)**
  - 目的: 見積り補正係数を計算
  - パラメータ:
    - user_id: ユーザーID
    - category: タスクカテゴリ（オプション）
  - 戻り値: 補正係数

### 2.2 BufferAnalysis API
- **analyzeBufferTrend(project_id)**
  - 目的: バッファ消費トレンドを分析
  - パラメータ:
    - project_id: プロジェクトID
  - 戻り値: トレンドデータ

- **predictCompletion(project_id)**
  - 目的: プロジェクト完了を予測
  - パラメータ:
    - project_id: プロジェクトID
  - 戻り値: 予測完了日と信頼区間

### 2.3 WorkloadAnalysis API
- **analyzeWorkload(user_id, start_date, end_date)**
  - 目的: 作業負荷を分析
  - パラメータ:
    - user_id: ユーザーID
    - start_date: 開始日
    - end_date: 終了日
  - 戻り値: 作業負荷データ

- **analyzeTaskDistribution(user_id, period)**
  - 目的: タスク種別の分布を分析
  - パラメータ:
    - user_id: ユーザーID
    - period: 期間
  - 戻り値: 分布データ

## 3. データエクスポート/インポートAPI

### 3.1 Export API
- **exportProject(project_id, format)**
  - 目的: プロジェクトデータをエクスポート
  - パラメータ:
    - project_id: プロジェクトID
    - format: 出力形式（JSON/CSV/Excel）
  - 戻り値: エクスポートされたデータ

- **exportAnalysisReport(report_type, parameters, format)**
  - 目的: 分析レポートをエクスポート
  - パラメータ:
    - report_type: レポートタイプ
    - parameters: レポートパラメータ
    - format: 出力形式
  - 戻り値: レポートデータ

### 3.2 Import API
- **importProject(data, merge_strategy)**
  - 目的: プロジェクトデータをインポート
  - パラメータ:
    - data: インポートデータ
    - merge_strategy: マージ戦略
  - 戻り値: インポートされたプロジェクトID

- **importTasks(project_id, data)**
  - 目的: タスクデータをインポート
  - パラメータ:
    - project_id: プロジェクトID
    - data: タスクデータ
  - 戻り値: インポートされたタスク数

## 4. 設定API

### 4.1 UserPreferences API
- **getUserPreferences(user_id)**
  - 目的: ユーザー設定を取得
  - パラメータ:
    - user_id: ユーザーID
  - 戻り値: 設定データ

- **updateUserPreferences(user_id, preferences)**
  - 目的: ユーザー設定を更新
  - パラメータ:
    - user_id: ユーザーID
    - preferences: 設定データ
  - 戻り値: 成功/失敗

### 4.2 SystemSettings API
- **getSystemSettings()**
  - 目的: システム設定を取得
  - パラメータ: なし
  - 戻り値: システム設定データ

- **updateSystemSettings(settings)**
  - 目的: システム設定を更新
  - パラメータ:
    - settings: 設定データ
  - 戻り値: 成功/失敗 