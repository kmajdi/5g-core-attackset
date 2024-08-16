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
    attack.execute()
    attack.finalize()    

class ActivityGenerator:
    def __init__(self):
        config_file = open("config.json","r")
        config = json.load(config_file)

        self.time_start = datetime.strptime(config["time_start"], '%Y-%m-%d %H:%M:%S')
        self.time_end = datetime.strptime(config["time_end"], '%Y-%m-%d %H:%M:%S')
        self.attack_type = config["attack_type"]
        self.attack_count = config["attack_count"]

        self.attacks_in_progress = []
        self.attacks_completed = []

        self.attack_objects = {}

    def start(self):
        dates = [random_date(self.time_start, self.time_end) for count in range(self.attack_count)]
        attack_types = np.random.choice(self.attack_type, size = self.attack_count, replace = True)
        attack_ids = [str(uuid.uuid4()) for h in range(self.attack_count)]
        self.attack_list = pd.DataFrame({"id": attack_ids, "time": dates, "type": attack_types})
        self.attack_list.to_csv("attack_list.csv")
        self.attack_list["time"] = pd.to_datetime(self.attack_list["time"])

    def update(self):
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
        to_start = self.attack_list[~self.attack_list["id"].isin(self.attacks_in_progress + self.attacks_completed) & (self.attack_list["time"] <= datetime.now())]["id"].values
        return to_start
    
    

