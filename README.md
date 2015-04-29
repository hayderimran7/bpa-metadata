# Bioplatforms Australia  Metadata Management

BPA Metadata is a web portal into Bioplatforms Australia's genomics sequencing data 
archive. It aims to aggregate all relevant meta and sequence data into a coherent data 
navigation system.

## Development
bpa-metada is available as a fully contained Dockerized stack. `develop.sh up` will spin up
the stack. See `./develop.sh usage` for some utility methods, which typically are simple 
wrappers arround docker:

```bash
Usage ./develop.sh (build|shell|unit_tests|selenium|superuser|up|rm|rpm_build|rmp_publish|ingest|ingest_all)
                   build        Build all images
                   shell        Create and shell into a new web image, used for db checking with Django env available
                   superuser    Create Django superuser
                   ingest       Ingest metadata
                   ingest_all       Ingest metadata
                   checksecure  Run security check
                   up           Spins up docker image stack
                   rm           Remove all containers
                   rpm_build    Build rpm
                   rpm_publish  Publish rpm
                   ci_staging   Continuous Integration staging
                   rpm_publish  Publish rpm
                   pythonlint   Run python lint
                   jslint       Run javascript lint
                   unit_tests   Run unit tests
                   selenium     Run selenium tests
                   usage
```

## Sites
- *Production* https://ccgapps.com.au/bpa-metadata/
- *Staging* https://staging.ccgapps.com.au/bpa-metadata/

## Licence
BPA Metadata is released under the GPL Version 3.0 licence. See source for a licence copy.


## CCG Internal documentation

https://ccgmurdoch.atlassian.net/wiki/display/BM/BPA+Metadata+Home


