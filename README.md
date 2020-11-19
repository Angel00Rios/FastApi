## Generate docker image
    docker build -t fast_api .
## Generate docker container
    docker run -d -p 5001:5001 -e AccessKey={AccessKey} -e LOGLEVEL=${LOGLEVEL} -e dbhostname={dbhostname} -e dbuid={dbuid} -e dbpwd={dbpwd} -e dbname={dbname} -v {local_route}:/app --name {container_name} {image}