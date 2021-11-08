import logging
from logging.handlers import RotatingFileHandler

# file_handler = RotatingFileHandler("logs/system.log", mode="a", maxBytes=10000, backupCount=1)


class MultiFileHandler(RotatingFileHandler):

    def __init__(self, filename, mode, encoding=None, delay=0):

        RotatingFileHandler.__init__(
            self, filename, mode, maxBytes=10000, backupCount=1, encoding=None, delay=0)

    def emit(self, record):

        self.change_file(record.levelname)

        logging.FileHandler.emit(self, record)

    def change_file(self, levelname):

        file_id = None

        if levelname == "WARNING":

            file_id = "logs/warning.log"

        elif levelname == "ERROR":

            file_id = "logs/error.log"

        elif levelname == "DEBUG":

            file_id = "logs/debug.log"

        elif levelname == "INFO":

            file_id = "logs/info.log"

        if file_id is not None:

            self.stream.close()

            self.baseFilename = file_id

            self.stream = self._open()
