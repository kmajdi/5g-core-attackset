# 5GProvGen Malicious Activity Generator

## Description

The activity generator is designed to be extendable by any user of the framework, allowing the addition of various types of activities to generate a dataset. We provide example classes of both benign and malicious activities that can be used as templates. As long as these activities implement the activity interface, they can be integrated into our activity generator and work seamlessly with the orchestrator. Furthermore, each activity class is designed to consume a log file where the necessary timestamps for labelling the data are written, ensuring accurate and organized dataset generation.

## Implementation

### Overview

The activity generator is implemented in a way to be used in the event loop of the orchestrator. The main part consists of a start function and an update function, where the start function (called via the constructor) is used to initialize and/or load attacks based on the configuration file. The update function is run in each iteration of an event loop to initiate attacks at scheduled times in an asynchronous manner.

### Parameters

#### Instantiation Parameters: 

   - `manual`: Boolean
     - False would lead to random generation of attacks with random types among the included attack types and randomly scheduled from start time to end time
     - True would assume that attacks are already written to `attack_list.csv` and reads the attack scheduling and types from there.

#### Configuration: [`config.json`]

- `time_start`: The starting time for the framework
- `time_end`: String formatted as `%Y-%m-%d %H:%M:%S` - The ending time for the framework
- `attack_count`: (listof String) - The total number of attacks generated within start time to end time
- `attack_type`: The types of attacks to be selected from (randomly)

### Attack Scheduling

#### Automatic

A list of attacks is generated where time, type, and the identifier of each attack are generated at random based on the requirements in the configuration file (`config.json`). The randomly generated start time falls between the start and end time indicated in the config file, the size of the list will equal the attack count parameter also in the config file, and the type of attack will be randomly sampled from the list of attacks specified in the config file. As a side effect, this method of attack scheduling saves a `.csv` file with the information of each scheduled attack at `attack_list.csv ` where this file has the correct format to be used in a manual attack in a future run.

#### Manual

This method assumes that a comma-delimited file called `attack_list.csv` exists with a unique identifier for each attack, and attempts to read that file without scheduling new attacks or reliance on any parameters from `config.json`.

### Attack Generation

Attacks of the specified types are generated at their scheduled times according to the output of the attack scheduling module. Each attack individually is produced in an asynchronous manner to prevent freezing the orchestrator. Since each iteration of the event loop in the orchestrator runs the update function once at a slightly later time than the earlier iteration, the update function does the following procedure in each call:

- Once an in-progress attack is declared finalized, collects the log generated from the ending of that attack.
- Edits the status of the newly completed attacks to completed.
- If an attack has been scheduled to initiate before the current time at the iteration and the attack has not been started yet, starts the attack and collects the log generated from the starting of that attack. 
- Edits the status of the newly started attacks to in-progress.
- Returns all the collected logs as a list of strings (possibly empty in case that an iteration does not initiate or end any new attacks).

## Usage

```json
// example config.json
{ 
	"time_start": "1992-04-20 21:00:00",
	"time_end": "1992-04-20 22:00:00",
	"attack_type": [
		"denial_of_service",
		"host_write",
		"port_scanning"
	],
	"attack_count": 15
}
```

```python
# example usage for activity_generator.py
act = ActivityGenerator(manual=False)
act.start()

while True:
	act.update()
```
