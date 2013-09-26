#! /usr/bin/env python
# coding: utf-8

"""  
Usage: 
  bpalink.py [options] (melanoma | wheat_pathogens | wheat_cultivars | coral | base) ARCHIVE_ROOT LINKTREE_ROOT

Options:
  -n --dry-run  Don't affect the target tree in any way.
  -v --verbose  Verbose mode.
  -c --checksums-filename=NAME  The filename to use for the generated checksums [default: checksums.md5].
  -i --datasetid=DATASETIDS  A list of dataset IDs, a empty set means all of them.

"""

from docopt import docopt
from unipath import Path
import StringIO, unipath
import pprint
import sys
from tendo import colorer
import logging

logging.basicConfig(level=logging.DEBUG)

__version__ = "1.1.0"

# this ID never changes... it captures the place where it was minted.
BPA_PREFIX = '102.100.101'


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


class BPAConfig(object):
    """
    This provides a simple lookup for the BPA Archive layout and other config parameters.
    """

    PROJECT_METADATA = {'melanoma': {'name': 'Melanoma', 'source': 'Melanoma'},
                        'wheat_pathogens': {'name': 'Wheat Pathogens', 'source': 'Wheat_Pathogens'},
                        'wheat_cultivars': {'name': 'Wheat Cultivars', 'source': 'Wheat_Cultivars'},
                        'coral': {'name': 'Coral', 'source': 'Coral'},
                        'base': {'name': 'BASE', 'source': 'BASE'},
                        }

    PROVIDER_DATA = {'agrf': {'source_folder': 'raw/agrf'},
                     'ramaciotti': {'source_folder': 'raw/ramaciotti'},
                     }

    def __init__(self, args):
        self.args = args
        self.archive_root = args['ARCHIVE_ROOT']

    def get_project_raw_path(self, project_name):
        """
        Returns the raw data Path for the given project
        :param project_name:
        """
        projects = self.PROJECT_METADATA.keys()
        if project_name not in projects:
            logging.error("{0} is not a valid project name".format(project_name))
            logging.info("Try one of {0}".format(pprint.pformat(projects)))
            exit(1)

        return Path(self.PROJECT_METADATA[project_name]['source'])

    def get_provider_raw_path(self, provider_name):
        """
        Returns the relative data Path given the provider
        """
        providers = self.PROVIDER_DATA.keys()
        if provider_name not in providers:
            logging.error("Provider {0} is not valid".format(provider_name))
            logging.info("Try one of {0}".format(pprint.pformat(providers)))
            exit(1)

        return Path(self.PROVIDER_DATA[provider_name]['source_folder'])

    def get_project_provider_raw_path(self, project_name, provider_name):
        """
        Returns the raw data path given the project and the provider.
        """
        project_path = self.get_project_raw_path(project_name)
        provider_path = self.get_provider_raw_path(provider_name)

        return Path(project_path, provider_path)

    def get_project_provider_absolute_raw_path(self, project_name, provider_name):
        """
        Return the absolute raw path given the archive directory, the project and the provider.
        """
        return Path(self.archive_root, self.get_project_provider_raw_path(project_name, provider_name))


class MD5Load(object):
    """
    Selects between the various md5 file formats in the archive.
    Prefers checksums.md5
    """

    def load(self, parent_folder):
        """
        Load md5 data
        """

        # attempted in order, first to return a dictionary wins
        fns = [
            self.load_md5sum_file,
            self.load_md5sum_exf_file, 
            lambda *args: self.load_md5sum_file(*args, source_checksums_file='checksums.cortex.md5'),
        ]
        for fn in fns:
            sums = fn(parent_folder)
            if sums is not None:
                return sums
        logging.warning("No md5 sums loaded - returning empty dictionary.")
        return {}

    def load_md5sum_file(self, parent_folder, source_checksums_file='checksums.md5'):
        """
        Loads md5 sums from checksum file into dict.
        :param parent_folder:
        :param source_checksums_file:
        :return: dict
        """

        md5file = Path(parent_folder, source_checksums_file)
        if md5file.exists():
            sums = {}
            logging.info('Loading {0}'.format(md5file))
            for l in md5file.read_file().splitlines():
                checksum, filename = l.split()
                sums[filename] = checksum
            return sums
        else:
            logging.warning("No {0} file found in {1}".format(source_checksums_file, parent_folder))
        return None

    def load_md5sum_exf_file(self, parent_folder, source_checksums_file='checksums.exf'):
        """
        Return a dictionary of file:md5sum pairs for the given folder.
        AGRF ships folders with .exf files that contains md5 checksums.
        """

        def set_sums():
            """
            Populate the checksums dict
            """
            for l in exf_file.read_file().splitlines():
                # ignore comments and empty lines
                if (l.strip().find(';') == 0) or l == "":
                    continue
                chksum, _, filename = l.partition(" *")
                sums[filename] = chksum

        def get_exf():
            """
            .exf files are not always consistently named, search for and return the first one found.
            """
            exf = Path(parent_folder, source_checksums_file)
            if not exf.exists():
                logging.warning("No {0} file found in {1}".format(source_checksums_file, parent_folder))
                # search for alternative .exf files in current folder
                lst = parent_folder.listdir(pattern='*exf')
                if len(lst) > 0:
                    exf = lst[0]
                else:
                    logging.warning("Could not find any .exf files in {0}".format(parent_folder))
            return exf

        exf_file = get_exf()
        if exf_file.exists():
            sums = {}
            logging.info('Loading {0}'.format(exf_file))
            set_sums()
            return sums
        return None

