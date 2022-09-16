import logging
from typing import Generator, Tuple

from lxml import etree, html

from parapartition.file_type import detect_format

logger = logging.getLogger(__name__)


def split_into_paragraphs(
    file_path: str, format: str = None
) -> Generator[Tuple[str, int, str], None, None]:
    format = format if format is not None else detect_format(file_path)
    if format is None:
        return
    if format == "plain":
        yield from _split_plain_text(file_path)
    elif format in {"tei", "xml"}:
        yield from _split_tei(file_path)
    elif format == "html":
        yield from _split_html(file_path)
    else:
        logger.warning("No valid format, skipping %s " % file_path)
        return


def _split_html(file_path: str) -> Generator[Tuple[str, int, str], None, None]:
    pass


def _split_tei(file_path: str) -> Generator[Tuple[str, int, str], None, None]:
    p_like_tags = {"p", "fw", "head", "ab"}
    other_tags = {"table", "list"}
    tags_to_iter = {f"{{*}}{tag}" for tag in p_like_tags.union(other_tags)}
    document = etree.parse(file_path)
    text_root = _determine_text_beginnig(document)
    for element in text_root.iter(tags_to_iter):
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


def _determine_text_beginnig(xml_tree: etree._ElementTree) -> etree._Element:
    tei_header = xml_tree.find(".//{*}teiHeader")
    if tei_header is None:
        text_root = xml_tree
    else:
        text_root = tei_header.getnext()
    return text_root


def _gather_complex_element_text(element: etree._Element) -> str:
    return " ".join(part.strip() for part in element.xpath(".//text()") if part.strip())
