from hiddenpickle.constants import *
import sys

class Pickler:
    def __init__(self, data):
        self.position = 0
        self.data = data

    def no_op(self):
        pass

    def read_bytes(self, length):
        value = self.data[self.position:self.position+length]
        self.position += length
        return value

    def u_num(self, length):
        return int.from_bytes(self.read_bytes(length), sys.byteorder)
    
    def u1(self):
        return self.u_num(1)
    
    def u2(self):
        return self.u_num(2)
    
    def u4(self):
        return self.u_num(4)

    def u8(self):
        return self.u_num(8)

    def s_num(self, length):
        return int.from_bytes(self.read_bytes(length), sys.byteorder, signed=True)
        
    def s4(self):
        return self.s_num(4)

    def long_num(self, length):
        return self.s_num(length)
        
    def long1(self):
        length = self.u1()
        return self.long_num(length)
        
    def long4(self):
        length = self.u4()
        return self.long_num(length)
    
    def get_unicode_string(self, length):
        return self.read_bytes(length).decode('utf-8')
    
    def get_string(self, length):
        return str(self.read_bytes(length))
        
    def unicodestring1(self):
        length = self.u1()
        return self.get_unicode_string(length)
        
    def unicodestring4(self):
        length = self.u4()
        return self.get_unicode_string(length)
        
    def unicodestring8(self):
        length = self.u8()
        return self.get_unicode_string(length)
    
    def unicodestringnl(self):
        s = ''
        val = self.read_bytes(1)
        while val != 0x0a:
            s += val
            val = self.read_bytes(1)
        return val.decode("utf-8")

    def string1(self):
        length = self.u1()
        return self.get_string(length)

    def string4(self):
        length = self.s4()
        return self.get_string(length)

    def stringnl(self):
        s = b''
        val = self.read_bytes(1)
        while val != b'\n':
            s += val
            val = self.read_bytes(1)
        print(s)
        return s.decode()
        
    def stringnl_noescape(self):
        return self.stringnl()
            
    def stringnl_noescape_pair(self):
        return self.stringnl_noescape() + '|' + self.stringnl_noescape()

    def bytes1(self):
        length = self.u1()
        return self.read_bytes(length)
        
    def bytes4(self):
        length = self.u4()
        return self.read_bytes(length)
        
    def bytes8(self):
        length = self.u8()
        return self.read_bytes(length)

    def bytearray8(self):
        length = self.u8()
        return self.read_bytes(length)
    
    def decimalnl_short(self):
        s = ''
        val = self.read_bytes(1)
        while val != 0x0a:
            s += val
            val = self.read_bytes(1)
        return val

    def decimalnl_long(self):
        s = ''
        val = self.read_bytes(1)
        while val != 0x0a:
            s += val
            val = self.read_bytes(1)
        val = self.read_bytes(1)
        print(val, "should be L")
        exit()
        return val

    def floatnl(self):
        s = ''
        val = self.read_bytes(1)
        while val != 0x0a:
            s += val
            val = self.read_bytes(1)
        return val
        
    def f8be(self):
        return str(float(self.u8()))
        
    def get_function(self, op):
        if op == 0x28 or op == 'mark':
            return self.no_op
        elif op == 0x29 or op == 'empty_tuple':
            return self.no_op
        elif op == 0x2e or op == 'stop':
            return self.no_op
        elif op == 0x30 or op == 'pop':
            return self.no_op
        elif op == 0x31 or op == 'pop_mark':
            return self.no_op
        elif op == 0x32 or op == 'dup':
            return self.no_op
        elif op == 0x42 or op == 'binbytes':
            return self.bytes4
        elif op == 0x43 or op == 'short_binbytes':
            return self.bytes1
        elif op == 0x46 or op == 'float':
            return self.floatnl
        elif op == 0x47 or op == 'binfloat':
            return self.f8be
        elif op == 0x49 or op == 'int':
            return self.decimalnl_short
        elif op == 0x4a or op == 'binint':
            return self.s4
        elif op == 0x4b or op == 'binint1':
            return self.u1
        elif op == 0x4c or op == 'long':
            return self.decimalnl_long
        elif op == 0x4d or op == 'binint2':
            return self.u2
        elif op == 0x4e or op == 'none':
            return self.no_op
        elif op == 0x50 or op == 'persid':
            return self.stringnl_noescape
        elif op == 0x51 or op == 'binpersid':
            return self.no_op
        elif op == 0x52 or op == 'reduce':
            return self.no_op
        elif op == 0x53 or op == 'string':
            return self.stringnl
        elif op == 0x54 or op == 'binstring':
            return self.string4
        elif op == 0x55 or op == 'short_binstring':
            return self.string1
        elif op == 0x56 or op == 'unicode':
            return self.unicodestringnl
        elif op == 0x58 or op == 'binunicode':
            return self.unicodestring4
        elif op == 0x5d or op == 'empty_list':
            return self.no_op
        elif op == 0x61 or op == 'append':
            return self.no_op
        elif op == 0x62 or op == 'build':
            return self.no_op
        elif op == 0x63 or op == 'global_opcode':
            return self.stringnl_noescape_pair
        elif op == 0x64 or op == 'dict':
            return self.no_op
        elif op == 0x65 or op == 'appends':
            return self.no_op
        elif op == 0x67 or op == 'get':
            return self.decimalnl_short
        elif op == 0x68 or op == 'binget':
            return self.u1
        elif op == 0x69 or op == 'inst':
            return self.stringnl_noescape_pair
        elif op == 0x6a or op == 'long_binget':
            return self.u4
        elif op == 0x6c or op == 'list':
            return self.no_op
        elif op == 0x6f or op == 'obj':
            return self.no_op
        elif op == 0x70 or op == 'put':
            return self.decimalnl_short
        elif op == 0x71 or op == 'binput':
            return self.u1
        elif op == 0x72 or op == 'long_binput':
            return self.u4
        elif op == 0x73 or op == 'setitem':
            return self.no_op
        elif op == 0x74 or op == 'tuple':
            return self.no_op
        elif op == 0x75 or op == 'setitems':
            return self.no_op
        elif op == 0x7d or op == 'empty_dict':
            return self.no_op
        elif op == 0x80 or op == 'proto':
            return self.u1
        elif op == 0x81 or op == 'newobj':
            return self.no_op
        elif op == 0x82 or op == 'ext1':
            return self.u1
        elif op == 0x83 or op == 'ext2':
            return self.u2
        elif op == 0x84 or op == 'ext4':
            return self.u4
        elif op == 0x85 or op == 'tuple1':
            return self.no_op
        elif op == 0x86 or op == 'tuple2':
            return self.no_op
        elif op == 0x87 or op == 'tuple3':
            return self.no_op
        elif op == 0x88 or op == 'newtrue':
            return self.no_op
        elif op == 0x89 or op == 'newfalse':
            return self.no_op
        elif op == 0x8a or op == 'long1':
            return self.long1
        elif op == 0x8b or op == 'long4':
            return self.long4
        elif op == 0x8c or op == 'short_binunicode':
            return self.unicodestring1
        elif op == 0x8d or op == 'binunicode8':
            return self.unicodestring8
        elif op == 0x8e or op == 'binbytes8':
            return self.bytes8
        elif op == 0x8f or op == 'empty_set':
            return self.no_op
        elif op == 0x90 or op == 'additems':
            return self.no_op
        elif op == 0x91 or op == 'frozenset':
            return self.no_op
        elif op == 0x92 or op == 'newobj_ex':
            return self.no_op
        elif op == 0x93 or op == 'stack_global':
            return self.no_op
        elif op == 0x94 or op == 'memoize':
            return self.no_op
        elif op == 0x95 or op == 'frame':
            return self.u8
        elif op == 0x96 or op == 'bytearray8':
            return self.bytearray8
        elif op == 0x97 or op == 'next_buffer':
            return self.no_op
        elif op == 0x98 or op == 'readonly_buffer':
            return self.no_op
        return None
    
    def create_patch(self, op, value):
        f = self.get_patch_function(op)
        if f == None:
            raise Exception("Could not find patch function")
        return op.to_bytes(1, sys.byteorder) + f(value)
    
    def add_instruction(self, op, value):
        self.data += self.create_patch(op, value)

    def patch(self, patch, position):
        pre_patch_position = self.position
        ##################################

        self.position = position
        self.read_next()

        size_of_instruction = self.position - position
        pre_patch_data = self.data[0:position]
        post_patch_data = self.data[self.position:]

        new_data = self.create_patch(patch.new_op, patch.new_value)

        self.data = pre_patch_data + new_data + post_patch_data

        ##################################
        self.position = pre_patch_position

    

    def no_op_patch(self, value):
        return b''

    def u_num_bytes(self, value, length):
        return value.to_bytes(length, sys.byteorder)
    
    def u1_patch(self, value):
        return self.u_num_bytes(value, 1)
    
    def u2_patch(self, value):
        return self.u_num_bytes(value, 2)
    
    def u4_patch(self, value):
        return self.u_num_bytes(value, 4)

    def u8_patch(self, value):
        return self.u_num_bytes(value, 8)

    def s_num_bytes(self, value, length):
        return value.to_bytes(length, sys.byteorder, signed=True)
        
    def s4_patch(self, value):
        return self.s_num_bytes(value, 4)
    
    def byte_length(self, i):
        return (i.bit_length() + 7) // 8

    def long_num_bytes(self, value, length):
        return self.s_num_bytes(value, length)
        
    def long1_patch(self, value):
        length = self.byte_length(value)
        return self.u1_patch(length) + self.long_num_bytes(value, length)
        
    def long4_patch(self, value):
        length = self.byte_length(value)
        return self.u4_patch(length) + self.long_num_bytes(value, length)
    
    def set_unicode_string(self, value):
        return value.encode('utf-8')
    
    def set_string(self, value):
        return value.encode()
        
    def unicodestring1_patch(self, value):
        length = len(value)
        return self.u1_patch(length) + self.set_unicode_string(value)
        
    def unicodestring4_patch(self, value):
        length = len(value)
        return self.u4_patch(length) + self.set_unicode_string(value)
        
    def unicodestring8_patch(self, value):
        length = len(value)
        return self.u8_patch(length) + self.set_unicode_string(value)
    
    def unicodestringnl_patch(self, value):
        return value.encode("utf-8") + b'\x0a'

    def string1_patch(self, value):
        length = len(value)
        return self.u1_patch(length) + self.set_string(value)

    def string4_patch(self, value):
        length = len(value)
        return self.s4_patch(length) + self.set_string(value)

    def stringnl_patch(self, value):
        return b'"' + value.encode() + b'"\x0a'
        
    def stringnl_noescape_patch(self, value):
        return self.stringnl_patch(value)
            
    def stringnl_noescape_pair_patch(self, value):
        return self.unicodestringnl_patch(value.split('|')[0]) + self.unicodestringnl_patch(value.split('|')[1])

    def bytes1_patch(self, value):
        length = len(value)
        return self.u1_patch(length) + value
        
    def bytes4_patch(self, value):
        length = len(value)
        return self.u4_patch(length) + value
        
    def bytes8_patch(self, value):
        length = len(value)
        return self.u8_patch(length) + value

    def bytearray8_patch(self, value):
        return self.bytes8_patch(value)
    
    def decimalnl_short_patch(self, value):
        return str(value).encode() + "\x0a"

    def decimalnl_long_patch(self, value):
        raise Exception("Not Implemented")

    def floatnl_patch(self, value):
        return str(value).encode() + "\x0a"
        
    def f8be_patch(self, value):
        raise Exception("Not Implemented")
    
    def get_patch_function(self, op):
        if op == 0x28 or op == 'mark':
            return self.no_op_patch
        elif op == 0x29 or op == 'empty_tuple':
            return self.no_op_patch
        elif op == 0x2e or op == 'stop':
            return self.no_op_patch
        elif op == 0x30 or op == 'pop':
            return self.no_op_patch
        elif op == 0x31 or op == 'pop_mark':
            return self.no_op_patch
        elif op == 0x32 or op == 'dup':
            return self.no_op_patch
        elif op == 0x42 or op == 'binbytes':
            return self.bytes4_patch
        elif op == 0x43 or op == 'short_binbytes':
            return self.bytes1_patch
        elif op == 0x46 or op == 'float':
            return self.floatnl_patch
        elif op == 0x47 or op == 'binfloat':
            return self.f8be_patch
        elif op == 0x49 or op == 'int':
            return self.decimalnl_short_patch
        elif op == 0x4a or op == 'binint':
            return self.s4_patch
        elif op == 0x4b or op == 'binint1':
            return self.u1_patch
        elif op == 0x4c or op == 'long':
            return self.decimalnl_long_patch
        elif op == 0x4d or op == 'binint2':
            return self.u2_patch
        elif op == 0x4e or op == 'none':
            return self.no_op_patch
        elif op == 0x50 or op == 'persid':
            return self.stringnl_noescape_patch
        elif op == 0x51 or op == 'binpersid':
            return self.no_op_patch
        elif op == 0x52 or op == 'reduce':
            return self.no_op_patch
        elif op == 0x53 or op == 'string':
            return self.stringnl_patch
        elif op == 0x54 or op == 'binstring':
            return self.string4_patch
        elif op == 0x55 or op == 'short_binstring':
            return self.string1_patch
        elif op == 0x56 or op == 'unicode':
            return self.unicodestringnl_patch
        elif op == 0x58 or op == 'binunicode':
            return self.unicodestring4_patch
        elif op == 0x5d or op == 'empty_list':
            return self.no_op_patch
        elif op == 0x61 or op == 'append':
            return self.no_op_patch
        elif op == 0x62 or op == 'build':
            return self.no_op_patch
        elif op == 0x63 or op == 'global_opcode':
            return self.stringnl_noescape_pair_patch
        elif op == 0x64 or op == 'dict':
            return self.no_op_patch
        elif op == 0x65 or op == 'appends':
            return self.no_op_patch
        elif op == 0x67 or op == 'get':
            return self.decimalnl_short_patch
        elif op == 0x68 or op == 'binget':
            return self.u1_patch
        elif op == 0x69 or op == 'inst':
            return self.stringnl_noescape_pair_patch
        elif op == 0x6a or op == 'long_binget':
            return self.u4_patch
        elif op == 0x6c or op == 'list':
            return self.no_op_patch
        elif op == 0x6f or op == 'obj':
            return self.no_op_patch
        elif op == 0x70 or op == 'put':
            return self.decimalnl_short_patch
        elif op == 0x71 or op == 'binput':
            return self.u1_patch
        elif op == 0x72 or op == 'long_binput':
            return self.u4_patch
        elif op == 0x73 or op == 'setitem':
            return self.no_op_patch
        elif op == 0x74 or op == 'tuple':
            return self.no_op_patch
        elif op == 0x75 or op == 'setitems':
            return self.no_op_patch
        elif op == 0x7d or op == 'empty_dict':
            return self.no_op_patch
        elif op == 0x80 or op == 'proto':
            return self.u1_patch
        elif op == 0x81 or op == 'newobj':
            return self.no_op_patch
        elif op == 0x82 or op == 'ext1':
            return self.u1_patch
        elif op == 0x83 or op == 'ext2':
            return self.u2_patch
        elif op == 0x84 or op == 'ext4':
            return self.u4_patch
        elif op == 0x85 or op == 'tuple1':
            return self.no_op_patch
        elif op == 0x86 or op == 'tuple2':
            return self.no_op_patch
        elif op == 0x87 or op == 'tuple3':
            return self.no_op_patch
        elif op == 0x88 or op == 'newtrue':
            return self.no_op_patch
        elif op == 0x89 or op == 'newfalse':
            return self.no_op_patch
        elif op == 0x8a or op == 'long1':
            return self.long1_patch
        elif op == 0x8b or op == 'long4':
            return self.long4_patch
        elif op == 0x8c or op == 'short_binunicode':
            return self.unicodestring1_patch
        elif op == 0x8d or op == 'binunicode8':
            return self.unicodestring8_patch
        elif op == 0x8e or op == 'binbytes8':
            return self.bytes8_patch
        elif op == 0x8f or op == 'empty_set':
            return self.no_op_patch
        elif op == 0x90 or op == 'additems':
            return self.no_op_patch
        elif op == 0x91 or op == 'frozenset':
            return self.no_op_patch
        elif op == 0x92 or op == 'newobj_ex':
            return self.no_op_patch
        elif op == 0x93 or op == 'stack_global':
            return self.no_op_patch
        elif op == 0x94 or op == 'memoize':
            return self.no_op_patch
        elif op == 0x95 or op == 'frame':
            return self.u8_patch
        elif op == 0x96 or op == 'bytearray8':
            return self.bytearray8_patch
        elif op == 0x97 or op == 'next_buffer':
            return self.no_op_patch
        elif op == 0x98 or op == 'readonly_buffer':
            return self.no_op_patch
        return None
        
    def read_next(self):
        if self.position >= len(self.data):
            return (self.position, "Unexpected EOF", None)

        position = self.position
        op = self.data[self.position]
        self.position += 1
        f = self.get_function(op)
        if f != None:
            value = f()

        return (position, op, value)
    
    def peek_next(self):
        if self.position >= len(self.data):
            return ("Unexpected EOF", None)
        
        position = self.position
        op = self.data[self.position]
        self.position += 1
        f = self.get_function(op)
        if f != None:
            value = f()
        self.position = position
        return (op, value)

    

    def read(self):
        (position, op, value) = self.read_next()
        while op != VALUE_TO_OPCODE['stop']:
            print(str(position) + ":",hex(op) + '{:20}'.format(" <" + OPCODE_TO_VALUE[op] + ">"), value)
            (position, op, value) = self.read_next()
            if op == "Unexpected EOF":
                break
        if type(op) == int:
            print(str(position) + ":",hex(op) + '{:20}'.format(" <" + OPCODE_TO_VALUE[op] + ">"), value)