#! /bin/bash

set -o nounset
set -o errexit

readonly TOPDIR=$(cd $(dirname $0); pwd)
readonly PROGNAME=$(basename $0)
readonly PROGDIR=$(readlink -m $(dirname $0))
readonly ACTION=${1:-"usage"}
readonly DATE=$(date +%Y.%m.%d)
readonly PROJECT_NAME='bpametadata'
readonly VIRTUALENV="${TOPDIR}/virt_${PROJECT_NAME}"

: ${DOCKER_BUILD_PROXY:="--build-arg http_proxy"}
: ${DOCKER_USE_HUB:="0"}
: ${DOCKER_IMAGE:="muccg/${PROJECT_NAME}"}
: ${SET_HTTP_PROXY:="1"}
: ${SET_PIP_PROXY:="1"}
: ${DOCKER_NO_CACHE:="0"}
: ${DOCKER_PULL:="1"}

: ${DJANGO_MAILGUN_API_KEY:="NOTSET"}

CMD_ENV="DJANGO_MAILGUN_API_KEY=${DJANGO_MAILGUN_API_KEY} PYTHONUNBUFFERED=1"
DOCKER_BUILD_OPTS=''
DOCKER_ROUTE=''
DOCKER_RUN_OPTS='-e PIP_INDEX_URL -e PIP_TRUSTED_HOST'
DOCKER_COMPOSE_BUILD_OPTS=''

usage() {
  cat << EOF
  Wrapper script to call common tools while developing ${PROJECT_NAME}

  Environment:
  Pull during docker build   DOCKER_PULL                 ${DOCKER_PULL}
  No cache during build      DOCKER_NO_CACHE             ${DOCKER_NO_CACHE}
  Use proxy during builds    DOCKER_BUILD_PROXY          ${DOCKER_BUILD_PROXY}
  Push/pull from docker hub  DOCKER_USE_HUB              ${DOCKER_USE_HUB}
  Release docker image       DOCKER_IMAGE                ${DOCKER_IMAGE}
  Use a http proxy           SET_HTTP_PROXY              ${SET_HTTP_PROXY}
  Use a pip proxy            SET_PIP_PROXY               ${SET_PIP_PROXY}
  Use mailgun to send mail   DJANGO_MAILGUN_API_KEY      ${DJANGO_MAILGUN_API_KEY}

  Usage: ${PROGNAME} options

  OPTIONS:
  dev            Pull up stack and start developing
  dev_rebuild    Rebuild dev stack images
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
  SET_PIP_PROXY=0 SET_HTTP_PROXY=0 ${PROGNAME} dev_rebuild
  ${PROGNAME} dev_rebuild
  ${PROGNAME} dev
EOF
  exit 1
}

# log
info () {
  printf "\r  [ \033[00;34mINFO\033[0m ] $1\n"
}

success () {
  printf "\r\033[2K  [ \033[00;32m OK \033[0m ] $1\n"
}


fail () {
  printf "\r\033[2K  [\033[0;31mFAIL\033[0m] $1\n"
  echo ''
  exit 1
}


