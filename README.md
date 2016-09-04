# hocr-spec-python
Validation of hOCR close to the specs

<!-- BEGIN-MARKDOWN-TOC -->
* [Rationale](#rationale)
* [Installation](#installation)
* [Command line interface](#command-line-interface)
* [API example](#api-example)

<!-- END-MARKDOWN-TOC -->

## Rationale

[hOCR](https://github.com/kba/hocr-spec) is a flavor of HTML for encoding
the results of Optical Character Recognition (OCR) engines. It is supported by
most OCR engines, such as
[tesseract](https://github.com/tesseract-ocr/tesseract),
[ocropus/ocropy](https://github.com/tmbdev/ocropy) and
[kraken](https://github.com/mittagessen/kraken).

The [hOCR specifications](https://github.com/kba/hocr-spec) is at the same time
very simple (hOCR is just HTML) and hard to implement, due to its terseness and
lack of up-to-date code samples. This project aims to implement the rules
defined by the specs from the ground up to serve as a validation tool and
reference implementation. It is meant to help hOCR implementers and support
tools like [hocr-tools](https://github.com/tmbdev/hocr-tools).

## Installation

Use pip:

```sh
# System-wide:
sudo pip install [--user] hocr-spec
# For current user:
pip install --user hocr-spec
```

From source:

```sh
git clone https://github.com/kba/hocr-spec-python
cd hocr-spec-python
# System-wide:
sudo python setup.py install
# For current user:
python setup.py install --user
```

## Command line interface

<!-- BEGIN-EVAL echo; ./hocr-spec -h |sed 's/^/    /' -->

    usage: hocr-spec [-h] [--format {text,bool,ansi,xml}]
                     [--profile {relaxed,standard}]
                     [--implicit_capabilities CAPABILITY]
                     [--skip-check {attributes,classes,metadata,properties}]
                     [--parse-strict] [--silent]
                     sources [sources ...]
    
    positional arguments:
      sources               hOCR file to check or '-' to read from STDIN
    
    optional arguments:
      -h, --help            show this help message and exit
      --format {text,bool,ansi,xml}, -f {text,bool,ansi,xml}
                            Report format
      --profile {relaxed,standard}, -p {relaxed,standard}
                            Validation profile
      --implicit_capabilities CAPABILITY, -C CAPABILITY
                            Enable this capability. Use '*' to enable all
                            capabilities. In addition to the 'ocr*' classes, you
                            can use ['ocrp_dir', 'ocrp_font', 'ocrp_lang',
                            'ocrp_nlp', 'ocrp_poly']
      --skip-check {attributes,classes,metadata,properties}, -X {attributes,classes,metadata,properties}
                            Skip one check
      --parse-strict        Parse HTML with less tolerance for errors
      --silent, -s          Don't produce any output but signal success with exit
                            code.

<!-- END-EVAL -->

## API example

```python
from hocr_spec import HocrValidator

validator = HocrValidator()
report = validator.validate('/path/to/sample.hocr')
print(report.format('xml'))
# <report valid='false'>...</report>
```
