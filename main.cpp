#include <iostream>
#include <typeinfo>
#include <cxxabi.h>
#include <string>

class MyDataClass {
    enum Month_t {
        Jan, Feb, Mar, Apr, May, Jun, Jul, Aug
    };
    int i_data = 1;
    float f_data = 3.14;
    Month_t mm[3] = {Jan, Feb, Aug};
};

class MyBaseClass {
public:
    int value = 10;
    virtual ~MyBaseClass() {} // Make the base class polymorphic
};

class MyDerivedClass : public MyBaseClass {
    enum class Day_t {
        Mon,
        Tue,
        Wed,
        Thurs,
        Fri,
        Sat,
        Sun
    };

    Day_t dd[2] = {Day_t::Sat, Day_t::Wed};
    MyDataClass data[2];
    int der_value = 20;
    int list[3] = {1,2,3};
    std::string my_str[4] = {"value1", "value2", "value3", "value4"};
    char* p = nullptr;
};

void anchor() {
    // as an anchor point for gdb break point
}

int main() {
    MyDerivedClass obj;
    // MyBaseClass* basePtr = new MyDerivedClass();

    // // Using typeid to get information about the type
    // const std::type_info& typeInfo = typeid(*basePtr);

    // // Demangling the type information
    // int status;
    // char* demangledName = abi::__cxa_demangle(typeInfo.name(), nullptr, nullptr, &status);

    // if (status == 0) {
    //     std::cout << "Demangled Type: " << demangledName << std::endl;
    //     free(demangledName);  // Remember to free the allocated memory
    // } else {
    //     std::cerr << "Demangling failed!" << std::endl;
    // }

    // // Don't forget to delete the allocated object
    // delete basePtr;

    anchor();
    return 0;
}


