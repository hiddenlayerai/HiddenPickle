# HiddenPickle

This repository houses HiddenPickle, a dissassembler, patcher, and compiler for Python Pickle files. The tool was released with during BlackHat US 2024 along with the talk [We R in a Right Pickle With All These Insecure Serialization Formats](https://www.blackhat.com/us-24/briefings/schedule/index.html#we-r-in-a-right-pickle-with-all-these-insecure-serialization-formats-39137) and allows users to recreate all of the techniques described in the talk.

## Installation

```
git clone https://github.com/hiddenlayer-engineering/HiddenPickle.git
cd HiddenPickle
pip install .
```

## Pickler

This is the pickle disassembler, it has four functions:

- read
    - this function will loop through and output all of the bytecode instructions in the pickle file
- read_next
    - this function will get the next bytecode instruction in the pickle file
- peek_next
    - does the same as read_next but doesn't increment the instruction pointer
- patch
    - this will apply a patch at a specific location

## RePickler

This is the pickle repacker, it has four functions:

- dis
    - this disassembles the pickle file
- patch_all
    - This will apply all patches to the pickle file
- create_pickle
    - When passed instructions it will create a new pickle file
- export_to_instructions
    - Takes a pickle and returns a string of instructions


### Basic Patches

```python
# do our imports
from hiddenpickle import RePickler, Patch
import pickle

# create our test class
class Test:
    def __reduce__(self):
        return (exec, ("print('hi')",))

# create the RePickler object
p = RePickler(pickle.dumps(Test()))

# check the disassembly
p.dis()

# create our patch for print('hi')
patches = [
    Patch(hook='short_binunicode', value="print('hi')", new_op='short_binunicode', new_value="print('bye')")
]

# apply our patches
data = p.patch_all(patches)

# check the new disassembly
RePickler(data).dis()
```

The output of this is:

Original:

```
0: 0x80 <proto>             4
2: 0x95 <frame>             39
11: 0x8c <short_binunicode>  builtins
21: 0x94 <memoize>           None
22: 0x8c <short_binunicode>  exec
28: 0x94 <memoize>           None
29: 0x93 <stack_global>      None
30: 0x94 <memoize>           None
31: 0x8c <short_binunicode>  print('hi')
44: 0x94 <memoize>           None
45: 0x85 <tuple1>            None
46: 0x94 <memoize>           None
47: 0x52 <reduce>            None
48: 0x94 <memoize>           None
49: 0x2e <stop>              None
```

```
0: 0x80 <proto>             4
2: 0x95 <frame>             39
11: 0x8c <short_binunicode>  builtins
21: 0x94 <memoize>           None
22: 0x8c <short_binunicode>  exec
28: 0x94 <memoize>           None
29: 0x93 <stack_global>      None
30: 0x94 <memoize>           None
31: 0x8c <short_binunicode>  print('bye')
45: 0x94 <memoize>           None
46: 0x85 <tuple1>            None
47: 0x94 <memoize>           None
48: 0x52 <reduce>            None
49: 0x94 <memoize>           None
50: 0x2e <stop>              None
```

### Changing Types with Patches

You can also change the opcode type by specifying a new opcode as long as the new value matches the expected type:

```python
from hiddenpickle import RePickler, Patch
import pickle


class Test:
    def __reduce__(self):
        return (exec, ("print('hi')",))

p = RePickler(pickle.dumps(Test()))

p.dis()

patches = [
    Patch(hook='short_binunicode', value="print('hi')", new_op='binunicode8', new_value="print('bye')")
]

data = p.patch_all(patches)

RePickler(data).dis()
```

The new data is:

```
0: 0x80 <proto>             4
2: 0x95 <frame>             39
11: 0x8c <short_binunicode>  builtins
21: 0x94 <memoize>           None
22: 0x8c <short_binunicode>  exec
28: 0x94 <memoize>           None
29: 0x93 <stack_global>      None
30: 0x94 <memoize>           None
31: 0x8d <binunicode8>       print('bye')
52: 0x94 <memoize>           None
53: 0x85 <tuple1>            None
54: 0x94 <memoize>           None
55: 0x52 <reduce>            None
56: 0x94 <memoize>           None
57: 0x2e <stop>              None
```

### Creating a New Pickle

You can also create a new pickle:

```python
from hiddenpickle import RePickler, Instruction

p = RePickler(b'')

instructions = [
    Instruction('proto', 4),
    Instruction('frame', 22)
]

data = p.create_pickle(instructions)

RePickler(data).dis()
```

Which would produce:

```
0: 0x80 <proto>             4
2: 0x95 <frame>             22
```

## Programmatic Pickle Generator

We also provide a script to generate pickle files that can be loaded with the base pickle module but allow for lambdas and functions to be serialized. This code can be found in `./scripts/generate_programatic_pickle.py` and can be modified to serialize any code you want.

*Code types requires different arguments for each Python version, the script we provide is for Python 3.10 but can easily be modified for other versions*
