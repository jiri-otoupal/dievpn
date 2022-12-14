import logging

from PySide6 import QtCore


def config_logger(level=logging.INFO):
    import logging
    from rich.logging import RichHandler

    FORMAT = "%(message)s"
    logging.basicConfig(
        level=level, handlers=[RichHandler()], datefmt="[%X]", format=FORMAT
    )


def qt_message_handler(mode, context, message):
    try:
        if mode == QtCore.QtInfoMsg:
            logging.info(
                "{} at: {} line: {}".format(message, context.file, context.line)
            )
        elif mode == QtCore.QtWarningMsg:
            logging.warning(
                "{} at: {} line: {}".format(message, context.file, context.line)
            )
        elif mode == QtCore.QtCriticalMsg:
            logging.critical(
                "{} at: {} line: {}".format(message, context.file, context.line)
            )
        elif mode == QtCore.QtFatalMsg:
            logging.fatal(
                "{} at: {} line: {}".format(message, context.file, context.line)
            )
        else:
            logging.debug(
                "{} at: {} line: {}".format(message, context.file, context.line)
            )
    except Exception as ex:
        logging.fatal(ex.__str__())
