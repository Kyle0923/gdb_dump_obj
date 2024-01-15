# GDB dump-obj extension
A GDB-Python script that converts the C/C++ object specified by obj_name to a Python dictionary object which allows for json print out or other processing afterward

Important!!  
**Remeber to compile the C++ code with `-g` debug option**

Tested POD, union, stl, std::string, Enum and Class with virtual inheritance

C-style strings (char[] and const char *) are treated as strings, if you are using them as buffers, you need to change the handling for these types  

# usage
You need to load the script by CLI `-x` option, e.g., `gdb -x dump_obj.py test/test1`, or use source command in GDB, `source dump_obj.py`   
Then you can use it in the same way as the `print` command. `dump-obj {variable name}`, this will print out the JSON representation of the object  

Alternatively, you can create a `driver_func()` similar to the one in dump_obj.py to set up the debugging context  
then run gdb: `gdb -x dump_obj.py` to automatic the process, you can also use the gdb command text file to achieve the same automation  

# Example
C++ code
```
class Global_data {};
Global_data g_data;
class MyData {
    enum Day_t {
        Mon, Tue, Wed, Thu, Fri, Sat, Sun
    };
    struct Nested_t
    {
        int nested_int = 2;
    };

    int i_data = 1;
    float f_data = 3.14;
    char* p = nullptr;
    const char* str = "const string";
    Nested_t nested;
    Day_t day_enum[2] = {Mon, Sat};
    int* i_ptr = &nested.nested_int;
    Global_data* g_ptr = &g_data;
    Nested_t* member_ptr = &nested;
};

MyDataClass obj;
```

This will generate the following JSON string (formatted externally)
```
{
  "i_data(int)": 1,
  "f_data(float)": 3.1400001,
  "p(char *)": "((nullptr))",
  "str(const char *)": "const string",
  "nested(MyData::Nested_t)": {
    "nested_int(int)": 2
  },
  "day_enum(enum MyData::Day_t [2])": [
    "MyData::Mon",
    "MyData::Sat"
  ],
  "i_ptr(int *)": "2(int) @ 0x7fffffffdfe8",
  "g_ptr(Global_data *)": "g_data(Global_data) @ 0x555555558011",
  "member_ptr(MyData::Nested_t *)": "anonymous(MyData::Nested_t) @ 0x7fffffffdfe8"
}
```

# Ref
https://sourceware.org/gdb/current/onlinedocs/gdb.html/Types-In-Python.html  
https://sourceware.org/gdb/current/onlinedocs/gdb.html/Values-From-Inferior.html


# Contact
<kyle0923@qq.com>
