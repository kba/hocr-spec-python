# -*- coding: utf-8 -*-

from future import standard_library
standard_library.install_aliases()

from builtins import str
from builtins import map
from builtins import object

import re

class HocrSpecProperties(object):

    class HocrSpecProperty(object):
        """
        Definition of a 'title' property

        Args:
            name (str): Name of the property
            type (type): str, int, float
            deprecated (Optional[Tuple[int,str]]): Version and message at which
                the property was removed from the specs
            obsolete (Optional[Tuple[int,str]]): Version and message at which
                the property was removed from the specs
            not_checked (bool): Whether the check is not currently tested in-depth
            list (bool): Whether the values are a list
            required_properties (Optional[List[str]]): Names of title
                properties that must be present in the same title
            required_capabilities (Optional[List[str]]): Names of capabilities
                that must be enabled for the document in order to use this
                property.
            split_pattern (List[str]): List of regexes to split list values.
                Specify mutiple regexes for multi-dimensional. Default: ['\s+']
            range (Optional[List[int]]): Minimum and maximum value of property
        """

        def __init__(self, name, type,
                     deprecated=False,
                     obsolete=False,
                     not_checked=False,
                     required_properties=None,
                     range=None,
                     required_capabilities=[],
                     split_pattern=[r"\s+"],
                     list=False):
            self.name = name
            self.type = type
            self.deprecated = deprecated
            self.obsolete = obsolete
            self.not_checked = not_checked
            self.required_properties = required_properties
            self.required_capabilities = required_capabilities
            self.range = range
            self.split_pattern = split_pattern
            self.list = list
        def __repr__(self):
            return '<* title="%s">' % self.name

    # General Properties
    bbox = HocrSpecProperty('bbox', int, list=True)
    textangle = HocrSpecProperty('textangle', float)
    poly = HocrSpecProperty('poly', int, list=True,
            required_capabilities=['ocrp_poly'])
    order = HocrSpecProperty('order', int)
    presence = HocrSpecProperty('presence', str)
    cflow = HocrSpecProperty('cflow', str)
    baseline = HocrSpecProperty('baseline', float, list=True)

    # Recommended Properties for typesetting elements
    image = HocrSpecProperty('image', str)
    imagemd5 = HocrSpecProperty('imagemd5', str)
    ppageno = HocrSpecProperty('ppageno', int)
    lpageno = HocrSpecProperty('lpageno', int)

    # Optional Properties for typesetting elements
    scan_res = HocrSpecProperty('scan_res', int, list=True)
    x_scanner = HocrSpecProperty('x_scanner', str)
    x_source = HocrSpecProperty('x_source', str)
    hardbreak = HocrSpecProperty('hardbreak', int)

    # 7 Character Information
    cuts = HocrSpecProperty(
        'cuts',
        int,
        list=True,
        split_pattern=[r'\s+', ','],
        required_properties=['bbox'])
    nlp = HocrSpecProperty(
        'nlp',
        float,
        list=True,
        required_properties=['bbox', 'cuts'],
        required_capabilities=['ocrp_nlp'])

    #  8 OCR Engine-Specific Markup
    x_font = HocrSpecProperty(
        'xfont_s', str, required_capabilities=['ocrp_font'])
    x_fsize = HocrSpecProperty(
        'xfont_s', int, required_capabilities=['ocrp_font'])
    x_bboxes = HocrSpecProperty('x_bboxes', int, list=True)
    x_confs = HocrSpecProperty('x_confs', float, list=True, range=[0, 100])
    x_wconf = HocrSpecProperty('x_wconf', float, range=[0, 100])

class HocrSpecAttributes(object):

    class HocrSpecAttribute(object):
        """
        HTML Attributes that have special meaning in hOCR.

        Note: 'title', 'class', 'name' and 'content' are handled elsewhere,
        this is for attributes that require special capabilities.
        """
        def __init__(self, name, required_capabilities=[]):
            self.name = name
            self.required_capabilities = required_capabilities

    attr_lang = HocrSpecAttribute('lang', required_capabilities=['ocrp_lang'])
    attr_dir = HocrSpecAttribute('dir', required_capabilities=['ocrp_dir'])

