import logging

class Print:
    _colors = {
        'RED': "\033[31m",
        'GREEN': "\033[32m",
        'YELLOW': "\033[33m",
        'BLUE': "\033[34m",
        'MAGENTA': "\033[35m",
        'CYAN': "\033[36m",
        "BOLD" : "\x1b[1m"
    }
    _RESET = "\033[0m"

    @staticmethod
    def red(*args):
        print(Print._colors['RED'], *args, Print._RESET,)
    
    @staticmethod
    def bold_red(*args):
        print(Print._colors['BOLD'], Print._colors['RED'], *args, Print._RESET)
    
    @staticmethod
    def bold(*args):
        print(Print._colors['BOLD'], *args, Print._RESET)

    @staticmethod
    def green(*args):
        print(Print._colors['GREEN'], *args, Print._RESET,)

    @staticmethod
    def yellow(*args):
        print(Print._colors['YELLOW'], *args, Print._RESET,)

    @staticmethod
    def blue(*args):
        print(Print._colors['BLUE'], *args, Print._RESET,)

    @staticmethod
    def magenta(*args):
        print(Print._colors['MAGENTA'], *args, Print._RESET,)

    @staticmethod
    def cyan(*args):
        print(Print._colors['CYAN'], *args, Print._RESET,)

class Logger:
  def __init__(self, level=logging.DEBUG):
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

  def debug(self, message : str):
    logging.debug(message)
    Print.cyan(message)

  def info(self, message : str):
    logging.info(message)
    Print.blue(message)

  def warning(self, message : str):
    logging.warning(message)
    Print.yellow(message)

  def error(self, message : str):
    logging.error(message)
    Print.red(message)

  def critical(self, message : str):
    logging.critical(message)