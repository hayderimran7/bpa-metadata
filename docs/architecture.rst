Architecture and Implementation Overview
========================================

* The Metadata project is implemented in the Django web framework.

Applications
------------

* There is a single Django Application for each BPA project. This includes:
    * Melanoma
    * Biome of Australian Soil Environments (BASE)
    * Great Barrier Reef (GBR)
    * Wheat Cultivars
    * Wheat Pathogens
    * Wheat Chromosome 7A
    * etc.

Downloads endpoint
------------------
* There is a single data portal endpoint that makes all raw data available. This includes:
    * Sequence data, typically fastq.gz files
    * The associated metadata, typically xlsx or csv spreadsheets.

Metadata front-end(s)
---------------------
* There are a few BPA Metadata front-end sites, depending on the development life-cycle, each with its own back-end database.
* Staging - for staging potential new releases.
* Production - the production site.
* Demo, there may be a demo site, depending on demand.

Metadata Ingestion
------------------
Because of the diverse nature of the different metadata formats individual data ingestion
scripts are used to pack the metadata into the database.

Once the database has been provisioned the data ingestion scripts are used to pack the metadata from the xlsx spreadsheets
into the database. This happens first on staging, and then on production.

