import sys

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
        #Optional config entries:
        optional_entries = ['hw_conditions', 'hw_triggers', 'env_triggers'] 
        #Hardware conditions - external conditions to happen for the step to be completed
        #Hardware triggers - external actions that are executed once the step is completed
        #Environment triggers - actions that influence global game variables, such as room overall state (lighting, sounds, etc.), time left or game status
        for entry in optional_entries:
            setattr(self, entry, config[entry] if entry in config.keys() else [] )

    def enable(self):
        self.enabled = True
        #Need to register callbacks

    def complete_conditions_met(self, condition_process_function):
        if not self.enabled():
            return False #A step cannot be finished if it's not enabled.
        if self.hw_conditions: 
            #All of the conditions need to be met to continue
            return all(condition_process_function('hw_condition', condition) for condition in self.hw_conditions)
        else:
            return True #As for now, only hardware conditions are supported

    def finish(self):
        pass            
    
class StepManager():
    config = None
    steps = []
    enabled_steps = []

    devices = {}

    finished_steps = [] #Check if needed

    def __init__(self, config_filename):
        self.config = json.load(config_filename)
        for step_config in self.config.steps:
            step = Step(step_config)
            self.steps.append(step)
            if step.enable_on_start = True:
                self.enable_step(step)
        self.update_enabled_steps()        
        #Maybe exec init triggers?

    def update_enabled_steps(self):
        self.enabled_steps = []
        for step in self.steps:
            if step.enabled:
                self.enabled_steps.append(step)
        return True

    def enable_step(step):
        step.enable()

    def process_condition(condition_type, condition):
        condition_type_mapping = { "hw_condition": self.process_hardware_condition}
        cpf = condition_type_mapping[condition_type]
        return cpf(condition)

    def process_hardware_condition(condition)
        sensor_name = condition['sensor']
        method_name = condition['method']
        sensor = get_sensor_by_name(sensor_name)
        method = getattr(sensor, condition[method_name])
        args = condition['args'] if 'args' in conditions else []
        kwargs = condition['kwargs'] if 'kwargs' in conditions else {}
        return method(*args, **kwargs)

    def get_step_by_name(step_name):
        for step in self.steps:
            if step.name = step_name:
                return step

    def poll(self):
        for step in self.enabled_steps:
            if step.complete_conditions_met():
                
                self.execute_triggers(step.finished_triggers)
                for step_name in step.steps_to_enable:
                    self.enable_step(self.get_step_by_name(step_name))
                self.disable_steps(step.name)
                #disable the step afterwards
        self.update_enabled_steps()
                    


step_manager = StepManager('scenario_small.json')
while True:
    step_manager.poll()
