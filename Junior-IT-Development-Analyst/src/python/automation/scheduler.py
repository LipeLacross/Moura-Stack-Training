import schedule
import time
import logging
from datetime import datetime
from typing import Callable

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("scheduler")


class TaskScheduler:
    def __init__(self):
        self._tasks: dict[str, dict] = {}

    def daily_at(self, tag: str, time_str: str, func: Callable, *args, **kwargs):
        schedule.every().day.at(time_str).do(self._wrap(tag, func, *args, **kwargs))
        self._tasks[tag] = {"type": "daily", "time": time_str, "func": func.__name__}
        logger.info(f"Tarefa '{tag}' agendada diariamente às {time_str}")

    def hourly(self, tag: str, func: Callable, *args, **kwargs):
        schedule.every().hour.do(self._wrap(tag, func, *args, **kwargs))
        self._tasks[tag] = {"type": "hourly", "func": func.__name__}
        logger.info(f"Tarefa '{tag}' agendada a cada hora")

    def every_minutes(self, tag: str, minutes: int, func: Callable, *args, **kwargs):
        schedule.every(minutes).minutes.do(self._wrap(tag, func, *args, **kwargs))
        self._tasks[tag] = {"type": f"every_{minutes}_min", "func": func.__name__}
        logger.info(f"Tarefa '{tag}' agendada a cada {minutes} minuto(s)")

    def weekly_at(self, tag: str, day: str, time_str: str, func: Callable, *args, **kwargs):
        days_map = {
            "segunda": schedule.every().monday,
            "terca": schedule.every().tuesday,
            "quarta": schedule.every().wednesday,
            "quinta": schedule.every().thursday,
            "sexta": schedule.every().friday,
            "sabado": schedule.every().saturday,
            "domingo": schedule.every().sunday,
        }
        day_lower = day.lower()
        if day_lower in days_map:
            days_map[day_lower].at(time_str).do(self._wrap(tag, func, *args, **kwargs))
            self._tasks[tag] = {"type": f"weekly_{day}", "time": time_str, "func": func.__name__}
            logger.info(f"Tarefa '{tag}' agendada {day} às {time_str}")

    def _wrap(self, tag: str, func: Callable, *args, **kwargs):
        def wrapper():
            logger.info(f"Iniciando tarefa '{tag}' em {datetime.now()}")
            try:
                result = func(*args, **kwargs)
                logger.info(f"Tarefa '{tag}' concluída com sucesso")
                return result
            except Exception as e:
                logger.error(f"Tarefa '{tag}' falhou: {e}")
        return wrapper

    def list_tasks(self) -> dict:
        return self._tasks

    def run(self):
        logger.info("Iniciando scheduler...")
        while True:
            schedule.run_pending()
            time.sleep(30)

    def run_once(self):
        schedule.run_pending()
