import logging
import re
from typing import Generator, Optional, Tuple, Union

from lxml import etree, html

from parapartition.file_format import detect_format

logger = logging.getLogger(__name__)


def split_into_paragraphs(
    file_path: str, format: Optional[str] = None
) -> Generator[Tuple[str, int, str], None, None]:
    """
    Split a xml/html/TEI or plain text file into paragraphs.

    Returns a generator of file name, source line, and text per paragraph.
    Accepted formats are 'plain', 'tei', 'xml', and 'html'.
    For TEI-files, the header will be ignored. For Tei, xml, and
    html files tables and lists are treated as a unit. For html,
    some tags are ignored (e.g. formatting and navigation).
    """

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
    complex_tags = {"table", "ul", "dl", "ol"}
    ignore_tags = {"meta", "script", "nav", "link", "label", "form", "title"}
    document = html.parse(file_path)
    text_root = _determine_text_beginnig_html(document)
    _strip_formatting_tags(text_root)
    for element in text_root.iter():
        if element.tag in ignore_tags:
            continue
        ancestors = {
            parent.tag
            for parent in element.iterancestors(complex_tags.union({"footer", "nav"}))
        }
        if ancestors:
            continue
        if element.tag in complex_tags:
            text = _gather_complex_element_text(element)
            if text.strip():
                yield (file_path, element.sourceline, text)
        else:
            text = element.text if element.text else ""
            if element.tail is not None and element.tail.strip():
                text += f" {element.tail.strip()}"
            if text.strip():
                yield (file_path, element.sourceline, text)


def _split_tei(file_path: str) -> Generator[Tuple[str, int, str], None, None]:
    p_like_tags = {"p", "head", "ab"}
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
            text = etree.tostring(element, method="text", encoding="unicode")
            text = re.sub("\n", " ", text).strip()
            if text:
                yield (file_path, element.sourceline, text)
            else:
                continue
        if el_tag in other_tags:
            text = _gather_complex_element_text(element)
            if text:
                yield (file_path, element.sourceline, text)
            else:
                continue


def _split_plain_text(file_path: str) -> Generator[Tuple[str, int, str], None, None]:
    with open(file_path, "r", encoding="utf-8") as ptr:
        for i, line in enumerate(ptr, 1):
            text = line.rstrip("\n")
            if text:
                yield (file_path, i, text)


def _determine_text_beginnig(
    xml_tree: etree._ElementTree,
) -> Union[etree._Element, etree._ElementTree]:
    tei_header = xml_tree.find(".//{*}teiHeader")
    if tei_header is None:
        text_root = xml_tree
    else:
        text_root = tei_header.getnext()
    return text_root


def _determine_text_beginnig_html(
    html_tree: etree._Element,
) -> Union[etree._Element, etree._ElementTree]:
    head = html_tree.find(".//head")
    if head is not None:
        return head.getnext()
    return html_tree


def _strip_formatting_tags(html_tree: etree._Element) -> None:
    formatting_tags = {
        "b",
        "a",
        "em",
        "strong",
        "mark",
        "span",
        "br",
        "cite",
        "code",
        "i",
        "dfn",
        "q",
        "big",
        "small",
        "time",
        "u",
        "var",
        "style",
        "sub",
        "sup",
        "label",
        "input",
    }
    etree.strip_tags(html_tree, formatting_tags)


def _gather_complex_element_text(element: etree._Element) -> str:
    text = etree.tostring(element, method="text", encoding="unicode")
    text = re.sub(r"\s\s+|\n", " ", text).strip()
    return text
