# GDB dump-obj extension
A GDB-Python script that converts the C/C++ object specified by obj_name to a Python dictionary object which allows for json print out or other processing afterward

Important!!  
**Remeber to compile the C++ code with `-g` debug option**

Tested POD, union, stl, std::string, Enum and Class with virtual inheritance

C-style strings (char[] and const char *) are not well formatted, but given my usecase rarely use these two as strings and char[] are often used as a memory buffer instead, I am leaving them as is  

STL containers could also use more handlings, but again, my usage is mostly on POD, so I am leaving the STLs to the GDB printer function

# usage
update the `driver_func()` in dump_obj.py to set up the debugging context  
then run gdb: `gdb -q -ex "source dump_obj.py"`

# Example
C++ code
```
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
    Nested_t nested;
    Day_t day[2] = {Mon, Sat};
};

MyDataClass obj;
```

This will generate the following JSON string (formatted externally)
```
{
  "i_data(int)": "1",
  "f_data(float)": "3.1400001",
  "p(char *)": "0x0",
  "nested(MyData::Nested_t)": {
    "nested_int(int)": "2"
  },
  "day(MyData::Day_t [2])": [
    "MyData::Mon",
    "MyData::Sat"
  ]
}
```

# Ref
https://sourceware.org/gdb/current/onlinedocs/gdb.html/Types-In-Python.html  
https://sourceware.org/gdb/current/onlinedocs/gdb.html/Values-From-Inferior.html


# Contact
<kyle0923@qq.com>