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
