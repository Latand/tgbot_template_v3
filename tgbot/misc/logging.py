import logging
import os


class LoggingPackagePathFilter(logging.Filter):
    """
    Filter add relative path to the log record.
    The filter create a short path instead of fullpath.

    Logs example:
        /home/user/project/file.py -> /file.py

    Usage example:
        logger = logging.getLogger(__name__)
        package_filter = LoggingPackagePathFilter()
        logger.addFilter(package_filter)

    """
    # taken from
    # https://stackoverflow.com/questions/52582458/how-can-i-include-the-relative-path-to-a-module-in-a-python-logging-statement
    def filter(self, record):
        record.pathname = record.pathname.replace(os.getcwd(), "")
        return True
