# -*- coding: utf-8 -*-

import re

MISEQ_FILENAME_PATTERN = """
    (?P<id>\d{4,6})_
    (?P<extraction>\d)_
    (?P<library>PE|MP)_
    (?P<size>\d*bp)_
    SEP_
    (?P<vendor>AGRF|UNSW)_
    (?P<plate>\w{5})_
    (?P<index>[G|A|T|C|-]*)_
    (?P<runsamplenum>\S\d*)_
    (?P<lane>L\d{3})_
    (?P<read>[R|I][1|2])\.fastq\.gz
"""
miseq_filename_pattern = re.compile(MISEQ_FILENAME_PATTERN, re.VERBOSE)

class MD5ParsedLine(object):
    # 26faa5838656dbd82d33dbd277fbe1bc  25705_1_PE_700bp_SEP_UNSW_APAFC_TAGCGCTC-GAGCCTTA_S1_L001_I1.fastq.gz
    # 6d0f632a121671463f8eb496c5ddeac3  25705_1_PE_700bp_SEP_UNSW_APAFC_TAGCGCTC-GAGCCTTA_S1_L001_I2.fastq.gz

    def __init__(self, pattern, line):
        self.pattern = pattern
        self._line = line
        self._ok = False
        self.__parse_line()
        self.md5 = None
        self.filename = None
        self.__parse_line()

    def is_ok(self):
        return self._ok

    def __parse_line(self):
        """ unpack the md5 line """
        self.md5, self.filename = self._line.split()
        matched = self.pattern.match(self.filename)
        if matched:
            self.md5data = matched.groupdict()
            self._ok = True

    def __str__(self):
        return "{} {}".format(self.filename, self.md5)

def parse_md5_file(pattern, md5_file):
    """ Parse md5 file """
    data = []
    with open(md5_file) as f:
        for line in f.read().splitlines():
            line = line.strip()
            if line == "":
                continue

            parsed_line = MD5ParsedLine(pattern, line)
            if parsed_line.is_ok():
                data.append(parsed_line)
    return data
