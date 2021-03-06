#!/usr/bin/env python

from __future__ import print_function

from future import standard_library
standard_library.install_aliases()

import sys
from hocr_spec import HocrValidator, HocrSpec
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument(
    'sources',
    nargs='+',
    help="hOCR file to check or '-' to read from STDIN")
parser.add_argument(
    '--format',
    '-f',
    choices=HocrValidator.formats,
    default=HocrValidator.formats[0],
    help="Report format")
parser.add_argument(
    '--filename',
    help="Filename to use in report")
parser.add_argument(
    '--profile',
    '-p',
    default='standard',
    choices=HocrSpec.list('profiles'),
    help="Validation profile")
parser.add_argument(
    '--implicit_capabilities',
    '-C',
    action='append',
    metavar='CAPABILITY',
    choices=HocrSpec.list('capabilities'),
    help="Enable this capability. Use '*' to enable all capabilities. "
         "In addition to the 'ocr*' classes, you can use %s" %
         HocrSpec.list('capabilities')
    )
parser.add_argument(
    '--skip-check',
    '-X',
    action='append',
    choices=HocrSpec.checks,
    help="Skip one check")
parser.add_argument(
    '--parse-strict',
    action='store_true',
    help="Parse HTML with less tolerance for errors")
parser.add_argument(
    '--silent',
    '-s',
    action='store_true',
    help="Don't produce any output but signal success with exit code.")

def main():
    args = parser.parse_args()

    validator = HocrValidator(args.profile,
                              skip_check=args.skip_check,
                              implicit_capabilities=args.implicit_capabilities)
    failed = 0
    for source in args.sources:
        report = validator.validate(
            source, parse_strict=args.parse_strict, filename=args.filename)
        failed += not report.is_valid()
        if not args.silent:
            print(report.format(args.format))
    sys.exit(0 if not failed else 1)


if __name__ == "__main__":
    main()