_docker_options() {
  DOCKER_ROUTE=$(ip -4 addr show docker0 | grep -Po 'inet \K[\d.]+')
  success "Docker ip ${DOCKER_ROUTE}"

  _http_proxy
  _pip_proxy

  if [ ${DOCKER_PULL} = "1" ]; then
    DOCKER_BUILD_PULL="--pull=true"
    DOCKER_COMPOSE_BUILD_PULL="--pull"
  else
    DOCKER_BUILD_PULL="--pull=false"
    DOCKER_COMPOSE_BUILD_PULL=""
  fi

  if [ ${DOCKER_NO_CACHE} = "1" ]; then
    DOCKER_BUILD_NOCACHE="--no-cache=true"
    DOCKER_COMPOSE_BUILD_NOCACHE="--no-cache"
  else
    DOCKER_BUILD_NOCACHE="--no-cache=false"
    DOCKER_COMPOSE_BUILD_NOCACHE=""
  fi

  DOCKER_BUILD_OPTS="${DOCKER_BUILD_OPTS} ${DOCKER_BUILD_NOCACHE} ${DOCKER_BUILD_PROXY} ${DOCKER_BUILD_PULL} ${DOCKER_BUILD_PIP_PROXY}"

  # compose does not expose all docker functionality, so we can't use compose to build in all cases
  DOCKER_COMPOSE_BUILD_OPTS="${DOCKER_COMPOSE_BUILD_OPTS} ${DOCKER_COMPOSE_BUILD_NOCACHE} ${DOCKER_COMPOSE_BUILD_PULL}"

  # environemnt used by subshells
  CMD_ENV="export ${CMD_ENV}"
}


_display_env() {
  info "Environment set as:"
  info "DOCKER_PULL            ${DOCKER_PULL}"
  info "DOCKER_NO_CACHE        ${DOCKER_NO_CACHE}"
  info "DOCKER_BUILD_PROXY     ${DOCKER_BUILD_PROXY}"
  info "DOCKER_USE_HUB         ${DOCKER_USE_HUB}"
  info "DOCKER_IMAGE           ${DOCKER_IMAGE}"
  info "SET_HTTP_PROXY         ${SET_HTTP_PROXY}"
  info "DJANGO_MAILGUN_API_KEY ${DJANGO_MAILGUN_API_KEY}"
}

_http_proxy() {
  info 'http proxy'

  if [ ${SET_HTTP_PROXY} = "1" ]; then
    local http_proxy="http://${DOCKER_ROUTE}:3128"
    CMD_ENV="${CMD_ENV} http_proxy=http://${DOCKER_ROUTE}:3128"
    success "Proxy $http_proxy"
  else
    info 'Not setting http_proxy'
  fi
}

_pip_proxy() {
  info 'pip proxy'

  # pip defaults
  PIP_INDEX_URL='https://pypi.python.org/simple'
  PIP_TRUSTED_HOST='127.0.0.1'

  if [ ${SET_PIP_PROXY} = "1" ]; then
    # use a local devpi install
    PIP_INDEX_URL="http://${DOCKER_ROUTE}:3141/root/pypi/+simple/"
    PIP_TRUSTED_HOST="${DOCKER_ROUTE}"
  fi

  CMD_ENV="${CMD_ENV} NO_PROXY=${DOCKER_ROUTE} no_proxy=${DOCKER_ROUTE} PIP_INDEX_URL=${PIP_INDEX_URL} PIP_TRUSTED_HOST=${PIP_TRUSTED_HOST}"
  DOCKER_BUILD_PIP_PROXY='--build-arg ARG_PIP_INDEX_URL='${PIP_INDEX_URL}' --build-arg ARG_PIP_TRUSTED_HOST='${PIP_TRUSTED_HOST}''

  success "Pip index url ${PIP_INDEX_URL}"
}

# figure out what branch/tag we are on, write out .version file
_github_revision() {
  info 'git revision'

  gittag=$(git describe --abbrev=0 --tags 2> /dev/null) 
  gitbranch=$(git rev-parse --abbrev-ref HEAD 2> /dev/null)

  info '$gittag'

  # only use tags when on master (release) branch
  if [ $gitbranch != "master" ]; then
    info 'Ignoring tags, not on master branch'
    gittag=$gitbranch
  fi

  # if no git tag, then use branch name
  if [ -z ${gittag+x} ]; then
    info 'No git tag set, using branch name'
    gittag=$gitbranch
  fi

  # create .version file for invalidating cache in Dockerfile
  # we hit remote as the Dockerfile clones remote
  # git ls-remote https://github.com/muccg/${PROJECT_NAME}.git ${gittag} > .version
  git rev-parse --short HEAD > .version

  success "$(cat .version)"
  success "git tag: ${gittag}"
}


