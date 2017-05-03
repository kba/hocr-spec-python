# -*- coding: utf-8 -*-

from future import standard_library
standard_library.install_aliases()

from builtins import object

import sys
import re
from lxml import etree
from functools import wraps
from .spec import HocrSpec

class HocrValidator(object):

    class LevelAnsiColor(object):
        OK    = '2'
        DEBUG = '4'
        WARN  = '3'
        ERROR = '1'
        FATAL = '1;1'

    class ReportItem(object):
        """
        A single report item
        """
        def __init__(self, level, sourceline, message, **kwargs):
            assert getattr(HocrValidator.LevelAnsiColor, level) != None
            self.level = level
            self.sourceline = sourceline
            self.message = message
        def __str__(self):
            return "[%s] +%s : %s" % (self.level, self.sourceline, self.message)

    class Report(object):

        """
        A validation Report
        """
        def __init__(self, filename):
            self.filename = filename
            self.items = []
            self.abort = False

        def __escape_xml(self, s):
            translation = {
                "'": '&apos;',
                '"': '&quot;',
                '<': '&lt;',
                '>': '&gt;',
                '&': '&amp;',
            }
            for k in translation:
                s = s.replace(k, translation[k])
            return s

        def add(self, level, *args, **kwargs):
            self.items.append(HocrValidator.ReportItem(level, *args, **kwargs))
            if level is 'FATAL':
                raise ValueError("Validation hit a FATAL issue: %s" % self.items[-1])

        def is_valid(self):
            return 0 == len([x for x in self.items if x.level in ['ERROR', 'FATAL']])

        def format(self, *args):
            """
            Format the report
            """
            format = args[0] if args[0] else 'text'
            if format == 'bool':
                return self.is_valid()
            elif format in ['text', 'ansi']:
                if self.is_valid():
                    self.add('OK', 0, "Document is valid")
                out = []
                for item in self.items:
                    filename = self.filename
                    if item.sourceline > 0:
                        filename += ':%d' % (item.sourceline)
                    level = item.level
                    if format == 'ansi':
                        level = "\033[3%sm%s\033[0m" % (
                            getattr(HocrValidator.LevelAnsiColor, item.level),
                            item.level)
                    out.append("[%s] %s %s" % (level, filename, item.message))
                return "\n".join(out)
            elif format == 'xml':
                out = []
                for item in self.items:
                    out.append(
                            '\t<item>\n'
                            '\t\t<level>%s</level>\n'
                            '\t\t<sourceline>%s</sourceline>\n'
                            '\t\t<message>%s</message>\n'
                            '\t</item>' % (item.level, item.sourceline,
                                self.__escape_xml(item.message)))
                return '<report filename="%s" valid="%s">\n%s\n</report>' % (
                        self.filename,
                        ('true' if self.is_valid() else 'false'),
                        "\n".join(out))
            else:
                raise ValueError("Unknown format '%s'")

    formats = ['text', 'bool', 'ansi', 'xml']

    def __init__(self, profile, **kwargs):
        self.spec = HocrSpec(profile, **kwargs)

    def validate(self, source, parse_strict=False, filename=None):
        """
        Validate a hocr document

        Args:
            source (str): A filename or '-' to read from STDIN
            parse_strict (bool): Whether to be strict about broken HTML. Default: False
            filename (str): Filename to use in the reports. Set this if reading
                            from STDIN for nicer output

        """
        parser = etree.HTMLParser(recover=parse_strict)
        if not filename: filename = source
        if source == '-': source = sys.stdin
        doc = etree.parse(source, parser)
        root = doc.getroot()
        report = HocrValidator.Report(filename)
        try:
            self.spec.check(report, root)
        except ValueError as e:
            sys.stderr.write("Validation errored\n")
        return report
