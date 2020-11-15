## Generate docker image
docker build -t fast_api .
## Generate docker container
docker run -d -p 5001:5001 -v {local_route}:/app --name {container_name} {image}
docker run -d -p 5001:5001 -e LOGLEVEL=${LOGLEVEL} -v /Users/angel.rios/git_/FastApi/:/app --name api fast_api