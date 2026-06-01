from pathlib import Path
import pytest
import tempfile
import shutil


@pytest.fixture
def temp_dir():
    path = Path(tempfile.mkdtemp())
    yield path
    shutil.rmtree(path)


class TestFileProcessor:
    def test_read_csv(self, temp_dir):
        from src.python.automation.file_processor import FileProcessor
        csv_path = temp_dir / "test.csv"
        csv_path.write_text("a,b,c\n1,2,3\n4,5,6\n", encoding="utf-8")

        fp = FileProcessor(temp_dir, temp_dir / "out")
        df = fp.read_file(csv_path)
        assert len(df) == 2
        assert list(df.columns) == ["a", "b", "c"]

    def test_export_csv(self, temp_dir):
        import pandas as pd
        from src.python.automation.file_processor import FileProcessor

        fp = FileProcessor(temp_dir, temp_dir / "out")
        df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})
        path = fp.export(df, "test_output", "csv")
        assert path.exists()
        assert "test_output.csv" in path.name

    def test_consolidate_files(self, temp_dir):
        from src.python.automation.file_processor import FileProcessor

        for i in range(3):
            (temp_dir / f"batch_{i}.csv").write_text(
                f"id,val\n{i*10+1},{i*100}\n{i*10+2},{i*100+50}\n", encoding="utf-8"
            )

        fp = FileProcessor(temp_dir, temp_dir / "out")
        df = fp.consolidate_files("batch_*.csv")
        assert len(df) == 6


class TestTaskScheduler:
    def test_schedule_daily(self):
        from src.python.automation.scheduler import TaskScheduler

        sched = TaskScheduler()
        calls = []

        def dummy():
            calls.append("ran")

        sched.daily_at("test", "14:00", dummy)
        tasks = sched.list_tasks()
        assert "test" in tasks
        assert tasks["test"]["type"] == "daily"

    def test_schedule_hourly(self):
        from src.python.automation.scheduler import TaskScheduler

        sched = TaskScheduler()
        sched.hourly("hourly_test", lambda: None)
        tasks = sched.list_tasks()
        assert "hourly_test" in tasks
