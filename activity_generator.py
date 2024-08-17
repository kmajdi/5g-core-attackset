import pandas as pd
import json
import numpy as np
from random import randrange
from datetime import timedelta, datetime
import asyncio
from get_attack_from_name import get_attack
import uuid

def random_date(start, end):
    """
    This function will return a random datetime between two datetime
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)

async def run_attack(attack):
    """
    This function runs an attack and finalizes it in an asynchronus manner
    """
    attack.execute()
    attack.finalize()    

class ActivityGenerator:
    """
    Activity Generator Module of the 5GProvGen framework - to be called and used by the Orchestrator
    
    Parameters: [Parameters are mainly controlled through the config.json configuration file explained below]
    
    - Instantiation Parameters: 
        - manual: Boolean
            - False would lead to random generation of attacks with random types among the included attack types and randomly scheduled from start time to end time
            - True would assume that attacks are already written to attack_todo.csv and reads the attack scheduling and types from there.

    - Configuration: [config.json]
        - time_start: The starting time for the framework
        - time_end: String formatted as %Y-%m-%d %H:%M:%S - The ending time for the framework
        - attack_count: (listof String) - The total number of attacks generated within start time to end time
        - attack_type: The types of attacks to be selected from (randomly)
    """
    
    def __init__(self, manual=False):
        # Constructor:
        # Loading of configurations and collections of parameters
        config_file = open("config.json","r")
        config = json.load(config_file)

        self.time_start = datetime.strptime(config["time_start"], '%Y-%m-%d %H:%M:%S')
        self.time_end = datetime.strptime(config["time_end"], '%Y-%m-%d %H:%M:%S')
        self.attack_type = config["attack_type"]
        self.attack_count = config["attack_count"]
        self.manual = manual

        self.attacks_in_progress = []
        self.attacks_completed = []

        self.attack_objects = {}
        self.start()

    def start(self):
        # Start function:
        # Not directly called
        # Used through contructor only
        if self.manual:
            self.attack_list = pd.read_csv("attack_list.csv")
        else:
            dates = [random_date(self.time_start, self.time_end) for count in range(self.attack_count)]
            attack_types = np.random.choice(self.attack_type, size = self.attack_count, replace = True)
            attack_ids = [str(uuid.uuid4()) for h in range(self.attack_count)]
            self.attack_list = pd.DataFrame({"id": attack_ids, "time": dates, "type": attack_types})
            self.attack_list.to_csv("attack_list.csv")
        
        self.attack_list["time"] = pd.to_datetime(self.attack_list["time"])

    def update(self):
        # Update function:
        # To be called once in each iteration of the orchestrator
        #   - Log end for attacks that have already been started
        #   - Start new attacks once their time has come and log for their start
        end_progress = []
        for attack_id in self.attacks_in_progress:
            if attack_objects[attack_id].time_end:
                self.end_progress.append(attack_id)
                self.attacks_completed.append(attack_id)
                print(attack_objects[attack_id].get_log_end())

        to_start = self.make_in_progress()
        for attack_id in to_start:
            attack_type = self.attack_list[self.attack_list["id"] == attack_id]["type"].values[0]
            attack_objects[attack_id] = get_attack(attack_type)
            print(attack_objects[attack_id].get_log_start())
            asyncio.run(run_attack(attack_objects[attack_id]))

        self.attacks_in_progress = self.attacks_in_progress + to_start.tolist()

    def make_in_progress(self):
        # Helper function to identify attacks that need to be started
        # Only to be called using the update function
        to_start = self.attack_list[~self.attack_list["id"].isin(self.attacks_in_progress + self.attacks_completed) & (self.attack_list["time"] <= datetime.now())]["id"].values
        return to_start
    
    

