import os
import unittest

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
            result = {paragraph[0] for paragraph in split_into_paragraphs(file, "xml")}
            with self.subTest():
                self.assertEqual(result, {file})

    def test_split_file_first_value_always_file_name_html(self):
        for file in self.files("html"):
            result = {paragraph[0] for paragraph in split_into_paragraphs(file, "html")}
            with self.subTest():
                self.assertEqual(result, {file})

    def test_split_xml_into_paragraphs_source_line_numbers_returned_correctly(self):
        pass

    def test_split_xml_text_content_returned_correctly(self):
        pass

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
