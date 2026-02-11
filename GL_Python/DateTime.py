# graphics_package/DateTime.py
from datetime import datetime, timezone, timedelta

class DateTime:
    """
    Python port of DateTime.
    Provides simple wrappers around Python's datetime.
    """

    def __init__(self):
        self._dt = datetime.now(timezone.utc)

    def year(self) -> int:
        return self._dt.year

    def month(self) -> int:
        return self._dt.month

    def day(self) -> int:
        return self._dt.day

    def hour(self) -> int:
        return self._dt.hour

    def minute(self) -> int:
        return self._dt.minute

    def second(self) -> int:
        return self._dt.second

    def to_string(self) -> str:
        """
        Return a formatted timestamp string.
        """
        return self._dt.strftime("%Y-%m-%d %H:%M:%S %Z")

    def add_seconds(self, secs: int) -> None:
        """
        Add seconds to this DateTime.
        """
        self._dt += timedelta(seconds=secs)

    def as_datetime(self) -> datetime:
        """
        Return the underlying datetime object.
        """
        return self._dt
