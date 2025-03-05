"""
pytest用の共通フィクスチャ
"""
from datetime import datetime, timedelta

import pytest

from ccpm.domain.entities.project import Project
from ccpm.domain.entities.task import Task
from ccpm.domain.entities.time_record import TimeRecord
from ccpm.domain.value_objects.buffer_status import BufferStatus


@pytest.fixture
def sample_project():
    """サンプルプロジェクトを作成"""
    return Project(
        name="テストプロジェクト",
        description="テスト用のプロジェクト",
        start_date=datetime.now(),
        planned_end_date=datetime.now() + timedelta(days=30),
        status="進行中",
        buffer_size=40.0,
        buffer_consumed=10.0,
    )

@pytest.fixture
def sample_tasks(sample_project):
    """サンプルタスクのリストを作成"""
    task1 = Task(
        name="タスク1",
        project_id=sample_project.id,
        description="最初のタスク",
        status="完了",
        priority=1,
        estimated_hours=20.0,
        actual_hours=18.0,
    )
    
    task2 = Task(
        name="タスク2",
        project_id=sample_project.id,
        description="2番目のタスク",
        status="進行中",
        priority=2,
        estimated_hours=30.0,
        actual_hours=15.0,
        dependencies=[task1.id],
    )
    
    task3 = Task(
        name="タスク3",
        project_id=sample_project.id,
        description="3番目のタスク",
        status="未着手",
        priority=3,
        estimated_hours=40.0,
        actual_hours=0.0,
        dependencies=[task2.id],
    )
    
    return [task1, task2, task3]

@pytest.fixture
def sample_time_record(sample_tasks):
    """サンプル時間記録を作成"""
    return TimeRecord(
        task_id=sample_tasks[1].id,
        start_time=datetime.now() - timedelta(hours=2),
        end_time=datetime.now() - timedelta(hours=1),
        description="タスク2の作業",
    )

@pytest.fixture
def sample_buffer_status():
    """サンプルバッファステータスを作成"""
    return BufferStatus(consumption_rate=0.25)