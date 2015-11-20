#!/bin/bash
# Script to control ${PROJECT_NAME} in dev and test

TOPDIR=$(cd $(dirname $0); pwd)

ACTION=$1

PROJECT_NAME='bpametadata'
VIRTUALENV="${HOME}/virt_${PROJECT_NAME}"

######### Logging ##########
COLOR_NORMAL=$(tput sgr0)
COLOR_RED=$(tput setaf 1)
COLOR_YELLOW=$(tput setaf 3)
COLOR_GREEN=$(tput setaf 2)

set -e

log_error() {
    echo ${COLOR_RED}ERROR: $* ${COLOR_NORMAL}
}

log_warning() {
    echo ${COLOR_YELLOW}WARNING: $* ${COLOR_NORMAL}
}

log_success() {
    echo ${COLOR_GREEN}SUCCESS: $* ${COLOR_NORMAL}
}

log_info() {
    echo INFO: $*
}

# no news is good news
log() {
    ERROR_CODE=$0
    MESSAGE=$1

    if [ ${ERROR_CODE} != 0 ]
    then
        log_warning ${MESSAGE}
    else
        log_success ${MESSAGE}
    fi
 }

activate_virtualenv() {
   if [ ! -d ${VIRTUALENV} ]
   then
        log_warning "There is no ${VIRTUALENV} here, making it."
        virtualenv ${VIRTUALENV}
        . ${VIRTUALENV}/bin/activate
        pip install docker-compose
        pip install 'flake8>=2.0,<2.1'
   else
      source ${VIRTUALENV}/bin/activate
   fi
}

# ssh setup, make sure our ccg commands can run in an automated environment
ci_ssh_agent() {
    ssh-agent > /tmp/agent.env.sh
    source /tmp/agent.env.sh
    ssh-add ~/.ssh/ccg-syd-staging-2014.pem
}


pythonlint() {
    activate_virtualenv
    # find . -type d -name ".ropeproject" -exec rm -fr {} \;
    ${VIRTUALENV}/bin/flake8 bpam --exclude=migrations,.ropeproject --ignore=E501,E303 --count
}


unit_tests() {
    activate_virtualenv

    mkdir -p data/tests
    chmod o+rwx data/tests
    docker-compose --project-name ${PROJECT_NAME} -f fig-test.yml up
}

up() {
    activate_virtualenv
    mkdir -p data/dev
    chmod o+rwx data/dev

    docker-compose --project-name ${PROJECT_NAME} up
}


selenium() {
    activate_virtualenv
    mkdir -p data/selenium
    chmod o+rwx data/selenium

    docker-compose --project-name ${PROJECT_NAME} -f fig-selenium.yml up
}


build() {
   activate_virtualenv
   docker-compose --project-name ${PROJECT_NAME} build
}

rm_containers() {
   docker-compose --project-name ${PROJECT_NAME} rm
}

entrypoint() {
   ENTRYPOINT=${1:-bash}
   log_info "Entrypoint ${ENTRYPOINT}"
   docker exec -it ${PROJECT_NAME}_web_1 ${ENTRYPOINT} $2
}


mint_docker_image() {
   activate_virtualenv

   image="muccg/${PROJECT_NAME}"
   gitbranch=$(git rev-parse --abbrev-ref HEAD 2> /dev/null)
   gittag=$(git describe --abbrev=0 --tags 2> /dev/null)
   template="$(cat docker/Dockerfile.in)"

   # avoid building naming images from branches 
   if [ $gitbranch != "master" ]
   then
      gittag=$gitbranch
   fi

   # log the Dockerfile
   echo "########################################"
   sed -e "s/GITTAG/${gittag}/g" docker/Dockerfile.in
   echo "########################################"

   # attempt to warm up docker cache
   docker pull ${image} || true

   sed -e "s/GITTAG/${gittag}/g" docker/Dockerfile.in | docker build --pull=true -t ${image} -
   sed -e "s/GITTAG/${gittag}/g" docker/Dockerfile.in | docker build -t ${image}:${DATE} -

   if [ -z ${gittag+x} ]
   then
      echo "No git tag set"
   else
      echo "Git tag ${gittag}"
      sed -e "s/GITTAG/${gittag}/g" docker/Dockerfile.in | docker build -t ${image}:${gittag} -
      docker push ${image}:${gittag}
   fi

   docker push ${image}
   docker push ${image}:${DATE}
}


usage() {
   echo 'Usage ./develop.sh (build|shell|unit_tests|selenium|superuser|up|rm|runscript|ingest_all)'

   echo '                   build        Build all images'
   echo '                   mint         Mint and push new docker images from current checked out tag'
   echo '                   shell        Create and shell into a new web image, used for db checking with Django env available'
   echo '                   superuser    Create Django superuser'
   echo '                   runscript    Run one of the available scripts' 
   echo '                   ingest_all   Ingest metadata'
   echo '                   checksecure  Run security check'
   echo '                   up           Spins up docker image stack'
   echo '                   rm           Remove all containers'
   echo '                   pythonlint   Run python lint'
   echo '                   unit_tests   Run unit tests'
   echo '                   selenium     Run selenium tests'
   echo '                   usage'
}

case ${ACTION} in
pythonlint)
    pythonlint
    ;;
ci_staging)
    ci_ssh_agent
    ci_staging
    ;;
start)
    up
    ;;
build)
    build
    ;;
mint)
   mint_docker_image
    ;;
rm)
    rm_containers
    ;;
clean)
    clean
    ;;
up)
    up
    ;;
shell)
    docker exec -it ${PROJECT_NAME}_web_1 /bin/bash
    ;;
superuser)
    docker exec -it ${PROJECT_NAME}_web_1 /app/docker-entrypoint.sh superuser
    ;;
ingest_all)
    docker exec -it ${PROJECT_NAME}_web_1 /app/docker-entrypoint.sh ingest_all
    ;;
runscript)
    docker exec -it ${PROJECT_NAME}_web_1 /app/docker-entrypoint.sh runscript $2
    ;;
nuclear)
    docker exec -it ${PROJECT_NAME}_web_1 /app/docker-entrypoint.sh nuclear
    ;;
ingest_gbr)
    docker exec -it ${PROJECT_NAME}_web_1 /app/docker-entrypoint.sh ingest_gbr
    ;;
unit_tests)
    unit_tests
    ;;
selenium)
    selenium
    ;;
checksecure)
    docker exec -it ${PROJECT_NAME}_web_1 /app/docker-entrypoint.sh checksecure
    ;;
*)
    usage
esac
