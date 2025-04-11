from machine import Pin
import time

#Outputs:
siren = Pin(20, Pin.OUT)
lamp = Pin(22, Pin.OUT)
#Inputs:
button = Pin(7, Pin.IN, Pin.PULL_UP)
alarm = Pin(9, Pin.IN, Pin.PULL_UP)

class State:
    state_list = {}
    def __init__(self, name, nextstate_conditions, outputs):
        self.name
        self.nextstate_conditions = nextstate_conditions #dictionary:  {state : (input1, input2)}
        self.outputs = outputs #array
        State.state_list= {name:self}
            
    def set_nextstate():
        for name,state in state_list:
            for key, cond in state.nextstate_conditions:
                key = State.state_list[key]
    
class ASM:
    output_list = [siren, lamp]
    input_list = [button, alarm]
    
    def __init__(self, name, clkprd, initial_state):
        self.name = name
        self.delay = clkprd
        self.initial_state = initial_state
        self.current_state = initial_state        
        print(f"{self.name}, delay: {self.delay}s, initial state: {self.initial_state}")

    def run_machine(self):
        #set outputs to match state:
        for output in ASM.output_list:
            if output in self.current_state.outputs:
                output.value(1)
            else:
                output.value(0)
                
        #next state check:                
        for state, inputs in self.current_state.nextstate_conditions:                     
            for input in ASM.input_list:
                if(( input.value() == 1 and input in inputs) or (input.value() == 0 and input not in inputs)):
                    break #state conditons not met, move to next state 
                else:
                    next_state = state #state
         
        self.current_state = next_state           
                
        #delay:  
        time.sleep(self.delay)
        
            
#States - outputs in state
#off - 
#alarm0 - lamp, siren
#alarm1 - light
#ack1 - 
#ack2 - lamp
#create states:
#variable = State(name, nextstate_conditions{a : (b,c)}, outputs[]
ack2 = State("ack2", {"ack1":()}), [lamp]
ack1 = State("ack1", {"ack2":(alarm),off:()}, [])
alarm1 = State("alarm1", {"off":(button)}, [lamp])
alarm0 = State("alarm0", {"alarm0":(alarm), alarm1:(), ack:(alarm,button)}, [lamp, siren])
off = State("off", {"alarm0": (alarm)}, [])
State.set_nextstate()


#ASM
#name, clkprd, initial_state, current_state
alarm_machine = ASM("alarm system 1", 0.050, off)

while True:
    alarm_machine.run_machine()


    