create_dev_image() {
  info 'create dev image'
  set -x
  # don't try and pull the base image
  docker-compose --project-name ${PROJECT_NAME} build ${DOCKER_COMPOSE_BUILD_NOCACHE}
  set +x
}


create_release_image() {
  info 'create release image'
  # assumes that base image and release tarball have been created
  _docker_release_build Dockerfile-release ${DOCKER_IMAGE}
  success "$(docker images | grep ${DOCKER_IMAGE} | grep ${gittag}-${DATE} | sed 's/  */ /g')"
}


create_build_image() {
  info 'create build image'
  _github_revision

  set -x
  # don't try and pull the build image
  (
  ${CMD_ENV}
  docker build ${DOCKER_BUILD_NOCACHE} ${DOCKER_BUILD_PROXY} --build-arg ARG_GIT_TAG=${gittag} -t muccg/${PROJECT_NAME}-build -f Dockerfile-build .
  )
  set +x
  success "$(docker images | grep muccg/${PROJECT_NAME}-build | sed 's/  */ /g')"
}


create_base_image() {
  info 'create base image'
  set -x
  (
  ${CMD_ENV}; docker build ${DOCKER_BUILD_NOCACHE} ${DOCKER_BUILD_PROXY} ${DOCKER_BUILD_PULL} -t muccg/${PROJECT_NAME}-base -f Dockerfile-base .)
  set +x
  success "$(docker images | grep muccg/${PROJECT_NAME}-base | sed 's/  */ /g')"
}

create_release_tarball() {
  info 'create release tarball'
  mkdir -p build
  chmod o+rwx build

  set -x
  local volume=$(readlink -f ./build/)
  (
  ${CMD_ENV}
  docker run ${DOCKER_RUN_OPTS} --rm -v ${volume}:/data muccg/${PROJECT_NAME}-build tarball
  )
  set +x
  success "$(ls -lh build/*)"
}


start_release() {
  info 'start release'
  mkdir -p data/release
  chmod o+rwx data/release

  set -x
  GIT_TAG=${gittag} docker-compose --project-name ${PROJECT_NAME} -f docker-compose-release.yml rm --force
  GIT_TAG=${gittag} docker-compose --project-name ${PROJECT_NAME} -f docker-compose-release.yml up
  set +x
}


start_dev() {
  info 'start dev'
  mkdir -p data/dev
  chmod o+rwx data/dev
  set -x
  ( ${CMD_ENV}; docker-compose --project-name ${PROJECT_NAME} up )
  set +x
}

rm_images() {
  info 'rm images'
  set -x
  ( ${CMD_ENV}; docker-compose --project-name ${PROJECT_NAME} rm )
  set +x
}

_ci_docker_login() {
  info 'Docker login'

  if [ -z ${bamboo_DOCKER_EMAIL+x} ]; then
    fail 'bamboo_DOCKER_EMAIL not set'
  fi
  if [ -z ${bamboo_DOCKER_USERNAME+x} ]; then
    fail 'bamboo_DOCKER_USERNAME not set'
  fi
  if [ -z ${bamboo_DOCKER_PASSWORD+x} ]; then
    fail 'bamboo_DOCKER_PASSWORD not set'
  fi

  docker login  -e "${bamboo_DOCKER_EMAIL}" -u ${bamboo_DOCKER_USERNAME} --password="${bamboo_DOCKER_PASSWORD}"
  success "Docker login"
}