class HocrSpecCapabilities(object):

    class HocrSpecCapability(object):
        """
        Definition of hOCR capabilities.
        """
        def __init__(self, name):
            self.name = name

    ocrp_lang = HocrSpecCapability('ocrp_lang')
    ocrp_dir = HocrSpecCapability('ocrp_dir')
    ocrp_poly = HocrSpecCapability('ocrp_poly')
    ocrp_font = HocrSpecCapability('ocrp_font')
    ocrp_nlp = HocrSpecCapability('ocrp_nlp')

class HocrSpecMetadataFields(object):

    class HocrSpecMetadataField(object):
        """
        Definition of hOCR metadata.
        """
        def __init__(self, name, required=False, recommended=False, known=[]):
            self.name = name
            self.required = required
            self.recommended = recommended
            self.known = known

    ocr_system = HocrSpecMetadataField(
        'ocr-system',
        required=True,
        known=['tesseract 3.03', 'OCRopus Revision: 312'])
    ocr_capabilities = HocrSpecMetadataField('ocr-capabilities', required=True)
    ocr_number_of_pages = HocrSpecMetadataField(
        'ocr-number-of-pages', recommended=True)
    ocr_langs = HocrSpecMetadataField('ocr-langs', recommended=True)
    ocr_scripts = HocrSpecMetadataField('ocr-scripts', recommended=True)


