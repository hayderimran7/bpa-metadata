#!/usr/bin/env python
# coding: utf-8

"""
bpalink.py builds download link trees with file names provided.

Usage: 
  bpalink.py [options] (melanoma | gbr | wheat7a | wheat_cultivars | wheat_pathogens | base ) SUBARCHIVE_ROOT

Options:
  -v, --verbose                       Verbose mode.
  -s, --swiftbase=SWIFTURI            Base URI for files in swift [default: http://swift.bioplatforms.com/v1/AUTH_b154c0aff02345fba80bd118a54177ea]
  -a, --apacheredirects=APACHEREDIRS  Output file for Apache redirects
  -l, --linktree=LINKTREE_ROOT        Base path for link tree
  -o, --htmlbase=HTMLBASE             Output path for HTML
  -b, --linkbase=PUBLICURI            Base URI for files on public interface,  [default: http://downloads.bioplatforms.com/]
"""

from docopt import docopt
from unipath import Path
from tendo import colorer
import StringIO, pprint, sys, csv, re, unipath, xlrd, urlparse, urllib, os, json, datetime
from collections import namedtuple
from jinja2 import FileSystemLoader
from jinja2.environment import Environment
import logging

logging.basicConfig(level=logging.DEBUG)

__version__ = "1.1.0"

# this ID never changes... it captures the place where it was minted.
BPA_PREFIX = '102.100.101'


def _stringify(s):
    if isinstance(s, str):
        return str(s.decode('utf8'))
    elif isinstance(s, unicode):
        return str(s.encode('utf8'))
    else:
        return str(s)


def stringify(s):
    _s = _stringify(s)
    return _s


def excel_date_to_string(date_mode, s):
    try:
        date_val = float(s)
        tpl = xlrd.xldate_as_tuple(date_val, date_mode)
        return datetime.datetime(*tpl).strftime("%d/%m/%Y")
    except ValueError:
        return s


class ExcelWrapper(object):
    def __init__(self, fname):
        self.x = xlrd.open_workbook(fname)

    def get_date_mode(self):
        return self.x.datemode

    def sheet_iter(self, sheet_name):
        sheet = [t for t in self.x.sheets() if t.name.lower() == sheet_name.lower()][0]
        for row_idx in xrange(sheet.nrows):
            vals = [stringify(t) for t in sheet.row_values(row_idx)]
            yield vals


def parse_to_named_tuple(typname, reader, header, fieldspec):
    """
    parse a CSV file and yield a list of namedtuple instances.
    fieldspec specifies the CSV fields to be read in, and the name 
    of the attribute to map them to on the new type
    reader should be past the header - clear to read normal rows.
    the header in which to look up fields must be passed in.

    always adds a 'row' member to the named tuple, which is the row 
    number of the entry in the source file (minus header)
    """
    typ = namedtuple(typname, ['row'] + [t[0] for t in fieldspec])
    lookup = []
    fns = [t[2] for t in fieldspec]
    for _, field_name, _ in fieldspec:
        idx = header.index(field_name)
        assert (idx != -1)
        lookup.append(idx)
    for idx, row in enumerate(reader):
        tpl = [idx]
        for fn, i in zip(fns, lookup):
            val = row[i].decode('utf-8').strip()
            if fn is not None:
                val = fn(val)
            tpl.append(val)
        yield typ(*tpl)