_docker_release_build() {
  info 'docker release build'

  local dockerfile='Dockerfile-release'
  local dockerimage=${DOCKER_IMAGE}

  _github_revision

  # attempt to warm up docker cache
  if [ ${DOCKER_USE_HUB} = "1" ]; then
    docker pull ${dockerimage}:${gittag} || true
  fi

  for tag in "${dockerimage}:${gittag}" "${dockerimage}:${gittag}-${DATE}"; do
    info "Building ${PROJECT_NAME} ${tag}"
    set -x
    # don't try and pull the base image
    (
    ${CMD_ENV}
    docker build ${DOCKER_BUILD_PROXY} ${DOCKER_BUILD_NOCACHE} --build-arg ARG_GIT_TAG=${gittag} -t ${tag} -f ${dockerfile} .
    )
    success "built ${tag}"

    if [ ${DOCKER_USE_HUB} = "1" ]; then
      docker push ${tag}
      success "pushed ${tag}"
    fi
  done

  rm -f .version || true
  success 'docker release build'
}


# docker build and push in CI
ci_dockerbuild() {
  info 'ci docker build'
  _ci_docker_login
  create_base_image
  create_build_image
  create_release_tarball
  _docker_release_build
  success 'ci docker build'
}

# lint using flake8
python_lint() {
  info "python lint"
  pip install 'flake8>=2.0,<2.1'
  flake8 bpam --count
  success "python lint"
}


make_virtualenv() {
  info "make virtualenv"
  # check requirements
  if ! which virtualenv > /dev/null; then
    fail "virtualenv is required by develop.sh but it isn't installed."
  fi
  if [ ! -e ${VIRTUALENV} ]; then
    virtualenv ${VIRTUALENV}
  fi
  set +o nounset
  . ${VIRTUALENV}/bin/activate
  set -o nounset
  if ! which docker-compose > /dev/null; then
    pip install 'docker-compose<1.6' --upgrade || true
  fi
  success "$(docker-compose --version)"
}


echo ''
info "$0 $@"
make_virtualenv

_docker_options
_display_env

case $ACTION in
  pythonlint)
    python_lint
    ;;
  jslint)
    js_lint
    ;;
  dev)
    start_dev
    ;;
  rm)
    rm_images 
    ;;
  dev_rebuild)
    create_base_image
    create_build_image
    create_dev_image
    start_dev
    ;;
  dev_full)
    start_dev_full
    ;;
  releasetarball)
    create_release_tarball
    ;;
  start_release)
    start_release
    ;;
  start_release_rebuild)
    create_base_image
    create_build_image
    create_release_tarball
    create_release_image
    start_release
    ;;
  baseimage)
    create_base_image
    ;;
  buildimage)
    create_build_image
    ;;
  releaseimage)
    create_release_image
    ;;
  devimage)
    create_dev_image
    ;;
  ci_dockerbuild)
    ci_dockerbuild
    ;;
  rpm_publish)
    _ci_ssh_agent
    rpm_publish
    ;;
  runtests)
    run_unit_tests
    ;;
  ci_docker_staging)
    _ci_ssh_agent
    ci_docker_staging
    ;;
  docker_staging_lettuce)
    docker_staging_lettuce
    ;;
  lettuce)
    lettuce
    ;;
  set_mirrors)
      docker exec -it ${PROJECT_NAME}_runserver_1 /app/docker-entrypoint.sh admin set_mirrors
      ;;
  shell)
    docker exec -it ${PROJECT_NAME}_runserver_1 /bin/bash
    ;;
  admin)
    docker exec -it ${PROJECT_NAME}_runserver_1 /app/docker-entrypoint.sh admin $2
    ;;
  superuser)
    docker exec -it ${PROJECT_NAME}_runserver_1 /app/docker-entrypoint.sh superuser
    ;;
  runscript)
    docker exec -it ${PROJECT_NAME}_runserver_1 /app/docker-entrypoint.sh runscript $2
    ;;
  nuclear)
    docker exec -it ${PROJECT_NAME}_runserver_1 /app/docker-entrypoint.sh nuclear
    ;;
  checksecure)
    docker exec -it ${PROJECT_NAME}_runserver_1 /app/docker-entrypoint.sh checksecure
    ;;
  help)
    usage 
    ;;
  *)
    usage
    ;;
esac
