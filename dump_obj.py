import gdb
from collections import defaultdict
import re

# usage
# gdb -q -ex "source dump_obj.py"

def dump_obj(value_obj:gdb.Value ,type_obj:gdb.Type):
    if (type_obj.is_scalar or is_string(type_obj)):
        return value_obj.format_string()
    # obj = defaultdict(lambda: defaultdict)
    obj = dict()
    for f in type_obj.fields():
        print(f"####{f.name}#{f.type}")
        type_str = f'{f.type}'
        if ('_vptr' in f'{f.name}'):
            # skip vtable
            continue
        if (f.is_base_class):
            # base class
            obj[f'BaseClass({f.name})'] = dump_obj(value_obj, f.type)
        elif (is_array(f.type)):
            # array
            obj[f'{f.name}({type_str})'] = list()
            size = int(re.compile('\[(\d+)\]').search(type_str)[1])
            for idx in range(0, size):
                v_obj = value_obj[f.name][idx]
                t_obj = gdb.types.get_basic_type(v_obj.type)
                obj[f'{f.name}({type_str})'].append(dump_obj(v_obj, t_obj))
        elif (is_string(f.type)):
            # string
            obj[f'{f.name}({type_str})'] = dump_obj(value_obj[f.name], f.type)
        elif (not f.type.is_scalar):
            # struct, class
            obj[f'{f.name}({type_str})'] = dump_obj(value_obj[f.name], f.type)
        else:
            # scalar
            obj[f'{f.name}({type_str})'] = f'{value_obj[f.name]}'
    return obj


def is_array(type_obj:gdb.Type):
    type_str = f'{type_obj}'
    return '[' in type_str
# build-in is_array_like
    return type_obj.is_array_like

def is_string(type_obj:gdb.Type):
    type_str = f'{type_obj}'
    return 'string' in type_str
# build-in is_string_like
    return type_str.is_string_like


def driver_func():
    gdb.execute('file main')
    gdb.execute('b anchor')
    gdb.execute('run')
    gdb.execute('finish')
    # obj = gdb.execute('p obj', to_string=True)
    # print("###", obj)
    gdb_obj = gdb.parse_and_eval("obj")
    # print("####", gdb_obj.type)
    type_obj = gdb.types.get_basic_type(gdb_obj.type)
    obj_dict = dump_obj(gdb_obj, type_obj)
    print(obj_dict)
    gdb.execute('c')
    gdb.execute('quit')

driver_func()

