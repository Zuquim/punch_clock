#!/usr/bin/env bash

DOCKER_IMAGE="punch-clock"
DOCKER_CONTAINER=$DOCKER_IMAGE

function print_syntax_exit {
    printf "\nSyntax: $0 <build|rebuild|run|test|update|full-update>\n"
    exit 1
}

function build_image {
    echo "Building API Docker base image from scratch..."
    docker build --rm --pull --no-cache -t $DOCKER_IMAGE:latest .
    echo "Docker image ($DOCKER_IMAGE) built!"
    exit 0
}

function rebuild_image {
    echo "Re-Building (on top of base image) API Docker image..."
    docker build --rm --no-cache -t $DOCKER_IMAGE:latest -f Dockerfile-fast .
    echo "Docker image ($DOCKER_IMAGE) built!"
    exit 0
}

function run_tests {
    echo "Running API tests..."
    docker run -it --rm -p 8001:80 \
           -v $PWD/log:/var/log/api \
           -e ENV=testing \
           -e TESTING=1 \
           -e FLASK_ENV=testing \
           $DOCKER_IMAGE \
           py.test -v
    echo "Done testing!"
    exit 0
}

function run_api {
    echo "Running API..."
    docker run -d --name $DOCKER_CONTAINER -p 8000:80 \
           -v $PWD/log:/var/log/api \
           $DOCKER_IMAGE
    echo "Done!"
    exit 0
}

if [[ $# != 1 ]]
then
  print_syntax_exit
elif [[ $1 == "build" ]]
then
  build_image
elif [[ $1 == "rebuild" ]]
then
  rebuild_image
elif [[ $1 == "run" ]]
then
  if [[ $(docker images | grep $DOCKER_IMAGE) != "" ]]
  then
    run_api
  else
    echo "PunchClock Docker image does not exist!"
    echo "Building it from scratch in 10s... [hit <Ctrl>+<C> to cancel]"
    sleep 10 && build_image && run_api
  fi
elif [[ $1 == "test" ]]
then
  run_tests
elif [[ $1 == "update" ]]
then
  rebuild_image
  echo "Stopping and removing current version..."
  docker stop $DOCKER_CONTAINER; docker rm $DOCKER_CONTAINER
  echo "Running new version..."
  run_api
elif [[ $1 == "full-update" ]]
then
  build_image
  echo "Stopping and removing current version..."
  docker stop $DOCKER_CONTAINER; docker rm $DOCKER_CONTAINER
  echo "Running new version..."
  run_api
else
  print_syntax_exit
fi
