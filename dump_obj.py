import gdb
import re
import json

# usage
# gdb -x dump_obj.py

# Brief:
# convert the C/C++ object specified by obj_name to a Python dictionary object
# that allows for json print out or other processing afterward


# Ref:
# https://sourceware.org/gdb/current/onlinedocs/gdb.html/Types-In-Python.html
# https://sourceware.org/gdb/current/onlinedocs/gdb.html/Values-From-Inferior.html

class DumpObj(gdb.Command):

    def __init__(self):
        super(DumpObj, self).__init__("dump-obj", gdb.COMMAND_DATA)

    def complete(self, text, word):
        frame = gdb.selected_frame()
        block = gdb.block_for_pc(frame.pc())
        # print(text)
        if block is not None:
            # print(11111)
            symbols = [sym.name for sym in block if sym.is_variable and sym.name.startswith(text)]
            return symbols
        else:
            return gdb.COMPLETE_EXPRESSION

    def invoke(self, arg, from_tty):
        self.dump_obj(arg, True)

    def dump_obj(self, var_name, print_json=False):
        gdb_value_obj = gdb.parse_and_eval(var_name)
        gdb_type_obj = gdb.types.get_basic_type(gdb_value_obj.type)
        obj_dict = self.dump_obj_impl(gdb_value_obj, gdb_type_obj)
        if print_json:
            print(json.dumps(obj_dict))
        return obj_dict

    def dump_obj_impl(self, value_obj:gdb.Value, type_obj:gdb.Type):

        char_arr_reg = re.compile('char \[\d*\]')

        if f'{type_obj}' in ['const char', 'char']:
            return chr(value_obj)

        if type_obj.code == gdb.TYPE_CODE_INT:
            return int(value_obj)

        if type_obj.code == gdb.TYPE_CODE_FLT:
            # use .format_string() to preserve the underlying precision
            return float(value_obj.format_string())

        if type_obj.code == gdb.TYPE_CODE_STRING:
            # does not capture C-string in my machine with gdb 12.1, ubuntu 22.04
            return value_obj.string()

        if ('const char *' == f'{type_obj}'):
            if (int(value_obj) == 0):
                return "((nullptr))"
            return value_obj.string()

        if char_arr_reg.search(f'{type_obj}') and int(value_obj[int(type_obj.range()[1])]) == 0:
            # char [] and the last char is \0
            return value_obj.string()

        if 'std::string' == f'{type_obj}':
            # std::string
            return DumpObj.trim_str(value_obj.format_string())

        if type_obj.code == gdb.TYPE_CODE_PTR:
            return self.ptr_info(value_obj)

        if type_obj.code == gdb.TYPE_CODE_ARRAY:
            # Convert array to a Python list
            size = int(type_obj.range()[1]) + 1
            return [self.dump_obj_impl(value_obj[i], value_obj[i].type) for i in range(size)]

        if DumpObj.is_stl(type_obj):
            return value_obj.format_string()

        if type_obj.code == gdb.TYPE_CODE_STRUCT:
            return self.convert_struct(value_obj, type_obj)

        # Default case: Convert to string
        return value_obj.format_string()

    def ptr_info(self, ptr_obj:gdb.Value):
        addr = int(ptr_obj)
        if (addr == 0):
            return "((nullptr))"
        target = ptr_obj.dereference()
        if target.type.code in [gdb.TYPE_CODE_INT, gdb.TYPE_CODE_FLT]:
            # number type
            value = target.format_string()
        else:
            symbol = gdb.execute('info symbol {}'.format(addr), to_string=True)
            if symbol.startswith('No symbol'):
                # member variables would not be able to look up symbol
                value = 'anonymous'
            else:
                # only global scope variable would have this
                value = symbol.strip().split(' ')[0]
        return f'{value}({self.format_type_name(target)}) @ {hex(addr)}'

    def convert_struct(self, value_obj:gdb.Value, type_obj:gdb.Type):
        # Convert struct to a Python dictionary
        result = {}
        for field in type_obj.fields():
            field_name = f'{field.name}'
            if ('_vptr' in field_name):
                # skip vtable
                continue
            if (field.is_base_class):
                # base class
                result[f'BaseClass({field.type})'] = self.dump_obj_impl(value_obj, field.type)
            else:
                field_value = value_obj[field_name]
                type_name = self.format_type_name(field_value)
                result[f'{field_name}({type_name})'] = self.dump_obj_impl(field_value, field.type)
        return result

    # pretty-print type names
    def format_type_name(self, value_obj:gdb.Value):
        type_obj = value_obj.type
        type_name = f'{type_obj}'

        type_name = type_name.replace(DumpObj.get_std_string_type(), "std::string")
        if (type_obj.code == gdb.TYPE_CODE_UNION):
            return f'union {type_name}'
        if (type_obj.code == gdb.TYPE_CODE_ENUM):
            return f'enum {type_name}'
        if (type_obj.code == gdb.TYPE_CODE_ARRAY):
            if (value_obj[0].type.code == gdb.TYPE_CODE_ENUM):
                return f'enum {type_name}'
            return type_name

        std_containers = ['map', 'unordered_map', 'vector', 'set', 'unordered_set']
        std_containers = ['std::' + e for e in std_containers]
        if any([type_name.startswith(container) for container in std_containers]):
            if type_name.startswith('std::map') or type_name.startswith('std::unordered_map'):
                template = DumpObj.get_template_arg(type_obj, 2)
            else:
                template = DumpObj.get_template_arg(type_obj, 1)
            container = type_name.split('<')[0]
            return f'{container}<{template}>'

        if "::list<" in type_name:
            container = 'std::list'
            template = DumpObj.get_template_arg(type_obj)
            return f'{container}<{template}>'

        return type_name

    # return the type args in C++ template
    @staticmethod
    def get_template_arg(type_obj:gdb.Type, num = 1):
        template_args = f'{type_obj.template_argument(0)}'
        for i in range(1, num):
            template_args += ', ' + f'{type_obj.template_argument(i)}'
        template_args = template_args.replace(DumpObj.get_std_string_type(), "std::string")
        return template_args

    @staticmethod
    def get_std_string_type():
        if not hasattr(DumpObj, 'std_string_type'):
            string_type = gdb.lookup_type('std::string')
            DumpObj.std_string_type = f'{string_type.strip_typedefs()}'
        return DumpObj.std_string_type

    @staticmethod
    def is_stl(type_obj:gdb.Type):
        type_str = f'{type_obj}'
        return type_str.startswith('std::')

    @staticmethod
    # remove the heading and trailing double quote
    def trim_str(string: str):
        if (string.startswith('"') and string.endswith('"')):
            return string[1:-1]
        return string


DumpObj()




#######################################################################################

# def driver_func():
#     # setup debug context
#     gdb.execute('file test/test1') # set executable
#     gdb.execute('b anchor') # set breakpoint
#     gdb.execute('run')
#     gdb.execute('finish')

#     # retrieve variable
#     var_name = "obj"
#     dump_obj = DumpObj()
#     obj_dict = dump_obj.dump_obj(var_name)
#     print()
#     print("Dumpping object:", var_name)
#     print(json.dumps(obj_dict))
#     print()

#     gdb.execute('c')
#     gdb.execute('quit')

# driver_func()

