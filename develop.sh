#! /bin/bash

set -o nounset
set -o errexit

readonly PROJECT_NAME='bpametadata'
readonly PROGNAME=$(basename $0)

. ./lib.sh


CMD_ENV="DJANGO_MAILGUN_API_KEY=${DJANGO_MAILGUN_API_KEY} DJANGO_MAILGUN_SERVER_NAME=${DJANGO_MAILGUN_SERVER_NAME} PYTHONUNBUFFERED=1"
DOCKER_BUILD_OPTS=''
DOCKER_ROUTE=''
DOCKER_RUN_OPTS='-e PIP_INDEX_URL -e PIP_TRUSTED_HOST'
DOCKER_COMPOSE_BUILD_OPTS=''


create_release_image() {
  info 'create release image'
  # assumes that base image and release tarball have been created
  _docker_release_build Dockerfile-release ${DOCKER_IMAGE}
  success "$(docker images | grep ${DOCKER_IMAGE} | grep ${gittag}-${DATE} | sed 's/  */ /g')"
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

# lint using flake8
python_lint() {
  info "python lint"
  pip install 'flake8>=2.0,<2.1'
  flake8 bpam --count
  success "python lint"
}

echo ''
info "$0 $@"
make_virtualenv

docker_options
display_env

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
    dev_build)
        create_base_image
        create_build_image
        create_dev_image
        ;;
    dev_full)
        start_dev_full
        ;;
    releasetarball)
        create_release_tarball
        ;;
    start_prod)
        start_prod
        ;;
    prod_build)
        create_base_image
        create_build_image
        create_release_tarball
        create_prod_image
        ;;
    baseimage)
        create_base_image
        ;;
    buildimage)
        create_build_image
        ;;
    prodimage)
        create_prod_image
        ;;
    devimage)
        create_dev_image
        ;;
    ci_dockerbuild)
        _ci_ssh_agent
        _ci_docker_login
        create_base_image
        create_build_image
        create_release_tarball
        create_prod_image
        ;;
    runtests)
        create_base_image
        create_build_image
        create_dev_image
        run_unit_tests
        ;;
    start_test_stack)
        start_test_stack
        ;;
    start_seleniumhub)
        start_seleniumhub
        ;;
    start_seleniumtests)
        start_seleniumtests
        ;;
    start_prodseleniumtests)
        start_prodseleniumtests
        ;;
    ci_docker_staging)
        _ci_ssh_agent
        ci_docker_staging
        ;;
    docker_staging_lettuce)
        docker_staging_lettuce
        ;;
    lettuce)
        create_base_image
        create_build_image
        create_dev_image
        lettuce
        ;;
    selenium)
        create_base_image
        create_build_image
        create_dev_image
        selenium
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