class HocrSpecClasses(object):

    class HocrSpecClass(object):
        """
        Definition of an element defined by its 'class' name

        Args:
            name (str): Name of the class
            deprecated (Optional[Tuple[int,str]]): Version and message at which
                the element was removed from the specs
            obsolete (Optional[Tuple[int,str]]): Version and message at which the element was
                removed from the specs
            not_checked (bool): Whether the validation is not currently tested in-depth
            tagnames (List[str]): Tag names elements with this class
                may have.
            must_exist (bool): Whether at least one elment of this class must
                be present in document
            must_not_contain (List[str]): Classes of elements that must not be
                descendants of this element
            required_attrib (Optional[List[str]]): Names of attributes that
                must be present on the element
            required_properties (Optional[List[str]]): Names of title
                properties that must be present in the title attribute
            required_capabilities (Optional[List[str]]): Names of capabilities
                that must be enabled for the document in order to use this
                class. Will always imply the class itself.
            one_ancestor: (Optional[List[str]]): Classes of elements
                of which there must be exactly one ancestor (think: every line
                must be in exactly one page)
            allowed_descendants: (Optional[List[str]]): Classes of elements
                that are allowed as descendants
        """

        def __init__(self, name,
                     deprecated=False,
                     obsolete=False,
                     not_checked=False,
                     tagnames=[],
                     must_exist=False,
                     must_not_contain=[],
                     required_attrib=[],
                     required_capabilities=[],
                     required_properties=[],
                     one_ancestor=[],
                     allowed_descendants=None):
            self.name = name
            self.deprecated = deprecated
            self.obsolete = obsolete
            self.not_checked = not_checked
            self.tagnames = tagnames
            self.must_exist = must_exist
            self.must_not_contain = must_not_contain
            self.required_attrib = required_attrib
            self.required_properties = required_properties
            self.required_capabilities = [self.name] + required_capabilities
            self.one_ancestor = one_ancestor
            self.allowed_descendants = allowed_descendants
        def __repr__(self):
            return '<* class="%s">' % self.name

    # 4 Logical Structuring Elements
    ocr_document = HocrSpecClass('ocr_document', not_checked=True)
    ocr_title = HocrSpecClass('ocr_title', not_checked=True)
    ocr_author = HocrSpecClass('ocr_author', not_checked=True)
    ocr_abstract = HocrSpecClass('ocr_abstract', not_checked=True)
    ocr_part = HocrSpecClass('ocr_part', tagnames=['h1'])
    ocr_chapter = HocrSpecClass('ocr_chapter', tagnames=['h1'])
    ocr_section = HocrSpecClass('ocr_section', tagnames=['h2'])
    ocr_subsection = HocrSpecClass('ocr_subsection', tagnames=['h3'])
    ocr_subsubsection = HocrSpecClass('ocr_subsubsection', tagnames=['h4'])
    ocr_display = HocrSpecClass('ocr_display', not_checked=True)
    ocr_blockquote = HocrSpecClass('ocr_blockquote', tagnames=['<blockquote>'])
    ocr_par = HocrSpecClass(
        'ocr_par', one_ancestor=['ocr_page'], tagnames=['p'])
    ocr_linear = HocrSpecClass('ocr_linear', not_checked=True)
    ocr_caption = HocrSpecClass('ocr_caption', not_checked=True)

    # 5 Typesetting Related Elements
    ocr_page = HocrSpecClass('ocr_page', must_exist=True)
    ocr_column = HocrSpecClass(
        'ocr_column',
        one_ancestor=['ocr_page'],
        obsolete=('1.1', "Please use ocr_carea instead of ocr_column"))
    ocr_carea = HocrSpecClass(
        'ocr_carea',
        one_ancestor=['ocr_page'])
    ocr_line = HocrSpecClass(
        'ocr_line',
        must_not_contain=['ocr_line'],
        one_ancestor=['ocr_page'],
        required_properties=['bbox'])
    ocr_separator = HocrSpecClass('ocr_separator', not_checked=True)
    ocr_noise = HocrSpecClass('ocr_noise', not_checked=True)

    # Classes for floats
    __FLOATS = [
        'ocr_float'
        'ocr_textfloat',
        'ocr_textimage',
        'ocr_image',
        'ocr_linedrawing',
        'ocr_photo',
        'ocr_header',
        'ocr_footer',
        'ocr_pageno',
        'ocr_table',
    ]
    ocr_float = HocrSpecClass('ocr_float', must_not_contain=__FLOATS)
    ocr_textfloat = HocrSpecClass('ocr_textfloat', must_not_contain=__FLOATS)
    ocr_textimage = HocrSpecClass('ocr_textimage', must_not_contain=__FLOATS)
    ocr_image = HocrSpecClass('ocr_image', must_not_contain=__FLOATS)
    ocr_linedrawing = HocrSpecClass('ocr_linedrawing', must_not_contain=__FLOATS)
    ocr_photo = HocrSpecClass('ocr_photo', must_not_contain=__FLOATS)
    ocr_header = HocrSpecClass('ocr_header', must_not_contain=__FLOATS)
    ocr_footer = HocrSpecClass('ocr_footer', must_not_contain=__FLOATS)
    ocr_pageno = HocrSpecClass('ocr_pageno', must_not_contain=__FLOATS)
    ocr_table = HocrSpecClass('ocr_table', must_not_contain=__FLOATS)

    # 6 Inline Representation
    ocr_glyph = HocrSpecClass('ocr_glyph', not_checked=True)
    ocr_glyphs = HocrSpecClass('ocr_glyphs', not_checked=True)
    ocr_dropcap = HocrSpecClass('ocr_dropcap', not_checked=True)
    ocr_glyphs = HocrSpecClass('ocr_glyphs', not_checked=True)
    ocr_chem = HocrSpecClass('ocr_chem', not_checked=True)
    ocr_math = HocrSpecClass('ocr_math', not_checked=True)
    # 7 Character Information
    ocr_cinfo = HocrSpecClass('ocr_cinfo', not_checked=True)

class HocrSpecProfile(object):
    """
    Restricts how the spec is checked.

    Args:
        version (str): Version to check against
        description (str): Descibe the profile
        implicit_capabilities (List[str]): Assume these capabilities were
            specified in <meta name=ocr-capabilities'>
        skip_check (List[str]): Specify a list of checks to skip.
    """

    def __init__(self, version='1.1', description=None,
            implicit_capabilities=[], skip_check=[]):
        self.version = version
        self.description = description
        self.implicit_capabilities = implicit_capabilities
        self.skip_check = skip_check

