# -*- coding: utf-8 -*-

from django.db import models
from apps.common.models import SequenceFile, BPAUniqueID, Facility


class Host(models.Model):
    '''Host from who sepsis sample was collected'''

    description = models.CharField('Host Description', max_length=200, blank=True, null=True)
    location = models.CharField('Host Location', max_length=200, blank=True, null=True, help_text='State, Country')
    sex = models.CharField('Host Sex', max_length=1, blank=True, null=True, choices=(('M', 'Male'), ('F', 'Female')))
    age = models.IntegerField('Host Age', blank=True, null=True)
    dob = models.DateField('Host Day of Birth', blank=True, null=True, help_text='DD/MM/YY')
    disease_outcome = models.TextField('Host Disease Outcome', blank=True, null=True)
    strain_or_isolate = models.CharField('Strain Or Isolate', max_length=200, blank=True, null=True, unique=True)

    associated = models.CharField('Host Associated', max_length=200, blank=True, null=True)
    health_state = models.CharField('Host Health State', max_length=200, blank=True, null=True)
    disease_status = models.CharField('Host Disease Status', max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = 'Host'

    def __unicode__(self):
        return '{} {}'.format(self.strain_or_isolate, self.location)


class GrowthMethod(models.Model):
    '''Sample preparation method metadata'''

    note = models.TextField('Note', max_length=500, blank=True, null=True)
    growth_condition_temperature = models.IntegerField('Growth condition temperature',
                                                       blank=True,
                                                       null=True,
                                                       help_text='Degrees Centigrade')
    growth_condition_time = models.CharField('Growth condition time',
                                             max_length=500,
                                             blank=True,
                                             null=True, )
    growth_condition_media = models.CharField('Growth condition media', max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = 'Growth Method'

    def __unicode__(self):
        return u'{} {}'.format(self.growth_condition_media,
                               self.growth_condition_temperature, )


class MiseqGenomicsMethod(models.Model):
    '''Genomics Metadata'''

    # Genomics method data from excell spreadsheet
    # Bacterial sample unique ID	Insert size range	Library construction protocol	Sequencer	AnalysisSoftwareVersion

    library_construction_protocol = models.CharField('Library Construction Protocol',
                                                     max_length=100,
                                                     blank=True,
                                                     null=True)
    insert_size_range = models.CharField('Insert Size Range', max_length=20, blank=True, null=True)
    sequencer = models.CharField('Sequencer', max_length=100, blank=True, null=True)
    analysis_software_version = models.CharField('Analysis Software Version', max_length=20, blank=True, null=True)

    class Meta:
        verbose_name = 'Miseq Genomics Method'

    def __unicode__(self):
        return u'{} {} {}'.format(self.library_construction_protocol, self.insert_size_range, self.sequencer)


class PacBioGenomicsMethod(models.Model):
    '''PacBio Genomics Metadata'''

    # Genomics method data from excell spreadsheet
    # Bacterial sample unique ID	Insert size range	Library construction protocol	Sequencer	Run ID	SMRT Cell ID	Cell Position	RS version

    library_construction_protocol = models.CharField('Library Construction Protocol',
                                                     max_length=500,
                                                     blank=True,
                                                     null=True)
    insert_size_range = models.CharField('Insert Size Range', max_length=40, blank=True, null=True)
    sequencer = models.CharField('Sequencer', max_length=200, blank=True, null=True)
    sequencer_run_id = models.CharField('Sequencer run ID', max_length=100, blank=True, null=True)
    smrt_cell_id = models.CharField('SMRT Cell ID', max_length=60, blank=True, null=True)
    cell_position = models.CharField('Cell Position', max_length=60, blank=True, null=True)
    rs_version = models.CharField('RS Version', max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = 'PacBio Genomics Method'

    def __unicode__(self):
        return u'{} {} {}'.format(self.library_construction_protocol, self.insert_size_range, self.sequencer)


class ProteomicsMethod(models.Model):
    '''Proteomics Metadata'''

    sample_fractionation = models.IntegerField('Sample Fractionation', blank=True, null=True)
    lc_column_type = models.CharField('LC/column type', max_length=100, blank=True, null=True)
    gradient = models.CharField('Gradient time (min)  /  % ACN (start-finish main gradient) / flow',
                                max_length=100,
                                blank=True,
                                null=True)
    column = models.CharField('Sample on column(µg) ', max_length=100, blank=True, null=True)
    mass_spectrometer = models.CharField('Mass Spectrometer', max_length=100, blank=True, null=True)
    aquisition_mode = models.CharField('Acquisition Mode / fragmentation', max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = 'Proteomics Method'

    def __unicode__(self):
        return u'{} {} {}'.format(self.sample_fractionation, self.lc_column_type, self.mass_spectrometer)


# TODO
class TranscriptomicsMethod(models.Model):
    '''Transcriptomics Metadata'''

    # Bacterial sample unique ID	Insert size range	Library construction protocol	Sequencer	CASAVA version
    library_construction_protocol = models.CharField('Library Construction Protocol',
                                                     max_length=100,
                                                     blank=True,
                                                     null=True)
    insert_size_range = models.CharField('Insert Size Range', max_length=20, blank=True, null=True)
    sequencer = models.CharField('Sequencer', max_length=100, blank=True, null=True)
    casava_version = models.CharField('CASAVA Version', max_length=20, blank=True, null=True)

    class Meta:
        verbose_name = 'Transcriptomics Method'

    def __unicode__(self):
        return u'{} {} {}'.format(self.library_construction_protocol, self.insert_size_range, self.sequencer)


class SampleTrack(models.Model):
    ''' Track the Sepsis Sample '''

    # 5 digit BPA ID
    # Taxon_OR_organism
    # Strain_OR_isolate
    # Serovar
    # Growth Media
    # Replicate
    # Omics
    # Analytical platform
    # Facility
    # Work order
    # Contextual Data Submission Date
    # Sample submission FIXME, no need for flag if date is set, date is flag
    # Sample submission date
    # Data generated
    # Archive ID
    # Archive Ingestion Date

    bpa_id = models.ForeignKey(BPAUniqueID,
                               null=True,
                               verbose_name='BPA ID',
                               help_text='Bioplatforms Australia Sample ID')

    #bpa_id = models.CharField('BPA ID', max_length=6)
    taxon_or_organism = models.CharField('Taxon or Organism', max_length=200, blank=True, null=True)
    strain_or_isolate = models.CharField('Strain Or Isolate', max_length=200, blank=True, null=True)
    serovar = models.CharField('Serovar', max_length=500, blank=True, null=True)
    growth_media = models.CharField('Growth Media', max_length=500, blank=True, null=True)
    replicate = models.IntegerField('Replicate', blank=True, null=True)
    omics = models.CharField('Omics Type', max_length=50, blank=True, null=True)
    analytical_platform = models.CharField('Analytical Platform', max_length=100, blank=True, null=True)
    # facility = models.ForeignKey(Facility, blank=True, null=True)
    facility = models.CharField('Facility', max_length=100, blank=True, null=True)
    work_order = models.CharField('Work Order', max_length=50, blank=True, null=True)
    contextual_data_submission_date = models.DateField('Contextual Data Submission Date', blank=True, null=True, help_text='YYYY-MM-DD')
    sample_submission_date = models.DateField('Sample Submission Date', blank=True, null=True, help_text='YYYY-MM-DD')
    data_generated = models.NullBooleanField('Data Generated', default=False)
    archive_ingestion_date = models.DateField('Archive Ingestion Date', blank=True, null=True, help_text='YYYY-MM-DD')
    curation_url = models.URLField('Curation URL', blank=True, null=True)
    dataset_url = models.URLField('Download URL', blank=True, null=True)

    def __unicode__(self):
        return u'{} {} {}'.format(self.bpa_id, self.taxon_or_organism, self.omics)

    class Meta:
        abstract = True
        verbose_name = 'Sample Tracking Information'
        verbose_name_plural = 'Sample Tracking'

class PacBioTrack(SampleTrack):
    class Meta:
        verbose_name = 'PacBio Tracking Information'
        verbose_name_plural = verbose_name

class MiSeqTrack(SampleTrack):
    class Meta:
        verbose_name = 'MiSeq Tracking Information'
        verbose_name_plural = verbose_name

# Little point in expanding the common Sample Type
class SepsisSample(models.Model):
    ''' Sepsis Sample '''

    bpa_id = models.OneToOneField(BPAUniqueID,
                                  verbose_name='BPA ID',
                                  primary_key=True,
                                  help_text='Bioplatforms Australia Sample ID')

    host = models.ForeignKey(Host, blank=True, null=True, related_name='samples', help_text='Sample donor host')

    growth_method = models.ForeignKey(GrowthMethod,
                                      blank=True,
                                      null=True,
                                      related_name='samples',
                                      help_text='Sample Growth Method')

    # FIXME
    #sample_track = models.OneToOneField(SampleTrack,
    #                                    blank=True,
    #                                    null=True,
    #                                    related_name='sample',
    #                                    help_text='Sample Tracking')

    taxon_or_organism = models.CharField('Taxon or Organism', max_length=200, blank=True, null=True)
    strain_or_isolate = models.CharField('Strain Or Isolate', max_length=200, blank=True, null=True)
    strain_description = models.CharField('Strain Description', max_length=300, blank=True, null=True)
    gram_stain = models.CharField('Gram Staining', max_length=3, choices=(('POS', 'Positive'), ('NEG', 'Negative')))
    serovar = models.CharField('Serovar', max_length=500, blank=True, null=True)
    key_virulence_genes = models.CharField('Key Virulence Genes', max_length=500, blank=True, null=True)

    isolation_source = models.CharField('Isolation Source', max_length=500, blank=True, null=True)
    isolation_growth_conditions = models.CharField('Isolation Growth Conditions', max_length=500, blank=True, null=True)

    publication_reference = models.CharField('Publication Reference', max_length=200, blank=True, null=True)
    contact_researcher = models.CharField('Contact Researcher', max_length=200, blank=True, null=True)
    culture_collection_date = models.DateField('Collection Date', blank=True, null=True, help_text='YYYY-MM-DD')
    culture_collection_id = models.CharField('Culture Collection ID', max_length=100, blank=True, null=True)

    study_title = models.CharField('Study Title', max_length=200, blank=True, null=True)
    investigation_type = models.CharField('Investigation Type', max_length=200, blank=True, null=True)
    project_name = models.CharField('Project Name', max_length=200, blank=True, null=True)
    sample_title = models.CharField('Sample Title', max_length=200, blank=True, null=True)
    ploidy  = models.CharField('Ploidy', max_length=200, blank=True, null=True) # FIXME, what is ploidy ?
    num_replicons  = models.CharField('Number of Replicons', max_length=200, blank=True, null=True)
    estimated_size  = models.CharField('Estimated Size', max_length=200, blank=True, null=True)
    propagation =  models.CharField('Propagation', max_length=200, blank=True, null=True)
    collected_by = models.CharField('Collected By', max_length=200, blank=True, null=True)


    def __unicode__(self):
        return ' '.join([e for e in (self.bpa_id.get_short_name(), self.taxon_or_organism, self.strain_or_isolate) if e])

    class Meta:
        verbose_name = 'Sepsis Sample'


class SepsisSequenceFile(SequenceFile):
    ''' Sequence Files '''

    project_name = 'sepsis'
    sample = models.ForeignKey(SepsisSample, related_name='%(app_label)s_%(class)s_files')

    def __unicode__(self):
        return u'{}'.format(self.filename)

    class Meta:
        abstract = True


class ProteomicsFile(SepsisSequenceFile):
    '''Sequence file from the proteomics analysis process'''

    def __unicode__(self):
        return u'{}'.format(self.filename)


class GenomicsFile(SepsisSequenceFile):
    '''Sequence file from the genomics analysis process'''

    extraction = models.IntegerField('Extraction', default=1)
    vendor = models.CharField('Vendor', max_length=100, default=1)

    class Meta:
        abstract = True


class GenomicsMiseqFile(GenomicsFile):
    '''Genomics Miseq'''

    method = models.ForeignKey(MiseqGenomicsMethod,
                               null=True,
                               related_name='%(app_label)s_%(class)s_files',
                               help_text='Genomics Method')

    library = models.CharField('Library', max_length=20, help_text='MP or PE')
    size = models.CharField('Extraction Size', max_length=100, default=1)
    flow_cell_id = models.CharField('Flow Cell ID', max_length=6)
    index = models.CharField('Index', max_length=20)
    runsamplenum = models.CharField('Sample Run Number', max_length=20)
    read = models.CharField('Read', max_length=3)

    def get_path_parts(self):
        return (self.project_name, 'genomics/miseq')

    def __unicode__(self):
        return u'Genomics Miseq {}'.format(self.filename)


class GenomicsPacBioFile(GenomicsFile):
    '''Genomics PacBio'''

    method = models.ForeignKey(PacBioGenomicsMethod,
                               null=True,
                               related_name='%(app_label)s_%(class)s_files',
                               help_text='PacBio Genomics Method')

    library = models.CharField('Library', max_length=20, help_text='MP or PE')
    size = models.CharField('Extraction Size', max_length=100, default=1)
    flow_cell_id = models.CharField('Flow Cell ID', max_length=6)
    index = models.CharField('Index', max_length=20)
    runsamplenum = models.CharField('Sample Run Number', max_length=20)
    read = models.CharField('Read', max_length=3)

    def get_path_parts(self):
        return (self.project_name, 'genomics/pacbio')

    def __unicode__(self):
        return u'Genomics Miseq {}'.format(self.filename)


class TranscriptomicsFile(SepsisSequenceFile):
    '''Sequence file from the transcriptomics analysis process'''

    def __unicode__(self):
        return u'{}'.format(self.filename)
