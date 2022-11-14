from lxml import etree


def detect_format(file_path: str) -> str:
    """
    Detect wheter a file is plain text, html, or xml/TEI.
    """
    try:
        doc = etree.parse(file_path)
    except etree.XMLSyntaxError:
        return "plain"
    else:
        root = doc.getroot()
        if root.tag == "html":
            return "html"
        if etree.QName(root.tag).localname == "TEI":
            return "tei"
        return "xml"
