# Bioplatforms Australia  Metadata Management

BPA Metadata is a web portal into Bioplatforms Australia's genomics sequencing data 
archive. It aims to aggregate all relevant meta and sequence data into a coherent data 
navigation system.

## Development
bpa-metada is available as a fully contained Dockerized stack. 

For development, or to use the bpa-metadata archive as a 'offline' [1] contained local tool that uses 
its own local DB.

### Quick Setup

* [Install docker and compose](https://docs.docker.com/compose/install/)
* git clone https://github.com/muccg/bpa-metadata.git
* `./develop.sh up`
* `./develop.sh ingest_all`

`develop.sh up` will spin up the stack. See `./develop.sh usage` for some utility methods, which typically are simple 
wrappers arround docker:

```bash
Usage ./develop.sh (build|shell|unit_tests|selenium|superuser|up|rm|runscript|ingest_all)
                   build        Build all images
                   mint         Mint and push new docker images from current checked out tag
                   shell        Create and shell into a new web image, used for db checking with Django env available
                   superuser    Create Django superuser
                   runscript    Run one of the available scripts
                   ingest_all   Ingest metadata
                   checksecure  Run security check
                   up           Spins up docker image stack
                   rm           Remove all containers
                   pythonlint   Run python lint
                   unit_tests   Run unit tests
                   selenium     Run selenium tests
                   usage
```

## Sites
- *Production* https://ccgapps.com.au/bpa-metadata/
- *Staging* https://staging.ccgapps.com.au/bpa-metadata/

## Licence
BPA Metadata is released under the GNU Affero GPL. See source for a licence copy.

## Contributing
* Fork next_release branch
* Make changes on a feature branch
* Submit pull request

## CCG Internal documentation

https://ccgmurdoch.atlassian.net/wiki/display/BM/BPA+Metadata+Home

[1]: Be aware that all CDN supported content still needs to be fetched from the internet. 
