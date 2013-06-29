from django.db import models


class Affiliation(models.Model):
    """
    Affiliation
    """
    name = models.CharField(max_length=100)


class DNASource(models.Model):
    """
    DNA Source
    """
    source = models.CharField(max_length=100)


class Facility(models.Model):
    """
    The Sequencing Facility
    """
    name = models.CharField(max_length=100)


class Contact(models.Model):
    """
    Contact Detail
    """
    name = models.CharField(max_length=200)
    affiliation = models.ForeignKey(Affiliation)
    email = models.CharField(max_length=200)


class Sample(models.Model):
    """
    A sample
    """

    bpa_sample_id = models.CharField(max_length=16)
    sample_name = models.CharField(max_length=200)
    requested_sequence_coverage = models.CharField(max_length=4)
    species = models.CharField(max_length=100)
    sequencing_faciltiy = models.ForeignKey(Facility)
    dna_source = models.ForeignKey(DNASource)

    sex = models.CharField(max_length=1)

