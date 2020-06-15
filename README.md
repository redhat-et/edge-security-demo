# Edge, AI & Security Demo

This repository contains the files needed to create a demonstration of an
OpenShift Cluster running an AI / Edge workload, protected by Keylime.

To create the container images, use the following command line syntax:

```
docker build -t et-demo .  
container_id=$(mktemp)
docker run --detach --privileged -v /sys/fs/cgroup:/sys/fs/cgroup:ro et-demo > ${container_id}
docker exec -u 0 -it --tty "$(cat ${container_id})" /bin/bash    
```
