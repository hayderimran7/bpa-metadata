#!/bin/sh

: ${PROJECT_NAME:='bpametadata'}
#readonly PROGNAME=$(basename $0)
. ./lib.sh

set -e

ACTION="$1"

#CMD_ENV="DJANGO_MAILGUN_API_KEY=${DJANGO_MAILGUN_API_KEY} DJANGO_MAILGUN_SERVER_NAME=${DJANGO_MAILGUN_SERVER_NAME} PYTHONUNBUFFERED=1"
#DOCKER_BUILD_OPTS=''
#DOCKER_ROUTE=''
#DOCKER_RUN_OPTS='-e PIP_INDEX_URL -e PIP_TRUSTED_HOST'
#DOCKER_COMPOSE_BUILD_OPTS=''
#
#usage() {
#    cat << EOF
#  Wrapper script to call common tools while developing ${PROJECT_NAME}
#
#  Environment:
#  Pull during docker build   DOCKER_PULL                 ${DOCKER_PULL}
#  No cache during build      DOCKER_NO_CACHE             ${DOCKER_NO_CACHE}
#  Use proxy during builds    DOCKER_BUILD_PROXY          ${DOCKER_BUILD_PROXY}
#  Push/pull from docker hub  DOCKER_USE_HUB              ${DOCKER_USE_HUB}
#  Release docker image       DOCKER_IMAGE                ${DOCKER_IMAGE}
#  Use a http proxy           SET_HTTP_PROXY              ${SET_HTTP_PROXY}
#  Use a pip proxy            SET_PIP_PROXY               ${SET_PIP_PROXY}
#  Use mailgun to send mail   DJANGO_MAILGUN_API_KEY      ${DJANGO_MAILGUN_API_KEY}
#  Use mailgun to send mail   DJANGO_MAILGUN_SERVER_NAME  ${DJANGO_MAILGUN_SERVER_NAME}
#
#  Usage: ${PROGNAME} options
#
#  OPTIONS:
#  dev            Pull up stack and start developing
#  dev_build      Build dev stack images
#  prod_build     Build production image from current tag or branch
#  baseimage      Build base image
#  buildimage     Build build image
#  devimage       Build dev image
#  releaseimage   Build release image
#  releasetarball Produce release tarball artifact
#  shell          Create and shell into a new web image, used for db checking with Django env available
#  superuser      Create Django superuser
#  runscript      Run one of the available scripts
#  checksecure    Run security check
#  up             Spins up docker development stack
#  rm             Remove all containers
#  pythonlint     Run python lint
#  unit_tests     Run unit tests
#  usage          Print this usage
#  help           Print this usage
#
#
#  Example, start dev with no proxy and rebuild everything:
#  SET_PIP_PROXY=0 SET_HTTP_PROXY=0 ${PROGNAME} dev_rebuild
#  ${PROGNAME} dev_build
#  ${PROGNAME} dev
#EOF
#    exit 1
#}


echo ''
info "$0 $@"
make_virtualenv
docker_options

#display_env

case $ACTION in
    pythonlint)
        python_lint
        ;;
    jslint)
        js_lint
        ;;
    rm)
        rm_images
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
    ingest_all)
        docker exec -it ${PROJECT_NAME}_runserver_1 /app/docker-entrypoint.sh ingest_all
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
