## Generate docker image
    docker build -t ai .
## Generate docker container
    docker run -d -p 5001:5001 -e AccessKey={AccessKey} -e LOGLEVEL=${LOGLEVEL} -e dbhostname={dbhostname} -e dbuid={dbuid} -e dbpwd={dbpwd} -e dbname={dbname} -v {local_route}:/app --name {container_name} {image}

    docker run -d -p 8087:5001 -e AccessKey=key -e LOGLEVEL=DEBUG -e dbhostname=187.188.44.173 -e dbuid=tostatronic -e dbpwd=Admin1995 -e port=33060 -e dbname=salespoint --runtime=nvidia -v /Users/angel.rios/git_/FastApi/:/app --name api ai