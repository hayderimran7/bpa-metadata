# Bioplatforms Australia  Metadata Management

BPA Metadata is a web portal into Bioplatforms Australia's genomics sequencing data 
archive. It aims to aggregate all relevant meta and sequence data into a coherent data 
navigation system.

# Development
Ensure a late version of both docker and docker-compose are available in your environment.

bpa-metada is available as a fully contained Dockerized stack. The dockerised stack are used for both production
and development. Appropiate configuration files are available depending on usage.

Note that for data ingestion to work you need passwords to the hosted data, these are available from BPA on request.
Set passwords in your environment, these will be passed to the container.

## Quick Setup

* [Install docker and compose](https://docs.docker.com/compose/install/)
* git clone https://github.com/muccg/bpa-metadata.git
* `./develop.sh dev_build`

`develop.sh dev` will spin up the stack. See `./develop.sh usage` for some utility methods, which typically are simple 
wrappers arround docker and docker-compose.

docker-compose will fire up the stack like below:
```
docker ps -f name="bpam*"

IMAGE                       PORTS                                                                          NAMES
muccg/nginx-uwsgi:1.10      0.0.0.0:8080->80/tcp, 0.0.0.0:8443->443/tcp                                    bpametadata_nginx_1
mdillon/postgis:9.5         0.0.0.0:32944->5432/tcp                                                        bpametadata_db_1
memcached:1.4               11211/tcp                                                                      bpametadata_cache_1
muccg/bpametadata-dev       0.0.0.0:9000-9001->9000-9001/tcp, 8000/tcp, 0.0.0.0:9100-9101->9100-9101/tcp   bpametadata_uwsgi_1
muccg/bpametadata-dev       9000-9001/tcp, 0.0.0.0:8000->8000/tcp, 9100-9101/tcp                           bpametadata_runserver_1
```

Setup mirror config
```
docker exec -it bpametadata_runserver_1 /app/docker-entrypoint.sh django-admin set_mirrors
```

To execute the ingestion scripts run `docker exec -it bpametadata_runserver_1 /app/docker-entrypoint.sh django-admin`, be sure
to have the relevant variables below available in the environment. 

```
DJANGO_MAILGUN_API_KEY
BASE_REQUEST_LIST
BPA_MELANOMA_DOWNLOADS_PASSWORD
BPA_BASE_DOWNLOADS_PASSWORD
BPA_USERS_DOWNLOADS_PASSWORD
BPA_GBR_DOWNLOADS_PASSWORD
BPA_SEPSIS_DOWNLOADS_PASSWORD
```



```bash
./develop.sh

  [ INFO ] ./develop.sh 
  [  OK  ] Docker ip 172.17.0.1
  [ INFO ] http proxy
  [  OK  ] Proxy http://172.17.0.1:3128
  [  OK  ] HTTP proxy http://172.17.0.1:3128
  [ INFO ] pip proxy
  [  OK  ] Pip index url http://172.17.0.1:3141/root/pypi/+simple/
  [ INFO ] git tag
  [ INFO ] Ignoring tags, not on master branch
  [  OK  ] git tag: next_release

Environment:
 Pull during build              DOCKER_PULL                 1 
 No cache during build          DOCKER_NO_CACHE             0 
 Use proxy during builds        DOCKER_BUILD_PROXY          --build-arg http_proxy
 Push/pull from docker hub      DOCKER_USE_HUB              0
 Release docker image           DOCKER_IMAGE                muccg/bpametadata
 Use a http proxy               SET_HTTP_PROXY              1
 Use a pip proxy                SET_PIP_PROXY               1

Usage:
 ./develop.sh (baseimage|buildimage|devimage|releasetarball|prodimage)
 ./develop.sh (dev|dev_build)
 ./develop.sh (start_prod|prod_build)
 ./develop.sh (runtests|lettuce|selenium)
 ./develop.sh (start_test_stack|start_seleniumhub|start_seleniumtests|start_prodseleniumtests)
 ./develop.sh (pythonlint|jslint)
 ./develop.sh (ci_docker_staging|docker_staging_lettuce)
 ./develop.sh (ci_docker_login)

Example, start dev with no proxy and rebuild everything:
SET_PIP_PROXY=0 SET_HTTP_PROXY=0 ./develop.sh dev_rebuild


```

## Sites
- *Production* https://downloads.bioplatforms.com

## Licence
BPA Metadata is released under the GNU Affero GPL. See source for a licence copy.

## Contributing
* Fork next_release branch
* Make changes on a feature branch
* Submit pull request

## CCG Internal documentation

https://ccgmurdoch.atlassian.net/wiki/display/BM/BPA+Metadata+Home

[1]: Be aware that all CDN supported content still needs to be fetched from the internet. 
