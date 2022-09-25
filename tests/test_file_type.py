import os
import unittest

from parapartition.file_type import detect_format


class FileTypeDetectionTester(unittest.TestCase):
    def setUp(self):
        self.testdata = os.path.join("tests", "testdata")

    def test_detect_format_on_xml_file(self):
        for file in self.files("xml"):
            result = detect_format(file)
            with self.subTest(file):
                self.assertEqual(result, "xml")

    def test_detect_format_on_tei_file(self):
        for file in self.files("tei"):
            result = detect_format(file)
            with self.subTest(file):
                self.assertEqual(result, "tei")

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

    def files(self, format):
        testfiles = {
            "xml": ["xml1.xml", "xml3", "xml7.txt", "xml8.html"],
            "html": ["html1.html", "html2", "html3.txt", "html4.xml"],
            "raw": ["raw.txt", "raw2", "raw3.xml", "raw4.html"],
            "tei": ["tei2.xml", "tei4", "tei5.txt", "tei6.html"],
        }
        return [
            os.path.join(self.testdata, format, file)
            if format != "tei"
            else os.path.join(self.testdata, "xml", file)
            for file in testfiles[format]
        ]
