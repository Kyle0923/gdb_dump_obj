import gdb
import re
import json

# usage
# gdb -q -ex "source dump_obj.py"

# Brief:
# convert the C/C++ object specified by obj_name to a Python dictionary object
# that allows for json print-out or other processing afterward


# Ref:
# https://sourceware.org/gdb/current/onlinedocs/gdb.html/Types-In-Python.html
# https://sourceware.org/gdb/current/onlinedocs/gdb.html/Values-From-Inferior.html

def dump_obj(obj_name: str):
    gdb_value_obj = gdb.parse_and_eval(obj_name)
    gdb_type_obj = gdb.types.get_basic_type(gdb_value_obj.type)
    return dump_obj_impl(gdb_value_obj, gdb_type_obj)

def dump_obj_impl(value_obj:gdb.Value, type_obj:gdb.Type):
    if (type_obj.is_scalar or is_string(type_obj)):
        return value_obj.format_string()

    obj = dict()
    for field in type_obj.fields():

        type_str = f'{field.type}'
        dict_key = f'{field.name}({type_str})'
        # print(dict_key)

        if ('_vptr' in f'{field.name}'):
            # skip vtable
            continue
        if (field.is_base_class):
            # base class
            obj[f'BaseClass({field.type})'] = dump_obj_impl(value_obj, field.type)
        elif (is_array(field.type)):
            # array
            obj[dict_key] = list()
            size = int(re.compile('\[(\d+)\]').search(type_str)[1])
            for idx in range(0, size):
                v_obj = value_obj[field.name][idx]
                t_obj = gdb.types.get_basic_type(v_obj.type)
                obj[dict_key].append(dump_obj_impl(v_obj, t_obj))
        elif (is_stl(field.type)):
            if (len(type_str) > 30):
                # trim the name
                type_reg = re.compile('std::\w+')
                type_str = type_reg.match(type_str)[0]
                dict_key = f'{field.name}({type_str})'
            obj[dict_key] = f'{value_obj[field.name].format_string()}'
        elif (not field.type.is_scalar):
            # struct, class
            obj[dict_key] = dump_obj_impl(value_obj[field.name], field.type)
        else:
            obj[dict_key] = f'{value_obj[field.name]}'
    return obj


def is_array(type_obj:gdb.Type):
    type_str = f'{type_obj}'
    return '[' in type_str
# build-in is_array_like, require GDB 14.1
    return type_obj.is_array_like

def is_string(type_obj:gdb.Type):
    type_str = f'{type_obj}'
    return '::basic_string' in type_str or 'const char *' in type_str
# build-in is_string_like, require GDB 14.1
    return type_str.is_string_like

def is_stl(type_obj:gdb.Type):
    type_str = f'{type_obj}'
    return "std::" in type_str

#######################################################################################

def driver_func():
    # setup debug context
    gdb.execute('file test/test1') # set executable
    gdb.execute('b anchor') # set breakpoint
    gdb.execute('run')
    gdb.execute('finish')

    # retrieve variable
    var_name = "obj"
    obj_dict = dump_obj(var_name)
    print()
    print("Dumpping object:", var_name)
    print(json.dumps(obj_dict))
    print()

    gdb.execute('c')
    gdb.execute('quit')

driver_func()

