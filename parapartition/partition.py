import logging
from typing import Generator, Tuple

import magic
from lxml import etree, html

logger = logging.getLogger(__name__)


def split_into_paragraphs(
    file_path: str, format: str = None
) -> Generator[Tuple[str, int, str], None, None]:
    format = format if format is not None else detect_format(file_path)
    if format is None:
        return
    if format == "plain":
        yield from _split_plain_text(file_path)
    elif format == "tei":
        yield from _split_tei(file_path)
    elif format == "html":
        yield from _split_html(file_path)
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


def _split_html(file_path: str) -> Generator[Tuple[str, int, str], None, None]:
    pass


def _split_tei(file_path: str) -> Generator[Tuple[str, int, str], None, None]:
    p_like_tags = {"p", "fw", "head", "ab"}
    other_tags = {"table", "list"}
    tags_to_iter = {f"{{*}}{tag}" for tag in p_like_tags.union(other_tags)}
    document = etree.parse(file_path)
    for element in document.iter(tags_to_iter):
        el_tag = etree.QName(element.tag).localname
        if el_tag in p_like_tags:
            # ignore <p> that are children of list or table
            ancestor_tags = {
                etree.QName(parent.tag).localname for parent in element.iterancestors()
            }
            if ancestor_tags.intersection(other_tags):
                continue
            text = element.text if element.text else ""
            if element.tail is not None and element.tail.strip():
                text += f" {element.tail.strip()}"
            if text:
                yield (file_path, element.sourceline, text)
            else:
                continue
        if el_tag in other_tags:
            text = _gather_complex_element_text(element)
            yield (file_path, element.sourceline, text)


def _split_plain_text(file_path: str) -> Generator[Tuple[str, int, str], None, None]:
    with open(file_path, "r", encoding="utf-8") as ptr:
        for i, line in enumerate(ptr, 1):
            yield (file_path, i, line.rstrip("\n"))


def _gather_complex_element_text(element: etree._Element) -> str:
    return " ".join(part.strip() for part in element.xpath(".//text()") if part.strip())
