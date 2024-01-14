import gdb
import re
import json

# usage
# gdb -q -ex "source dump_obj.py"

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
        elif (is_string(field.type)):
            obj[dict_key] = f'{value_obj[field.name].format_string()}'
        elif (is_array(field.type)):
            # array
            obj[dict_key] = list()
            size = int(re.compile('\[(\d+)\]').search(type_str)[1])
            for idx in range(0, size):
                v_obj = value_obj[field.name][idx]
                t_obj = gdb.types.get_basic_type(v_obj.type)
                obj[dict_key].append(dump_obj_impl(v_obj, t_obj))
        else:
            # scalar, std::string, struct, class
            obj[dict_key] = f'{value_obj[field.name]}'
    return obj


def is_array(type_obj:gdb.Type):
    type_str = f'{type_obj}'
    return '[' in type_str
# build-in is_array_like
    return type_obj.is_array_like

def is_string(type_obj:gdb.Type):
    type_str = f'{type_obj}'
    return '::basic_string' in type_str or 'const char *' in type_str
# build-in is_string_like
    return type_str.is_string_like

def driver_func():
    gdb.execute('file main')
    gdb.execute('b anchor')
    gdb.execute('run')
    gdb.execute('finish')
    obj_dict = dump_obj("obj")
    print(json.dumps(obj_dict))
    gdb.execute('c')
    gdb.execute('quit')

driver_func()

