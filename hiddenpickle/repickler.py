from hiddenpickle.pickler import Pickler
from hiddenpickle.constants import *

class Patch:
    def __init__(self, hook, new_op, new_value, value=None):
        if type(hook) == int:
            self.op = hook
        else:
            self.op = VALUE_TO_OPCODE[hook]
        self.value = value
        
        if type(new_op) == int:
            self.new_op = new_op
        else:
            self.new_op = VALUE_TO_OPCODE[new_op]

        self.new_value = new_value

    def should_patch(self, op, value):
        if self.op == op:
            return (value == self.value or self.value == None)
        return False

class Instruction:
    def __init__(self, op, value):
        if type(op) == int:
            self.op = op
        else:
            self.op = VALUE_TO_OPCODE[op]

        self.value = value


class RePickler:
    def __init__(self, data):
        self.data = data

    def dis(self):
        pickler = Pickler(self.data)
        pickler.read()

    def patch(self, pickler, patch):
        print("triggered patch")

    def patch_all(self, patches):
        pickler = Pickler(self.data)
        (op, value) = pickler.peek_next()
        while op != VALUE_TO_OPCODE['stop'] and op != "Unexpected EOF":

            for patch in patches:
                if patch.should_patch(op, value):
                    pickler.patch(patch, pickler.position)

            pickler.read_next()

            (op, value) = pickler.peek_next()

        return pickler.data
    
    def create_pickle(self, instructions):
        pickler = Pickler(b'')
        for instruction in instructions:
            pickler.add_instruction(instruction.op, instruction.value)
        return pickler.data
    
    def export_to_instructions(self):
        s = "["

        pickler = Pickler(self.data)
        (position, op, value) = pickler.read_next()
        while op != VALUE_TO_OPCODE['stop'] and op != "Unexpected EOF":

            if value == None:
                s += "\n    Instruction('" + str(OPCODE_TO_VALUE[op]) + "', None)," 
            elif type(value) == int:
                s += "\n    Instruction('" + str(OPCODE_TO_VALUE[op]) + "', " + str(value) + ")," 
            elif type(value) == str:
                s += "\n    Instruction('" + str(OPCODE_TO_VALUE[op]) + "', '" + value + "')," 
            elif type(value) == bytes:
                try:
                    s += "\n    Instruction('" + str(OPCODE_TO_VALUE[op]) + "', b'" + value.decode() + "')," 
                except:
                    s += "\n    Instruction('" + str(OPCODE_TO_VALUE[op]) + "', " + str(value) + ")," 
            else:
                print(type(value))
                raise Exception("Error")

            (position, op, value) = pickler.read_next()
        s += "\n    Instruction('" + str(OPCODE_TO_VALUE[op]) + "', None)," 

        s += "\n]"

        return s