class MD5Load(object):
    @classmethod
    def load(cls, folder, checksums=None):
        """
        Load md5 data in the folder specified. if a conflict is found a message is logged
        and the entry in the dictionary is set to None. If `checksums' is passed in, it is updated 
        (in place) and returned.
        """

        if checksums is None:
            checksums = {}

        # we can't trust filenames to determine if a checksum file is MD5 or EXF format, 
        # so instead we use a single parser that copes with either format on a line by line 
        # basis
        plain = folder.listdir(pattern="*.exf", filter=unipath.FILES)
        plain += folder.listdir(pattern="checksums.*", filter=unipath.FILES)
        plain += folder.listdir(pattern="*md5*", filter=unipath.FILES)

        for path in plain:
            if not path.endswith('.xls'):
                cls.parse_checksum_file(path, checksums)
        xls = folder.listdir(pattern="*md5*.xls", filter=unipath.FILES)
        for path in xls:
            cls.parse_xls_checksum_file(path, checksums)
        return checksums

    @classmethod
    def update_checksums_from_iter(cls, it, checksums):
        """
        updates @checksums from (md5, filename) tuples yielded by @it
        """
        for md5sum, filename in it:
            # some md5 files have relative or absolute paths -- we just want filename
            filename = filename.rsplit('/', 1)[-1]
            if filename in checksums and checksums[filename] != md5sum:
                logging.warning("conflict: `%s' %s vs %s." % (filename, md5sum, checksums[filename]))
                checksums[filename] = None
            else:
                checksums[filename] = md5sum

    exf_line_re = re.compile(r'^([a-z0-9]{32}) \*(.*)$')
    md5_line_re = re.compile(r'^([a-z0-9]{32})  (.*)$')

    @classmethod
    def parse_checksum_file(cls, path, checksums):
        """copes with exf and plain md5 file formats"""

        def checksums_iter():
            for line in path.read_file().splitlines():
                m = cls.exf_line_re.match(line)
                if m:
                    yield m.groups()
                    continue
                m = cls.md5_line_re.match(line)
                if m:
                    yield m.groups()
                    continue
                    # logging.info("skipped: " + path + " " + repr(line.rstrip()))

        cls.update_checksums_from_iter(checksums_iter(), checksums)
        return checksums

    @classmethod
    def parse_xls_checksum_file(cls, path, checksums):
        def xls_iter():
            x = xlrd.open_workbook(path.absolute())
            for sheet in x.sheets():
                for row_idx in xrange(sheet.nrows):
                    vals = [t.strip() for t in sheet.row_values(row_idx)]
                    if len(vals) == 2 and len(vals[1]) == 32:
                        filename, md5 = vals
                        yield md5, filename

        cls.update_checksums_from_iter(xls_iter(), checksums)
        return checksums


class AmbiguousChecksum(Exception):
    pass


class NoChecksum(Exception):
    pass


class Unknown(Exception):
    pass


class FastqInventory(object):
    fastq = namedtuple('Fastq', ['filename', 'md5'])

    def __init__(self, base):
        self.base = base
        self.inventory = []
        self.no_checksum = set()
        self.ambiguous_checksum = set()
        # walk through subdirectories and find all the fastq files; then try to find 
        # checksums for them
        for sub in base.walk(filter=unipath.DIRS):
            fastq = sub.listdir(pattern="*fastq.gz", filter=unipath.FILES)
            fastq += sub.listdir(pattern="*txt.bz2", filter=unipath.FILES)
            if len(fastq) == 0:
                continue
                # build a dictionary of MD5sums from this subdirectory up to our parent
            md5s = {}
            md5_sub = sub
            while True:
                md5s = MD5Load.load(md5_sub, md5s)
                md5_sub = md5_sub.parent
                if md5_sub == self.base:
                    break
            for path in fastq:
                if path.name not in md5s:
                    logging.warning("no MD5 found for: `%s'" % path)
                    self.no_checksum.add(path.name)
                    continue
                if md5s[path.name] is None:
                    logging.warning("ambiguous checksum for: `%s'" % path)
                    self.ambiguous_checksum.add(path.name)
                    continue
                self.inventory.append(self.fastq(path, md5s[path.name]))
            # lookup by hash table and filename
        self.lookup = dict(((t.filename.name, t.md5), t) for t in self.inventory)

    def get_path_by_name_md5(self, filename, md5sum):
        path = self.lookup.get((filename, md5sum))
        if path is None:
            if filename in self.ambiguous_checksum:
                raise AmbiguousChecksum(filename)
            elif filename in self.no_checksum:
                raise NoChecksum(filename)
            else:
                raise Unknown(filename)
        return path