class LinkNode(object):
    """
    A single node in the tree. It represents a file to be linked
    """

    def __init__(self, args):
        self.args = args
        self.md5sum = ""
        self.filename = None
        self.source_path = None
        self.link_path = None
        self.patient_id = None
        self.patient_path = None
        self.flowcell_id = None

    def make_patient_folder(self):
        """
        This Node knows where to make a place for itself in the tree
        """

        if self.patient_id:
            folder = BPA_PREFIX + '.' + self.patient_id
            patient_path = Path(self.args['LINKTREE_ROOT'], folder)
            logging.info("Making patient folder: %s" % (patient_path))
            patient_path.mkdir(parents=True)
            self.patient_path = patient_path
        else:
            logging.warning("Cannot make this node's parent folder as the patient ID is not set.")

    def process(self):
        if not self.args['--dry-run']:
            self.make_patient_folder()
            link_file = Path(self.patient_path, self.filename)
            link_file.make_relative_link_to(self.source_path)

    def write_md5_sum(self):
        """ 
        Write my md5_sum to local checksums.md5. 
        """

        # load the exiting file, if it exist 
        sums = MD5Load().load_md5sum_file(self.patient_path)
        if sums is None:
            sums = {}
        sums[self.filename] = self.md5sum

        # flush the sums to disk            
        new_md5 = StringIO.StringIO()
        keys = sums.keys()
        keys.sort()
        for key in keys:
            new_md5.write(sums[key] + '  ' + key + "\n")  # notice the two spaces...

        checksums_file = Path(self.patient_path, self.args['--checksums-filename'])
        checksums_file.write_file(new_md5.getvalue())

    def __str__(self):
        return "{0} {1}".format(self.filename, self.md5sum)


class NodeFactory(object):
    """
    A Link Node Factory. Links existing data sets into user-specified trees
    """

    def __init__(self, project_name, provider_name, args):

        self.bpa_config = BPAConfig(args)
        self.source_folder = self.bpa_config.get_project_provider_absolute_raw_path(project_name, provider_name)
        logging.info("Factory source folder: {0}".format(self.source_folder))

        if self.source_folder.exists():
            logging.info("{0} source folder found".format(provider_name))
        else:
            logging.warning("Did not find {0} source folder in {1}".format(provider_name, self.source_folder))

    def get_brlops_folders(self):
        """
        Data sets must be curated, for us this means it has a JIRA ticket.
        """
        return self.source_folder.listdir(pattern='BRLOPS*')
    
    @classmethod
    def get_fastq_files(cls, sub):
        return sub.listdir(pattern="*fastq.gz", filter=unipath.FILES)

    @classmethod
    def get_fastq_subdirs(cls, base):
        """
        Returns Path instances for each folder containing one or more fastq files.
        """
        for sub in base.walk(filter=unipath.DIRS):
            fastq = NodeFactory.get_fastq_files(sub)
            if len(fastq) > 0:
                yield sub

