from logging import Logger, getLogger
from typing import Dict, Optional, cast


class SpeedLogger:
    """
    Logger that writes train speed announcements to different files,
    depending on the value.
    """

    FILE_PATHS: Dict[float, Logger] = {
        140.0: getLogger("fast"),
        40.0: getLogger("normal"),
        0.0: getLogger("slow"),
    }
    LOG_FORMAT: str = "speed of train {train_id}: {speed}"

    @classmethod
    def log_speed_to_file(cls, train_id: str, speed: float) -> None:
        """Write the announced speed to a correct file based on conditions."""

        logger: Optional[Logger] = None
        for speed_threshold, logger_ in cls.FILE_PATHS.items():
            if speed >= speed_threshold:
                logger = logger_

        cast(Logger, logger).info(cls.LOG_FORMAT.format(train_id=train_id, speed=speed))