class Archive(object):
    sane_uid = re.compile(r'^[0-9\.]+$')
    # empty flow cell ID is valid
    sane_flow_cell_id = re.compile(r'^[A-Z0-9_\.]*$')
    sane_filename = re.compile(r'^[^/]+$')

    def tie_metadata_to_fastq(self):
        """
        for every file in metadata, try to find the file in the FastqInventory; returns a 
        list of tuples of (fastq, metadata) tuples
        """
        unknown = ambiguous = no_checksum = 0
        matches = []
        for meta in self.metadata:
            try:
                fastq_info = self.fastq.get_path_by_name_md5(meta.filename, meta.md5)
                matches.append((fastq_info, meta))
            except AmbiguousChecksum:
                logging.error(
                    "File present in archive but ambiguous checksum %s / %s @%d" % (meta.filename, meta.md5, meta.row))
                ambiguous += 1
            except NoChecksum:
                logging.error(
                    "File present in archive but no checksum %s / %s @%d" % (meta.filename, meta.md5, meta.row))
                no_checksum += 1
            except Unknown:
                logging.error("File not found in BPA archive %s / %s @%d" % (meta.filename, meta.md5, meta.row))
                unknown += 1
        problems = ambiguous + no_checksum + unknown
        logging.info(
            "%d BPA %s metadata entries ok, %d problems (%d ambiguous, %d no checksum, %d totally unknown)" % (
            len(matches), type(self).__name__, problems, ambiguous, no_checksum, unknown))
        return matches

    def build_linktree(self, root):
        for fastq, meta in self.matches:
            folder = meta.uid.replace('/', '.') + '/' + meta.flow_cell_id
            patient_path = Path(root, folder)
            patient_path.mkdir(parents=True)
            link_file = Path(patient_path, meta.filename)
            link_file.make_relative_link_to(fastq.filename)

    def swift_path(self, fastq):
        return '%s/%s' % (self.container_name, self.base.rel_path_to(fastq.filename))

    def public_file_path(self, fastq):
        return '/files/' + self.base.rel_path_to(fastq.filename)

    def paths_for_match(self, meta, fastq):
        uid = meta.uid.replace('/', '.')
        if not Archive.sane_uid.match(uid) or not Archive.sane_flow_cell_id.match(
                meta.flow_cell_id) or not Archive.sane_filename.match(meta.filename):
            logging.error("sanity check failed, skipping: %s / %s / %s" % (uid, meta.flow_cell_id, meta.filename))
            raise Exception("invalid metadata")
        if meta.flow_cell_id:
            public_path = '/data/%s/%s/%s/%s' % (self.container_name, uid, meta.flow_cell_id, meta.filename)
        else:
            public_path = '/data/%s/%s/%s' % (self.container_name, uid, meta.filename)
        return self.swift_path(fastq), public_path

    def build_apache_redirects(self, swiftbase, outf):
        with open(outf, 'w') as fd:
            # RedirectMatch because Redirect (annoyingly) does prefix matches that can't be disabled
            # Apache wants URLs in non-% escaped form; it %-escapes them itself. hence very bodgy escaping
            # to avoid quotation marks in files breaking things

            def apache_escape(s):
                s = s.replace('\\', '\\\\')
                s = s.replace('"', '\\"')
                return s

            # make public URIs for all fastq files
            for fastq in self.fastq.inventory:
                swift_path = self.swift_path(fastq)
                swift_uri = urlparse.urljoin(swiftbase, swift_path)
                print >> fd, 'RedirectMatch "^%s$" "%s"' % (
                re.escape(self.public_file_path(fastq)), apache_escape(swift_uri))
            if self.matches is None:
                return
                # make public linktree by patient ID / flow cell
            for fastq, meta in self.matches:
                swift_path, public_path = self.paths_for_match(meta, fastq)
                swift_uri = urlparse.urljoin(swiftbase, swift_path)
                print >> fd, 'RedirectMatch "^%s$" "%s"' % (re.escape(public_path), apache_escape(swift_uri))

    def process(self, args):
        if args['--linktree']:
            root = Path(args['--linktree'])
            self.build_linktree(root)
        if args['--apacheredirects']:
            self.build_apache_redirects(args['--swiftbase'], args['--apacheredirects'])
        if args['--htmlbase']:
            self.generate_html(args['--htmlbase'], args['--linkbase'], args['--swiftbase'])
            self.generate_json_metadata(args['--htmlbase'], args['--linkbase'], args['--swiftbase'])

    def generate_html(self, output_base, publicuri, swifturi):
        env = Environment()
        env.loader = FileSystemLoader('templates/')

        def render_directory(base, bpa_id=None):
            try:
                os.mkdir(base)
            except OSError:
                pass # probably already exists
            template = env.get_template(self.template_name)
            output_filename = os.path.join(base, 'index.html')
            tmpf = output_filename + '.tmp'
            with open(tmpf, 'w') as fd:
                template_env = self.get_template_environment(publicuri, swifturi, bpa_id)
                if bpa_id is not None:
                    template_env['bpa_id'] = bpa_id
                fd.write(template.render(template_env))
            os.rename(tmpf, output_filename)

        render_directory(output_base)
        for bpa_id in self.get_bpa_ids():
            render_directory(os.path.join(output_base, bpa_id.replace('/', '.')), bpa_id)

    def generate_json_metadata(self, output_base, publicuri, swifturi):
        metadata_dict = {}
        metadata_dict['files'] = [{
                                      "url": urlparse.urljoin(publicuri, self.public_file_path(fastq)),
                                      "filename": fastq.filename.name,
                                      "md5": fastq.md5,
                                  } for fastq in self.fastq.inventory]
        metadata_dict['matches'] = match_info = []
        if self.matches is not None:
            for fastq, meta in self.matches:
                swift_path, public_path = self.paths_for_match(meta, fastq)
                match_info.append({
                    "url": urlparse.urljoin(publicuri, public_path),
                    "filename": fastq.filename.name,
                    "md5": fastq.md5,
                })
        json_filename = os.path.join(output_base, 'metadata.json')
        tmpf = json_filename + '.tmp'
        with open(tmpf, 'w') as fd:
            json.dump(metadata_dict, fd, sort_keys=True, indent=4, separators=(',', ': '))
        os.rename(tmpf, json_filename)

    def bpa_sort_key(self, bpa_id):
        return [int(t) for t in bpa_id.replace('/', '.').split('.')]

    def get_bpa_ids(self):
        """should work for all subclasses, but may need to overridden in the future"""
        if self.metadata is not None:
            last = None
            for meta in sorted(self.metadata, key=lambda m: self.bpa_sort_key(m.uid)):
                if last is None or meta.uid != last:
                    yield meta.uid
                    last = meta.uid

    def get_matches(self, bpa_id):
        for fastq, meta in self.matches:
            if bpa_id is None or meta.uid == bpa_id:
                yield fastq, meta


