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
* `./develop.sh dev`
* `./develop.sh ingest_all`

`develop.sh dev` will spin up the stack. See `./develop.sh usage` for some utility methods, which typically are simple 
wrappers arround docker:

```bash
./develop.sh                         next_release 

  [ INFO ] ./develop.sh 
  [ INFO ] make virtualenv
  [  OK  ] docker-compose version 1.5.2, build 7240ff3
  [  OK  ] Docker ip 172.17.0.1
  [ INFO ] http proxy
  [  OK  ] Proxy http://172.17.0.1:3128
  [ INFO ] pip proxy
  [  OK  ] Pip index url http://172.17.0.1:3141/root/pypi/+simple/
  [ INFO ] Environment set as:
  [ INFO ] DOCKER_PULL                 1
  [ INFO ] DOCKER_NO_CACHE             0
  [ INFO ] DOCKER_BUILD_PROXY          --build-arg http_proxy
  [ INFO ] DOCKER_USE_HUB              0
  [ INFO ] DOCKER_IMAGE                muccg/bpametadata
  [ INFO ] SET_HTTP_PROXY              1
  [ INFO ] DJANGO_MAILGUN_API_KEY      NOTSET
  [ INFO ] DJANGO_MAILGUN_SERVER_NAME  mg.ccgapps.com.au
  Wrapper script to call common tools while developing bpametadata

  Environment:
  Pull during docker build   DOCKER_PULL                 1
  No cache during build      DOCKER_NO_CACHE             0
  Use proxy during builds    DOCKER_BUILD_PROXY          --build-arg http_proxy
  Push/pull from docker hub  DOCKER_USE_HUB              0
  Release docker image       DOCKER_IMAGE                muccg/bpametadata
  Use a http proxy           SET_HTTP_PROXY              1
  Use a pip proxy            SET_PIP_PROXY               1
  Use mailgun to send mail   DJANGO_MAILGUN_API_KEY      NOTSET
  Use mailgun to send mail   DJANGO_MAILGUN_SERVER_NAME  ccgmg.com.au

  Usage: develop.sh options

  OPTIONS:
  dev            Pull up stack and start developing
  dev_build      Build dev stack images
  prod_build     Build production image from current tag or branch
  baseimage      Build base image
  buildimage     Build build image
  devimage       Build dev image
  releaseimage   Build release image
  releasetarball Produce release tarball artifact
  shell          Create and shell into a new web image, used for db checking with Django env available
  superuser      Create Django superuser
  runscript      Run one of the available scripts
  checksecure    Run security check
  up             Spins up docker development stack
  rm             Remove all containers
  pythonlint     Run python lint
  unit_tests     Run unit tests
  usage          Print this usage
  help           Print this usage


  Example, start dev with no proxy and rebuild everything:
  SET_PIP_PROXY=0 SET_HTTP_PROXY=0 develop.sh dev_rebuild
  develop.sh dev_build
  develop.sh dev

```

## Sites
- *Production* https://downloads.bioplatforms.com/metadata/
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
