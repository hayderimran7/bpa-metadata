# -*- coding: utf-8 -*-
""" Parses md5 file """

import os
import logger_utils

logger = logger_utils.get_logger(__name__)
BPA_PREFIX = "102.100.100."

class MD5ParsedLine(object):
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

def get_base_metagenomics_data(md5_file):
    """
    Parse md5 file
    d33c76935c343df30572a2f719510eec  Sample_7910_1_PE_550bp_BASE_UNSW_H2TFJBCXX/7910_1_PE_550bp_BASE_UNSW_H2TFJBCXX_GAATTCGT-TATAGCCT_L001_R1_001.fastq.gz
    """

    data = []

    with open(md5_file) as f:
        for line in f.read().splitlines():
            line = line.strip()
            if line == '':
                continue

            file_data = {}
            md5, filepath = line.split()
            file_data['md5'] = md5

            filename = os.path.basename(filepath)
            no_extentions_filename = filename.split('.')[0]
            parts = no_extentions_filename.split('_')

            if len(parts) == 11:
                # UniqueID_extraction_library_insert-size_BASE_facility code_FlowID_Index_Lane_F1/R1
                bpa_id, extraction_id, library, insert_size, _, facility, flowcell, index, lane, run_num, run_id = parts

                file_data['target'] = "metagenomics"
                file_data['filename'] = filename
                file_data['bpa_id'] = BPA_PREFIX + bpa_id
                file_data['extraction_id'] = extraction_id
                file_data['facility'] = facility
                file_data['library'] = library
                file_data['insert_size'] = insert_size
                file_data['flowcell'] = insert_size
                file_data['index'] = index
                file_data['lane'] = lane
                file_data['run'] = run_num
                file_data['run_id'] = run_id
            else:
                logger.error('Ignoring line {} from {} with missing data'.format(filename, md5_file))
                continue

            data.append(file_data)

    return data
