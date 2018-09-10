MODULE_NAME=qfe_cache

docker build -t $MODULE_NAME -f ./deploy/cache.Dockerfile $PWD
docker run --rm  --name $MODULE_NAME \
  --network $DOCKER_NETWORK \
  -e REDIS_HOST=$REDIS_HOST \
  -e REDIS_PORT=$REDIS_PORT \
  -p $REDIS_PORT:$REDIS_PORT \
  $MODULE_NAME