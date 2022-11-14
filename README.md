# parapartition
Split texts (.txt, TEI/.xml, .html) into paragraphs

## Installation
Install from github repository with
```sh
$ pip install git+https://github.com/knit-bee/parapartition.git
```
### Requirements
Python >= 3.7
lxml >= 4.0

## Usage
```py
>>> from parapartition import split_into_paragraphs
>>> list(split_into_paragraphs("my_file"), "plain")
[("my_file", 1, "first line"), ("my_file", 2, "second line")]
```

Raw txt files will be splitted on newline characters. For xml and TEI-files, text that is contained in <p/>, <fw/>, <ab/> or <head/> elements as well as in tables and lists is treated as a paragraph unit. For TEI-files, the header is ignored and the splitting will start at the beginng of the text content. Xml-files are assumed to contain the afore mentioned TEI-like tags.
For html files, the header (an element tagged <head/>) is also ignored if present, and formatting_tags are stripped from the tree and some tags (e.g. <meta/>) are ignored. Text in tables and lists is also treated as a unit, otherwise the text from each tag is returned as a paragraph.
If no format parameter is passed to the *split_into_paragraphs* function, it is tried to detect the format. Possible formats are *plain*, *html*, *xml*, and *tei*.


## License
This project is licensed under the GNU General Public License v3.0.
