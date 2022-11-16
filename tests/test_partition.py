import os
import re
import unittest

from lxml import etree

from parapartition.partition import split_into_paragraphs


class ParapartitionTester(unittest.TestCase):
    def setUp(self):
        self.testdata = os.path.join("tests", "testdata")

    def test_split_raw_text_file_all_lines_returned_individually(self):
        file = os.path.join(self.testdata, "raw", "raw.txt")
        result = list(split_into_paragraphs(file))
        self.assertEqual(len(result), 17)

    def test_paragraph_content_returned(self):
        file = os.path.join(self.testdata, "raw", "raw.txt")
        result = [paragraph[2] for paragraph in split_into_paragraphs(file, "plain")]
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
            "Einfach halten, dem KISS-Prinzip folgen. Einfachheit wird hierbei als"
            "ohne unnötige Ergänzungen oder Veränderungendefiniert.[6] "
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
        file = os.path.join(self.testdata, "html", "html1.html")
        result = [para[1] for para in split_into_paragraphs(file, "html")]
        expected = [
            48,
            51,
            53,
            56,
            59,
            102,
            103,
            105,
            106,
            126,
            127,
            128,
            129,
            131,
            132,
            134,
            136,
            137,
            139,
            140,
            141,
            142,
            144,
            145,
            147,
            151,
            153,
            154,
            155,
            157,
            159,
            161,
            162,
            163,
            165,
            166,
            167,
            169,
            170,
            171,
            173,
            174,
            175,
            178,
            179,
            180,
            183,
            184,
            230,
            231,
            231,
            235,
            284,
        ]
        self.assertEqual(result, expected)

    def test_split_html_text_content_returned_correctly(self):
        file = os.path.join(self.testdata, "html_with_empty_p.html")
        result = [para[2] for para in split_into_paragraphs(file, "html")]
        expected = [
            "text in first cell text in second cell",
            "text in paragraph",
            # third item
            "Es gibt mehrere Distributionen, die entweder von Arch Linux abstammen"
            " oder dessen Paketquellen nutzen. Dazu zählen Antergos mit einem Live-System,"
            " das auf Benutzerfreundlichkeit ausgerichtete Manjaro, Apricity OS für "
            "mobile Cloud-Anwender, das mit einem Tiling Fenstermanager ausgestattete"
            " ArchBang oder Chakra mit Fokus auf KDE[15] aber auch BlackArch[16] "
            "für Penetrationstester, EndeavourOS[17] mit grafischem Installer, "
            "Parabola GNU/Linux-libre[18] ohne unfreie Bestandteile, SystemRescueCd[19]"
            " zur Datenrettung und Artix Linux welches auf systemd verzichtet.[20] "
            "Das italienische Condres OS setzt den Fokus auf Benutzerfreundlichkeit"
            " und bietet offizielle Paketquellen für 32-Bit Architekturen an. ArcoLinux"
            " hingegen versteht sich als Lernsystem, das in den Umgang mit Arch Linux "
            "einführt.[21] SteamOS ab Version 3, welches auf dem Steam Deck eingesetzt "
            "wird, basiert auf Arch Linux.[22] Weblinks",
            # fourth item
            "Arch Linux Website (offiziell, englisch) Arch Linux Wiki (offiziell,"
            " englisch) Arch Linux Website (inoffiziell, deutsch, privat betrieben)",
        ]

        self.assertEqual(expected, result)

    def test_split_tei_header_ignored(self):
        file = os.path.join(self.testdata, "tei_with_p_in_header.xml")
        result = [para[2] for para in split_into_paragraphs(file, "tei")]
        expected = [
            "Arch Linux",
            "Arch Linux [ɑːrtʃ ˈlinʊks] ist eine AMD64-optimierte Linux-Distribution mit Rolling Releases,",
        ]
        self.assertEqual(result, expected)

    def test_split_format_detected_on_xml(self):
        file = os.path.join(self.testdata, "xml", "xml1.xml")
        result = [para[2] for para in split_into_paragraphs(file)]
        result = re.sub(r"\s", "", "".join(result))
        doc = etree.parse(file)
        expected = re.sub(r"\s", "", "".join(doc.getroot().itertext()))
        self.assertEqual(result, expected)

    def test_split_file_format_detected_on_tei(self):
        file = os.path.join(self.testdata, "tei_with_empty_p.xml")
        result = [para[2] for para in split_into_paragraphs(file)]
        expected = [
            "Arch Linux",
            "Arch Linux [ɑːrtʃ ˈlinʊks] ist eine AMD64-optimierte Linux-Distribution mit Rolling Releases,",
            "more text",
        ]
        self.assertEqual(result, expected)

    def test_split_file_format_detected_on_html(self):
        file = os.path.join(self.testdata, "html", "html2")
        result = [para[2].strip() for para in split_into_paragraphs(file)]
        expected = [
            "CentralNotice",
            "Arch Linux",
            "aus Wikipedia, der freien Enzyklopädie",
        ]
        self.assertEqual(result[:3], expected)

    def test_split_file_format_detected_on_plain_text(self):
        file = os.path.join(self.testdata, "raw", "raw.txt")
        result = [paragraph[2] for paragraph in split_into_paragraphs(file)]
        with open(file, encoding="utf-8") as ptr:
            expected = [line.rstrip("\n") for line in ptr]
        self.assertEqual(result, expected)

    def test_split_empty_file_into_paragraphs(self):
        file = os.path.join(self.testdata, "empty.txt")
        result = list(split_into_paragraphs(file))
        self.assertEqual(result, [])

    def test_invalid_format_returns_empty_list(self):
        file = "some_file"
        result = list(split_into_paragraphs(file, "some_format"))
        self.assertEqual(result, [])

    def test_empty_paragraph_skipped_in_xml(self):
        file = os.path.join(self.testdata, "tei_with_empty_p.xml")
        result = [paragraph[2] for paragraph in split_into_paragraphs(file, "tei")]
        self.assertEqual(len(result), 3)

    def test_empty_paragraph_skipped_in_html(self):
        file = os.path.join(self.testdata, "html_with_empty_p.html")
        result = [para[2] for para in split_into_paragraphs(file, "html")]
        self.assertEqual(len(result), 4)

    def test_empty_lines_skipped_in_plain_text(self):
        file = os.path.join(self.testdata, "plain_with_empty_lines.txt")
        result = [para[2] for para in split_into_paragraphs(file, "plain")]
        self.assertEqual(len(result), 4)

    def test_text_concatenated_correctly_from_complex_paragraphs(self):
        file = os.path.join(self.testdata, "tei_with_complex_elements.xml")
        result = [para[2] for para in split_into_paragraphs(file, "tei")]
        self.assertTrue("laſſen ſie" in result[1])

    def test_empty_list_skipped(self):
        file = os.path.join(self.testdata, "tei_with_complex_elements.xml")
        result = [para[2] for para in split_into_paragraphs(file, "tei")]
        self.assertEqual(len(result), 2)

    def test_text_concatenated_correctly_from_list_with_formatting(self):
        file = os.path.join(self.testdata, "tei_with_complex_elements.xml")
        result = [para[2] for para in split_into_paragraphs(file, "tei")]
        expected = (
            "Das 1. Cap. Von den Kranckheiten insgemein 77 2. Cap. Von "
            "ungleichen Mei- nungen der Medicorum in Kranckheiten 79 3. Cap. Von Nutzen"
            " der Kranck- heiten 79 4. Cap. Von Frantzoſen 82 5. Cap. Von der Gonorrhœe 89 "
            "6. Cap. Von der allgemeinen Ungeſundheit oder Cachexia 90 7. Cap. Was von der"
            " Fettigkeit des Menſchen zu halten 92"
        )
        self.assertEqual(result[0], expected)

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