class MelanomaArchive(Archive):
    metadata_filename = '../../data/melanoma/Melanoma_study_metadata.xlsx'
    metadata_sheet = 'Melanoma_study_metadata'
    pilot_sheet = 'Melanoma_pilot_study'
    container_name = 'Melanoma'
    template_name = 'melanoma.html'

    def __init__(self, bpa_base):
        self.base = Path(bpa_base)
        self.fastq = FastqInventory(self.base)
        self.metadata = self.parse_metadata()
        self.matches = self.tie_metadata_to_fastq()

    def parse_metadata(self):
        wrapper = ExcelWrapper(self.metadata_filename)
        reader = wrapper.sheet_iter(self.metadata_sheet)
        metadata = []
        header = [t.strip() for t in next(reader)]
        # second header line - assert just to make sure it's still there, file format
        # hasn't changed without script update
        second_header = next(reader)

        for tpl in parse_to_named_tuple('MelanomaMeta', reader, header, [
            ('md5', 'MD5 checksum', None),
            ('filename', 'Sequence file names - supplied by sequencing facility', lambda p: p.rsplit('/', 1)[-1]),
            ('uid', 'Unique Identifier', None),
            ('flow_cell_id', 'Run #:Flow Cell ID', None),
            ('sample_name', 'Sample Name', None),
            ('date_received', 'Date Received', lambda s: excel_date_to_string(wrapper.get_date_mode(), s) ),
            ('run', 'Run number', None),
        ]):
            if tpl.filename == '':
                continue
                # tpl.filename = tpl.filename.rsplit('/', 1)[-1]
            metadata.append(tpl)

        reader = wrapper.sheet_iter(self.pilot_sheet)
        header = [t.strip() for t in next(reader)]
        if header[0] == '':
            header[0] = 'UID'

        current_uid = None
        for tpl in parse_to_named_tuple('MelanomaMeta', reader, header, [
            ('md5', 'MD5 checksum', None),
            ('filename', 'FILE NAMES - supplied by sequencing facility', lambda p: p.rsplit('/', 1)[-1]),
            ('uid', 'UID', None),
            ('flow_cell_id', 'Run #:Flow Cell ID', None),
            ('sample_name', 'Sample Name', None),
            ('date_received', 'Date Received', lambda s: excel_date_to_string(wrapper.get_date_mode(), s)),
            ('run', 'Run number', None),
        ]):
            if tpl.filename == '':
                continue
            if tpl.uid == '':
                # ugly, we have to rewrite the tuple (it's immutable)
                d = dict((t, getattr(tpl, t)) for t in dir(tpl) if
                         not t.startswith('_') and not hasattr(getattr(tpl, t), '__call__'))
                d['uid'] = current_uid
                tpl = type(tpl)(**d)
            else:
                current_uid = tpl.uid
                # tpl.filename = tpl.filename.rsplit('/', 1)[-1]
            metadata.append(tpl)

        return metadata

    def get_template_environment(self, publicuri, swifturi, bpa_id):
        objects = []
        for fastq, meta in self.get_matches(bpa_id):
            swift_path, public_path = self.paths_for_match(meta, fastq)
            url = urlparse.urljoin(publicuri, public_path)
            objects.append({
                'bpa_id': meta.uid,
                'filename': meta.filename,
                'md5': meta.md5,
                'name': meta.sample_name,
                'date_received_from_sequencing_facility': meta.date_received,
                'run': meta.run,
                'url': url,
            })
        objects.sort(key=lambda o: self.bpa_sort_key(o['bpa_id']))
        return {'object_list': objects}