class HocrSpec(object):
    """
    The constraints of the HOCR HTML application profile.

    Checks:
        - metadata
        - attributes
        - properties
        - classes
    """
    profiles = {
        'standard': HocrSpecProfile(
            description="Full validation of current spec [Default]"),
        'relaxed': HocrSpecProfile(
            description="Validation without any capability and attribute checks",
            implicit_capabilities=['*'],
            skip_check=['attribute']),
    }
    checks = ['attributes', 'classes', 'metadata', 'properties']

    def __init__(self, profile='standard', **kwargs):
        self.profile = self.__class__.profiles[profile]
        for arg in kwargs:
            if kwargs[arg]:
                setattr(self.profile, arg, kwargs[arg])
        self.checks = []
        for check in self.__class__.checks:
            if not check in self.profile.skip_check:
                self.checks.append(check)

    #=========================================================================
    #
    # Private methods
    #
    #=========================================================================
    def __elem_name(self, el):
        """
        Stringify an element with its attributes
        """
        attrib = " ".join(['%s="%s"'%(k, el.attrib[k]) for k in el.attrib])
        #  attrib = str(el.attrib).replace(': ', ':').replace(', ', ',')
        #  attrib = attrib.replace("{'", '{').replace("':'", ":'").replace("'}", '}')
        return "<%s %s>" %(el.tag, attrib)

    def __get_capabilities(self, root):
        """
        List all capabilities of the document.
        """
        try:
            caps = root.xpath('//meta[@name="ocr-capabilities"]/@content')[0]
            return re.split(r'\s+', caps)
        except IndexError as e: return []

    def __has_capability(self, report, el, cap):
        """
        Check whether the document of `el` has capability `cap`.
        """
        if '*' in self.profile.implicit_capabilities:
            return True
        if not cap in self.__get_capabilities(el) + self.profile.implicit_capabilities:
            report.add('ERROR',
                    el.sourceline,
                    '%s: Requires the "%s" capability but it is not specified'
                    % (self.__elem_name(el), cap))

    def __not_contains_class(self, report, el, contains_classes):
        """
        el must not contain any elements with a class from `contains_classes`
        """
        for contains_class in contains_classes:
            contained = el.xpath(".//*[@class='%s']" % contains_class)
            if len(contained) > 0:
                report.add('ERROR', el.sourceline,
                        "%s must not contain '%s', but does contain %s in line %d" %
                        (self.__elem_name(el),
                            contains_class,
                            self.__elem_name(contained[0]),
                            contained[0].sourceline))

    def __exactly_one_ancestor_class(self, report, el, ancestor_class):
        """
        There must be exactly one element matching xpath.
        """
        nr = len(el.xpath("./ancestor::*[@class='%s']" % ancestor_class))
        if 1 != nr:
            report.add('ERROR', el.sourceline,
                    "%s must be descendant of exactly one '%s', but found %d" %
                    (self.__elem_name(el), ancestor_class, nr))

    def __has_tagname(self, report, el, tagnames):
        """
        Element el must have one of the tag names tagnames
        """
        if tagnames and not el.tag in tagnames:
            report.add('ERROR', el.sourceline,
                       "%s must have a tag name from %s, not '%s'" %
                       (self.__elem_name(el), tagnames, el.tag))

    def __has_attrib(self, report, el, attrib):
        """
        Elements el must have attribute attrib
        """
        if not attrib in el.attrib:
            report.add('ERROR', el.sourceline, "%s must have attribute '%s'"
                    %(self.__elem_name(el), attrib))

    def __has_property(self, report, el, prop):
        """
        Test whether an element el has a property prop in its title field
        """
        try:
            props = self.parse_properties(el)
        except KeyError as e:
            report.add('ERROR', el.sourceline, '%s Cannot parse properties, missing atttribute: %s'
                    %(self.__elem_name(el), e))
            return
        except Exception as e:
            report.add('ERROR', el.sourceline, 'Error parsing properties for "%s" : %s'
                    %(self.__elem_name(el), e))
            return
        if not prop in props:
            report.add('ERROR', el.sourceline, "Element %s must have title prop '%s'"
                    %(self.__elem_name(el), prop))

    def __check_version(self, report, el, spec):
        if spec.deprecated and self.profile.version >= spec.deprecated[0]:
            report.add(
                'WARN', el.sourceline,
                '%s %s has been deprecated since version %s: %s' %
                (self.__elem_name(el), spec, spec.deprecated[0], spec.deprecated[1]))
        if spec.obsolete and self.profile.version >= spec.obsolete[0]:
            report.add('ERROR', el.sourceline,
                       '%s %s has been obsolete since version %s: %s' %
                       (self.__elem_name(el), spec, spec.obsolete[0], spec.obsolete[1]))

    def __check_against_ocr_class(self, report, el, c):
        """
        check an element against its hOCR class.
        """
        if c.not_checked:
            return report.add("WARN", el.sourceline,
                              "Validation of %s not tested in-depth" % c)
        self.__check_version(report, el, c)
        self.__has_tagname(report, el, c.tagnames)
        self.__not_contains_class(report, el, c.must_not_contain)
        for ancestor_class in c.one_ancestor:
            self.__exactly_one_ancestor_class(report, el, ancestor_class)
        for attrib in c.required_attrib:
            self.__has_attrib(report, el, attrib)
        for prop in c.required_properties:
            self.__has_property(report, el, prop)
        for cap in c.required_capabilities:
            self.__has_capability(report, el, cap)

    def __check_against_prop_spec(self, report, el, k, v):
        """
        check a property value against its spec.

        Most structural validation must happen at parse-time to ensure
        syntactical correctness. Here we check value constraints.
        """
        prop_spec = getattr(HocrSpecProperties, k)
        prop_str = str(prop_spec).replace('*', el.tag)
        for cap in prop_spec.required_capabilities:
            self.__has_capability(report, el, cap)
        if prop_spec.deprecated and self.profile.version >= prop_spec.deprecated[0]:
            report.add(
                'WARN', el.sourceline,
                '%s %s has been deprecated since version %s: %s' %
                (self.__elem_name(el), prop_spec, prop_spec.deprecated[0], prop_spec.deprecated[1]))
        if prop_spec.obsolete and self.profile.version >= prop_spec.obsolete[0]:
            report.add('WARN', el.sourceline,
                       '%s %s has been obsolete since version %s: %s' %
                       (self.__elem_name(el), prop_spec, prop_spec.obsolete[0], prop_spec.obsolete[1]))
        # primitives
        if not prop_spec.list:
            if prop_spec.range:
                if not prop_spec.range[0] <= v <= prop_spec.range[1]:
                    report.add(
                        'ERROR',
                        el.sourceline,
                        "%s : Value out of range: %d not in %s"
                        % (prop_str, v, prop_spec.range))
            return
        # lists
        if prop_spec.range:
            for i, vv in enumerate(v):
                if 1 == len(prop_spec.split_pattern):
                    if not prop_spec.range[0] <= vv <= prop_spec.range[1]:
                        report.add(
                            'ERROR',
                            el.sourceline,
                            "%s : List value [%d] out of range (%d not in %s"
                            % (prop_str, i, vv, prop_spec.range))
                if 2 == len(prop_spec.split_pattern):
                    for ii, vv in enumerate(v):
                        if not prop_spec.range[0] <= vv <= prop_spec.range[1]:
                            report.add(
                                'ERROR',
                                el.sourceline,
                                "%s : List value [%d][%d] out of range (%d not in %s"
                                % (prop_str, i, ii, vv, prop_spec.range))

    #=========================================================================
    #
    # Class methods
    #
    #=========================================================================
    @classmethod
    def list(cls, category):
        if category == 'profiles':
            return list(cls.profiles.keys())
        elif category == 'checks':
            return [k[len('check_'):] for k in dir(cls)]
        elif category == 'capabilities':
            return [k for k in dir(HocrSpecCapabilities) if re.match(r'^[a-z].*', k)]
        else:
            raise ValueError("Unknown category %s" % category)

    #=========================================================================
    #
    # Public methods
    #
    #=========================================================================

    def parse_properties(self, title):
        """
        Parse the 'title' attribute of an element.
        """
        ret = {}
        # if it's an lxml node, take the 'title' attribute or die trying
        if hasattr(title, 'attrib'):
            title = title.attrib['title']
        # Split on semicolon, optionally preceded and followed by whitespace
        for kv in re.split(r'\s*;\s*', title):
            # Split key and value at first whitespace
            (k, v) = re.split(r'\s+', kv, 1)
            # Make sure the property is from the list of known properties
            try:
                prop_spec = getattr(HocrSpecProperties, k)
                # If the property is a list value, split the value at the
                # property's 'split_pattern' and apply the type to its values
                if prop_spec.list:
                    if 1 == len(prop_spec.split_pattern):
                        v = list(map(prop_spec.type,
                                     re.split(prop_spec.split_pattern[0], v)))
                    elif 2 == len(prop_spec.split_pattern):
                        #  lambda vv: map(prop_spec.type, re.split(prop_spec.split_pattern[1], vv)),
                        v = [list(map(prop_spec.type, re.split(prop_spec.split_pattern[1], vv))) for vv in re.split(prop_spec.split_pattern[0], v)]
                # If the property is a scalar value, apply the type to the value
                else:
                    v = prop_spec.type(v)
            except Exception as e:
                raise type(e)(str(e) + ' (%s on "%s")' % (type(e).__name__, k))
            ret[k] = v
        return ret

    def check_properties(self, report, root):
        """
        Parse and check all properties.
        """
        #  print __method__
        #  if self.profile.implicit_capabilities
        for el in root.xpath('//*[starts-with(@class, "ocr")][@title]'):
            try:
                props = self.parse_properties(el.attrib['title'])
            except Exception as e:
                return report.add('ERROR', el.sourceline,
                                  'Error parsing properties for "%s" : (property %s)' %
                                  (self.__elem_name(el), e))
            for k in props:
                self.__check_against_prop_spec(report, el, k, props[k])

    def check_classes(self, report, root):
        """
        check all elements by their class
        """
        for class_spec in [getattr(HocrSpecClasses, k)
                           for k in dir(HocrSpecClasses)
                           if k.startswith('ocr')]:
            els = root.xpath('//*[@class="%s"]' % class_spec.name)
            if class_spec.must_exist and len(els) == 0:
                report.add('ERROR', 0,
                           'At least one %s must exist' % class_spec)
            for el in els:
                self.__check_against_ocr_class(report, el, class_spec)

    def check_attributes(self, report, root):
        """
        check attributes according to the spec.
        """
        for attr_spec in [getattr(HocrSpecAttributes, k)
                          for k in dir(HocrSpecAttributes)
                          if k.startswith('attr_')]:
            els = root.xpath('//*[starts-with(@class, "ocr")][@%s]' %
                             attr_spec.name)
            for el in els:
                if '' == el.attrib[attr_spec.name]:
                    report.add(
                        'ERROR', el.sourceline,
                        "%s: Attribute '%s' is empty. "
                        "Either use 'unknown' or don't specify the attribtue"
                        % (self.__elem_name(el), attr_spec.name))
                for cap in attr_spec.required_capabilities:
                    self.__has_capability(report, el, cap)

    def check_metadata(self, report, root):
        """
        check metadata tags.
        """
        # Check for unknown fields
        for el in root.xpath("//meta[starts-with(@name, 'ocr')]"):
            name = el.attrib['name']
            if not getattr(HocrSpecMetadataFields, name.replace('-', '_'), None):
                report.add('ERROR', el.sourceline, "%s Unknown metadata field '%s'"
                           % (self.__elem_name(el), name))
        for field_spec in [getattr(HocrSpecMetadataFields, k)
                     for k in dir(HocrSpecMetadataFields)
                     if k.startswith('ocr')]:
            els = root.xpath("//meta[@name='%s']" % field_spec.name)
            # Cardinality checks
            if len(els) > 1:
                report.add('ERROR', els[1].sourceline,
                           "Metadata fields must not be repeated")
            elif len(els) == 0:
                if field_spec.required:
                    report.add('ERROR', 0, "Required metadata field '%s' missing" %
                               field_spec.name)
                elif field_spec.recommended:
                    report.add('WARN', 0, "Recommended metadata field '%s' missing" %
                               field_spec.name)
                return
            # Field-specific checks
            el = els[0]
            try:
                content = el.attrib['content']
            except KeyError as e:
                report.add('ERROR', el.sourceline, "%s must have 'content' attribute"
                        % self.__elem_name(el))
                return
            if HocrSpecMetadataFields.ocr_system == field_spec:
                if not content in field_spec.known:
                    report.add(
                        'DEBUG', el.sourceline,
                        "Unknown ocr-system: '%s'. "
                        "Consider opening an issue to let others know about it."
                        % content)
            # TODO check other metadata

    def check(self, report, root):
        """
        Execute all enabled checks
        """
        for check in self.checks:
            fn = getattr(HocrSpec, "check_%s"%(check))
            fn(self, report, root)