class MelanomaRamaciottiNodeFactory(NodeFactory):
    """
    Ramaciotti node builder for the Melanoma Project
    """

    def __init__(self, args):
        super(MelanomaRamaciottiNodeFactory, self).__init__('melanoma', 'ramaciotti', args)
        self.args = args

    def process(self):
        """
        Process the source files
        """

        def write_md5sum(nodes, patient_id):
            """
            Add new md5sum entries to existing checksums.md5 file in patient folder
            """

            existing_md5checksums = Path(self.args['LINKTREE_ROOT'], BPA_PREFIX + "." + patient_id,
                                        self.args['--checksums-filename'])
            sums = MD5Load().load_md5sum_file(existing_md5checksums)
            if sums is None:
                sums = {}

            # add the new sums to the dict           
            for node in nodes:
                sums[node.filename] = node.md5sum

            # flush the dict to disk            
            new_md5 = StringIO.StringIO()
            keys = sums.keys()
            keys.sort()
            for key in keys:
                new_md5.write(sums[key] + '  ' + key + "\n")

            existing_md5checksums.write_file(new_md5.getvalue())

        def make_nodes(sub_folder, patient_id, flowcell_id):
            sums = MD5Load().load(sub_folder)
            nodes = []

            logging.info("Make nodes: %s" % (sub_folder))

            fastq = NodeFactory.get_fastq_files(sub_folder)
            for data_file in fastq:
                node = LinkNode(self.args)
                node.patient_id = patient_id
                node.make_patient_folder()
                node.source_path = Path(data_file)
                node.filename = data_file.name
                node.flowcell_id = flowcell_id
                if node.filename not in sums:
                    logging.error("Cannot look up MD5 sum for `%s'." % (node.filename))
                    continue
                node.md5sum = sums[node.filename]
                nodes.append(node)
                node.process()

            if len(fastq) > 0:
                write_md5sum(nodes, patient_id)

        for jira_ticket_folder in self.get_brlops_folders():
            # for Ramaciotti data sets the sub folders are like so: 10781_UNSW_D27DEACXX, patient_id, UNSW, flowcell_id
            for sub_folder in NodeFactory.get_fastq_subdirs(jira_ticket_folder):
                logging.info("MelanomaRamaciottiNodeFactory: entering %s" % (sub_folder))
                try:
                    patient_id, nsw, flowcell_id = sub_folder.name.split('_')
                    _ = int(patient_id) # test that patient ID is an integer
                    logging.info("Parsed folder name: `%s' -> %s, %s, %s" % (sub_folder, patient_id, nsw, flowcell_id))
                    make_nodes(sub_folder, patient_id, flowcell_id)
                except ValueError:
                    logging.error("Cannot parse folder name: `%s'" % (sub_folder))


class MelanomaAGRFNodeFactory(NodeFactory):
    """
    Builds link nodes for the Melanoma Project with data from AGRF
    """

    def __init__(self, args):
        super(MelanomaAGRFNodeFactory, self).__init__('melanoma', 'agrf', args)
        self.args = args

    def process_data_file(self, data_file, md5sum):
        """
        Process the AGRF provided data file
        """

        patient = data_file.name.partition('_')[0]
        if patient != '' and is_number(patient):
            node = LinkNode(self.args)
            node.md5sum = md5sum
            node.patient_id = patient
            node.source_path = data_file
            node.filename = data_file.name
            node.make_patient_folder()
            node.process()
            node.write_md5_sum()
            logging.info("Linked node: {0}".format(node))

    def process(self):
        """
        Process the BRLOPS directories in Melanoma/agrf/
        """
        for data_set in self.get_brlops_folders():
            logging.info("Processing Dataset {0}".format(data_set))
            for sub in NodeFactory.get_fastq_subdirs(data_set):
                logging.info("Processing folder {0} in data_set {1}".format(sub, data_set))
                md5dict = MD5Load().load(sub)
                # AGRF file names contain the patient number
                for data_file in NodeFactory.get_fastq_files(sub):
                    try:
                        self.process_data_file(data_file, md5dict[data_file.name])
                    except KeyError as e:
                        logging.error("Cannot look up MD5 sum for `%s'." % (data_file))
                        logging.error(pprint.pformat(md5dict))


if __name__ == '__main__':

    def run():
        if args['melanoma']:
            # build the Ramaciotti nodes
            ramaciotti = MelanomaRamaciottiNodeFactory(args)
            ramaciotti.process()

            # build the AGRF nodes
            agrf = MelanomaAGRFNodeFactory(args)
            agrf.process()

    def sanity_check(args):
        def test_path(path):
            if not Path(path).exists():
                sys.exit("The folder {0} does not exist. Quitting".format(path))

        # does the source folder exist ?
        test_path(args['ARCHIVE_ROOT'])
        test_path(args['LINKTREE_ROOT'])

    args = docopt(__doc__, version=__version__)
    if args['--verbose']:
        logging.info(args)
    sanity_check(args)
    run()
    
    

        
    
    

