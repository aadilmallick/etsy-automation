import logging

class Logger:
  def __init__(self, level=logging.DEBUG):
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

  def debug(self, message : str):
    logging.debug(message)

  def info(self, message : str):
    logging.info(message)

  def warning(self, message : str):
    logging.warning(message)

  def error(self, message : str):
    logging.error(message)

  def critical(self, message : str):
    logging.critical(message)