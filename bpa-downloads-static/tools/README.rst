Linktree Factory
================

This tool takes a source data directory and builds a linktree directory in a target directory, using
a predefined format.

A section of the melanoma project's linktree looks like this::

    /home/thys/melanoma/
    ├── 102.100.100.10781
    │   ├── 10781_UNSW_D27DEACXX_NoIndex_L007_R1_001.fastq.gz -> ../../bpaarchive/RAW/Ramaciotti/BRLOPS-80/10781_UNSW_D27DEACXX/10781_UNSW_D27DEACXX_NoIndex_L007_R1_001.fastq.gz
    │   ├── 10781_UNSW_D27DEACXX_NoIndex_L007_R2_001.fastq.gz -> ../../bpaarchive/RAW/Ramaciotti/BRLOPS-80/10781_UNSW_D27DEACXX/10781_UNSW_D27DEACXX_NoIndex_L007_R2_001.fastq.gz
    │   └── checksums.md5
    ├── 102.100.100.10782
    │   ├── 10782_UNSW_D272BACXX_NoIndex_L003_R1_001.fastq.gz -> ../../bpaarchive/RAW/Ramaciotti/BRLOPS-80/10782_UNSW_D272BACXX/10782_UNSW_D272BACXX_NoIndex_L003_R1_001.fastq.gz
    │   ├── 10782_UNSW_D272BACXX_NoIndex_L004_R2_001.fastq.gz -> ../../bpaarchive/RAW/Ramaciotti/BRLOPS-80/10782_UNSW_D272BACXX/10782_UNSW_D272BACXX_NoIndex_L004_R2_001.fastq.gz
    │   └── checksums.md5
    ├── 102.100.100.10783    

That would be::

    melanoma/<melanoma-project-id>.<patient-id>/*.fastq.gz
    melanoma/<melanoma-project-id>.<patient-id>/cheksums.md5


This module walks through a data source folder. The folder contains data from several different data providers.
Each data provider's source format is slightly different.

The data process problem is modeled using the following:

- A process tree, just a file tree with directories and data file symlinks back to the original data, see sample above.
- A Linker for each of the source data types, a linker
- A Linktree Node object, each datafile is presented by a Node
- The node keeps enough state to link itself into the linktree