class GBRArchive(Archive):
    metadata_filename = '../../data/gbr/BPA_ReFuGe2020_METADATA.xlsx'
    metadata_sheet = 'DNA library Sequencing - Pilot'
    container_name = 'GBR'
    template_name = 'gbr.html'

    def __init__(self, bpa_base):
        self.base = Path(bpa_base)
        self.fastq = FastqInventory(self.base)
        self.metadata = self.parse_metadata()
        self.matches = self.tie_metadata_to_fastq()

    def parse_metadata(self):
        metadata = []

        wrapper = ExcelWrapper(self.metadata_filename)
        reader = wrapper.sheet_iter(self.metadata_sheet)
        header = [t.strip() for t in next(reader)]
        for tpl in parse_to_named_tuple('GBRMeta', reader, header, [
            ('md5', 'MD5 checksum', None),
            ('filename', 'FILE NAMES - supplied by sequencing facility', lambda p: p.rsplit('/', 1)[-1]),
            ('uid', 'Unique ID', None),
            ('flow_cell_id', 'Run #:Flow Cell ID', None),
            ('species', 'Species', None),
            ('dataset', 'Dataset', None),
            ('sample_name', 'Sample Description', None),
            ('date_received', 'Date data sent/transferred', lambda s: excel_date_to_string(wrapper.get_date_mode(), s)),
            ('run', 'Run number', None),
        ]):
            if tpl.filename == '':
                continue
                # tpl.filename = tpl.filename.rsplit('/', 1)[-1]
            metadata.append(tpl)
        return metadata

    def get_template_environment(self, publicuri, swifturi, bpa_id):
        objects = []
        for fastq, meta in self.get_matches(bpa_id):
            swift_path, public_path = self.paths_for_match(meta, fastq)
            url = urlparse.urljoin(publicuri, public_path)
            objects.append({
                'bpa_id': meta.uid,
                'filename': meta.filename,
                'name': meta.sample_name,
                'date_received_from_sequencing_facility': meta.date_received,
                'run': meta.run,
                'url': url,
            })
        objects.sort(key=lambda o: self.bpa_sort_key(o['bpa_id']))
        return {'object_list': objects}


