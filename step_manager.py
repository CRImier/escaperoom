import sys
import json

import logging
logging.basicConfig(stream = sys.stdout, level=logging.DEBUG)

class Step():
    enabled = False
    finished =  False

    enable_conditions = []

    def __init__(self, config):
        #Obligatory config entries:
        obligatory_entries = ['name', 'description', 'steps_that_enable']
        #Name
        #Description
        #Steps to be completed to enable this step
        try:
            for entry in obligatory_entries:
                try:
                    setattr(self, entry, config[entry])
                except KeyError:
                    if hasattr(self, 'name'):
                        logging.error("Step {} lacks obligatory attribute {}".format(name, entry))
                    else:
                        logging.error("Error in scenario: name not set for a step")
                    raise
        except KeyError:
            logging.error("A problem with scenario was found, unable to continue.")
            sys.exit(2)
        self.enable_on_start = True if 'start' in self.steps_that_enable else False
        #Optional config entries:
        optional_entries = ['hw_conditions', 'hw_triggers', 'env_triggers'] 
        #Hardware conditions - external conditions to happen for the step to be completed
        #Hardware triggers - external actions that are executed once the step is completed
        #Environment triggers - actions that influence global game variables, such as room overall state (lighting, sounds, etc.), time left or game status
        for entry in optional_entries:
            setattr(self, entry, config[entry] if entry in config.keys() else [] ) #If the entry is not set, we'll set it to empty list to avoid KeyErrors 

    def enable(self):
        logging.info("Step enabled: {}".format(self.name))
        self.enabled = True

    def disable(self):
        logging.info("Step disabled: {}".format(self.name))
        self.enabled = False

    def complete_conditions_met(self, condition_process_function):
        if not self.enabled:
            logging.warning("Bug: a check of step's conditions was attempted with step not enabled")
            return False
        if self.hw_conditions: 
            #All of the conditions need to be met to continue
            return all(condition_process_function('hw_condition', condition) for condition in self.hw_conditions)
        else:
            return True #TODO: as for now, only hardware conditions are supported, my employer hasn't needed any more

    def finish(self):
        pass            
    
class StepManager():
    config = {}
    steps = []
    enabled_steps = []
    devices = {}
    finished_steps = [] #Check if needed

    def __init__(self, config, room_manager):
        self.room = room_manager
        self.devices = room_manager.devices
        self.config = config
        for step_config in self.config:
            step = Step(step_config)
            if step.enable_on_start == True:
                logging.debug("Enabling step...")
                self.enable_step(step)
            self.steps.append(step)
        self.update_enabled_steps()        
        #Maybe exec init triggers?

    def update_enabled_steps(self):
        for step in self.steps:
            #Checking for steps that have met their enable conditions but haven't yet been activated during the game
            if not step.enabled and step not in self.finished_steps:
                #If at least one of the steps in enable conditions is not finished, the step won't be activated
                results = [] #Step completeness list. Maybe it can be made to look better than this
                for step_name in step.steps_that_enable:
                    enabling_step = self.get_step_by_name(step_name)
                    results.append(enabling_step in self.finished_steps)
                if all(results):
                    #Conditions for step activation met
                    logging.info("Step {} enabled because of following steps being completed: {}".format(step.name, ",".join(step.steps_that_enable)))
                    step.enable()
        #Now rebuild the enabled_steps list from scratch. This is the most straightforward and working solution ;-)
        self.enabled_steps = []
        for step in self.steps:
            print("{} - {}".format(step.name, 'enabled' if step.enabled else 'disabled'))
            if step.enabled:
                self.enabled_steps.append(step)
        #Maybe we could merge those loops
        logging.info("Enabled steps updated, count: {}".format(len(self.enabled_steps)))
        logging.debug(self.enabled_steps)
        return True

    def disable_step(self, step):
        step.disable()

    def finish_step(self, step):
        step.disable()
        self.finished_steps.append(step)

    def enable_step(self, step):
        step.enable()

    def execute_triggers(self, step):
        for hw_trigger in step.hw_triggers:
            print(hw_trigger)
            self.room.execute_hw_trigger(hw_trigger)
        for env_trigger in step.env_triggers:
            print(env_trigger)
            #self.room_manager.execute_env_trigger(env_trigger)

    def process_condition(self, condition_type, condition):
        condition_type_mapping = { "hw_condition": self.process_hardware_condition}
        cpf = condition_type_mapping[condition_type]
        return cpf(condition)

    def get_sensor_by_name(self, name):
        return self.room.devices[name]

    def process_hardware_condition(self, condition):
        logging.info("Processing condition {}".format(condition))
        sensor_name = condition['sensor']
        method_name = condition['method']
        sensor = self.get_sensor_by_name(sensor_name)
        method = getattr(sensor, method_name)
        args = condition['args'] if 'args' in condition else []
        kwargs = condition['kwargs'] if 'kwargs' in condition else {}
        return method(*args, **kwargs)

    def get_step_by_name(self, step_name):
        for step in self.steps:
            if step.name == step_name:
                return step

    def poll(self):
        logging.debug("Step manager - polling...")
        for step in self.enabled_steps:
            if step.complete_conditions_met(self.process_condition):
                logging.info("Step has been completed: {}".format(step.name))
                self.execute_triggers(step)
                self.finish_step(step)
                self.update_enabled_steps()
