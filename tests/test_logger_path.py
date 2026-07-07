from pathlib import Path

import logger


def test_log_file_uses_module_directory():
    log_path = Path(logger.LOG_FILE)
    assert log_path.is_absolute()
    assert log_path.parent == Path(logger.__file__).resolve().parent
