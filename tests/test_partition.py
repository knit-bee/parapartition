import os
import re
import unittest

from lxml import etree

from parapartition.partition import detect_format, split_into_paragraphs


class ParapartitionTester(unittest.TestCase):
    def setUp(self):
        self.testdata = os.path.join("tests", "testdata")

    def test_detect_format_on_xml_file(self):
        for file in self.files("xml"):
            result = detect_format(file)
            with self.subTest(file):
                self.assertEqual(result, "html")

    def test_detect_format_on_raw_text_file(self):
        for file in self.files("raw"):
            result = detect_format(file)
            with self.subTest(file):
                self.assertEqual(result, "plain")

    def test_detect_format_on_html_file(self):
        for file in self.files("html"):
            result = detect_format(file)
            with self.subTest():
                self.assertEqual(result, "html")

    def test_detect_format_for_empty_file(self):
        file = os.path.join(self.testdata, "empty.txt")
        result = detect_format(file)
        self.assertIsNone(result)

    def test_split_raw_text_file_all_lines_returned_individually(self):
        file = os.path.join(self.testdata, "raw", "raw.txt")
        result = list(split_into_paragraphs(file))
        self.assertEqual(len(result), 17)

    def test_paragraph_content_returned(self):
        file = os.path.join(self.testdata, "raw", "raw.txt")
        result = [paragraph[2] for paragraph in split_into_paragraphs(file)]
        with open(file, encoding="utf-8") as ptr:
            expected = [line.rstrip("\n") for line in ptr]
        self.assertEqual(result, expected)

    def test_split_raw_text_file_lines_enumerated_correctly(self):
        file = os.path.join(self.testdata, "raw", "raw.txt")
        result = [paragraph[1] for paragraph in split_into_paragraphs(file)]
        self.assertEqual(result, list(range(1, 18)))

    def test_split_file_first_value_always_file_name_raw(self):
        for file in self.files("raw"):
            result = {
                paragraph[0]
                for paragraph in split_into_paragraphs(file, format="plain")
            }
            with self.subTest():
                self.assertEqual(result, {file})

    def test_split_file_first_value_always_file_name_xml(self):
        for file in self.files("xml"):
            result = {paragraph[0] for paragraph in split_into_paragraphs(file, "tei")}
            with self.subTest():
                self.assertEqual(result, {file})

    def test_split_file_first_value_always_file_name_html(self):
        for file in self.files("html"):
            result = {paragraph[0] for paragraph in split_into_paragraphs(file, "html")}
            with self.subTest():
                self.assertEqual(result, {file})

    def test_split_xml_into_paragraphs_source_line_numbers_returned_correctly(self):
        file = os.path.join(self.testdata, "xml", "xml1.xml")
        result = [para[1] for para in split_into_paragraphs(file, "tei")]
        self.assertEqual(
            result,
            [3, 4, 48, 49, 50, 51, 52, 53, 57, 58, 59, 60, 61, 67, 68, 71, 75, 80, 81],
        )

    def test_split_xml_text_content_returned_correctly(self):
        file = os.path.join(self.testdata, "xml", "xml1.xml")
        output = [paragraph[2] for paragraph in split_into_paragraphs(file, "tei")]
        result = output[:3] + output[7:8]
        expected = [
            # first item
            "Arch Linux",
            # second item
            "Arch Linux Arch Linux mit der Desktopumgebung KDE Plasma 5 Entwickler 2002–2007: "
            "Judd Vinet; 2007–2020: Aaron Griffin; seit 2020: Levente Polyak[1] Lizenz(en) "
            "GPL und andere Lizenzen Erstveröff. 12. März 2002 Akt. Version Rolling Release "
            "(monatlicher Schnappschuss zur Installation[2]) Abstammung GNU/Linux ↳ Arch "
            "Architektur(en) AMD64, Arm (inoffiziell), 32-Bit-x86 (i486, pentium4 und i686, inoffiziell) "
            "www.archlinux.org",
            # third item
            "Arch Linux [ɑːrtʃ ˈlinʊks] ist eine AMD64-optimierte Linux-Distribution mit Rolling"
            " Releases, deren Entwicklerteam dem KISS-Prinzip („keep it simple, stupid“) folgt. Zugunsten"
            " der Einfachheit wird auf grafische Installations- und Konfigurationshilfen verzichtet. Aufgrund"
            " dieses Ansatzes ist Arch Linux als Distribution für fortgeschrittene Benutzer zu sehen. "
            "Inspiriert wurden die Ersteller von Crux und BSD.[3]",
            # eigth item
            "Einfach halten, dem KISS-Prinzip folgen. Einfachheit wird hierbei als "
            "ohne unnötige Ergänzungen oder Veränderungen definiert.[6] "
            "Keine GUI-Werkzeuge zur Konfiguration benutzen, die die eigentlichen Vorgänge"
            " vor dem Benutzer verstecken.",
        ]
        self.assertEqual(result, expected)

    def test_split_xml_no_content_missing(self):
        file = os.path.join(self.testdata, "xml", "xml1.xml")
        result = "".join(
            paragraph[2] for paragraph in split_into_paragraphs(file, "tei")
        )
        result = re.sub(r"\s", "", result)
        doc = etree.parse(file)
        expected = re.sub(r"\s", "", "".join(doc.getroot().itertext()))
        self.assertEqual(result, expected)

    def test_split_html_source_line_numbers_returned_correctly(self):
        pass

    def test_split_html_text_content_returned_correctly(self):
        pass

    def test_split_tei_header_ignored(self):
        pass

    def test_split_tei_sources_lines_numbered_correctly(self):
        pass

    def test_split_tei_text_content_returned(self):
        pass

    def test_split_empty_file_into_paragraphs(self):
        file = os.path.join(self.testdata, "empty.txt")
        result = list(split_into_paragraphs(file))
        self.assertEqual(result, [])

    def test_invalid_format_returns_empty_list(self):
        file = "some_file"
        result = list(split_into_paragraphs(file, "some_format"))
        self.assertEqual(result, [])

    def files(self, format):
        testfiles = {
            "xml": [
                "tei2.xml",
                "tei4",
                "tei5.txt",
                "tei6.html",
                "xml1.xml",
                "xml3",
                "xml7.txt",
                "xml8.html",
            ],
            "html": ["html1.html", "html2", "html3.txt", "html4.xml"],
            "raw": ["raw.txt", "raw2", "raw3.xml", "raw4.html"],
        }
        return [os.path.join(self.testdata, format, file) for file in testfiles[format]]
