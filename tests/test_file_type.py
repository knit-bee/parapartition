import unittest
import os
from parapartition.file_type import detect_format


class FileTypeDetectionTester(unittest.TestCase):
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
