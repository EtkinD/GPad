import sys
from os import sep, mkdir, path
from datetime import datetime


class _Logger:
    """
    File writer class that specified for standard error.
    """

    def __init__(self, folder_path: str):
        if not path.exists(path.abspath(folder_path)):
            mkdir(folder_path)
        self.log_file = open(f'{folder_path}{sep}log_{datetime.now().strftime("%Y-%m-%d_%H.%M.%S")}.log', 'w', encoding="UTF-8")

    def write(self, message):
        self.log_file.write(message)

    def flush(self):
        self.log_file.flush()

    def close(self):
        self.log_file.close()


def redirect_error(folder_path: str = 'Logs'):
    """
    The method that redirects stderr to a file.
    Log files are created depending on current date.
    @param folder_path: directory path to store log files.
    """
    assert len(folder_path) > 0
    sys.stderr = _Logger(folder_path=folder_path)
