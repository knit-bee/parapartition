import logging

import magic

logger = logging.getLogger(__name__)


def detect_format(file_path):
    format = magic.from_file(file_path, mime=True).split("/")
    if format[0] != "text":
        logger.warning(
            "Skipping file %s, it is not a plain text file or empty." % file_path
        )
        return None
    return format[1]