class WheatPathogensArchive(Archive):
    metadata_filename = '../../data/wheat_pathogens/current'
    metadata_sheet = 'Metadata'
    container_name = 'Wheat_Pathogens'
    template_name = 'wheat_pathogens.html'

    def __init__(self, bpa_base):
        self.base = Path(bpa_base)
        self.fastq = FastqInventory(self.base)
        self.metadata = self.parse_metadata()
        self.matches = self.tie_metadata_to_fastq()

    def parse_metadata(self):
        metadata = []

        wrapper = ExcelWrapper(self.metadata_filename)
        reader = wrapper.sheet_iter(self.metadata_sheet)
        header = [t.strip() for t in next(reader)]
        for tpl in parse_to_named_tuple('WheatPathogensMeta', reader, header, [
            ('md5', 'MD5 checksum', None),
            ('filename', 'FILE NAMES - supplied by AGRF', lambda p: p.rsplit('/', 1)[-1]),
            ('uid', 'BPA ID', None),
            ('flow_cell_id', 'Run #:Flow Cell ID', None),
            ('species', 'Species', None),
            ('official_variety_name', 'Official Variety Name', None),
            ('run', 'Run number', lambda s: s.replace('RUN #', '')),
        ]):
            if tpl.filename == '' or tpl.uid == '':
                continue
                # tpl.filename = tpl.filename.rsplit('/', 1)[-1]
            metadata.append(tpl)
        return metadata

    def get_template_environment(self, publicuri, swifturi, bpa_id):
        objects = []
        for fastq, meta in self.get_matches(bpa_id):
            swift_path, public_path = self.paths_for_match(meta, fastq)
            url = urlparse.urljoin(publicuri, public_path)
            objects.append({
                'bpa_id': meta.uid,
                'filename': meta.filename,
                'name': meta.official_variety_name,
                'run': meta.run,
                'url': url,
            })
        objects.sort(key=lambda o: self.bpa_sort_key(o['bpa_id']))
        return {'object_list': objects}


class NoMetadataArchive(Archive):
    def __init__(self, bpa_base):
        self.base = Path(bpa_base)
        self.fastq = FastqInventory(self.base)
        self.metadata = None
        self.matches = None

    def get_template_environment(self, publicuri, swifturi, bpa_id):
        objects = []
        for fastq in sorted(self.fastq.inventory, key=lambda f: f.filename.name):
            public_file_path = self.public_file_path(fastq)
            url = urlparse.urljoin(publicuri, public_file_path)
            objects.append({
                'filename': fastq.filename.name,
                'md5': fastq.md5,
                'url': url,
            })
        return {'object_list': objects}


class Wheat7aArchive(NoMetadataArchive):
    container_name = 'Wheat7a'
    template_name = 'wheat7a.html'


class BASEArchive(NoMetadataArchive):
    container_name = 'BASE'
    template_name = 'base.html'


class WheatPathogensArchiveOld(NoMetadataArchive):
    container_name = 'Wheat_Pathogens'
    template_name = 'wheat_pathogens_old.html'


class WheatCultivarsArchive(NoMetadataArchive):
    container_name = 'Wheat_Cultivars'
    template_name = 'wheat_cultivars.html'


if __name__ == '__main__':
    def sanity_check(args):
        def test_path(path):
            if not Path(path).exists():
                sys.exit("The folder {0} does not exist. Quitting".format(path))

        # does the source folder exist ?
        test_path(args['SUBARCHIVE_ROOT'])

    def run_archive(cls, args):
        archive = cls(args['SUBARCHIVE_ROOT'])
        archive.process(args)

    def run():
        if args['melanoma']:
            run_archive(MelanomaArchive, args)
        elif args['gbr']:
            run_archive(GBRArchive, args)
        elif args['wheat7a']:
            run_archive(Wheat7aArchive, args)
        elif args['wheat_pathogens']:
            run_archive(WheatPathogensArchive, args)
        elif args['wheat_cultivars']:
            run_archive(WheatCultivarsArchive, args)
        elif args['base']:
            run_archive(BASEArchive, args)

    args = docopt(__doc__, version=__version__)
    if args['--verbose']:
        logging.info(args)
    sanity_check(args)
    run()
