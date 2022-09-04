import logging
from typing import Generator, Tuple

import magic

logger = logging.getLogger(__name__)


def split_into_paragraphs(
    file_path: str, format: str = None
) -> Generator[Tuple[str, int, str], None, None]:
    format = format if format is not None else detect_format(file_path)
    if format is None:
        return
    if format == "plain":
        yield from _split_plain_text(file_path)
    elif format == "xml":
        yield from _split_xml(file_path)
    elif format == "html":
        yield from _split_html(file_path)
    elif format == "tei":
        yield from _split_tei(file_path)
    else:
        logger.warning("No valid format, skipping %s " % file_path)
        return


# raw text
# xml /tei : list, table, paragraph , head to paragraph


def detect_format(file_path):
    format = magic.from_file(file_path, mime=True).split("/")
    if format[0] != "text":
        logger.warning(
            "Skipping file %s, it is not a plain text file or empty." % file_path
        )
        return None
    return format[1]


def _split_tei(file_path: str) -> Generator[Tuple[str, int, str], None, None]:
    pass


def _split_html(file_path: str) -> Generator[Tuple[str, int, str], None, None]:
    pass


def _split_xml(file_path: str) -> Generator[Tuple[str, int, str], None, None]:
    pass


def _split_plain_text(file_path: str) -> Generator[Tuple[str, int, str], None, None]:
    with open(file_path, "r", encoding="utf-8") as ptr:
        for i, line in enumerate(ptr, 1):
            yield (file_path, i, line.rstrip("\n"))
