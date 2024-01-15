#include <string>
#include <vector>
#include <list>
#include <map>
#include <set>
#include <utility>

class MyDataClass {
    int i_data[2] = {1, 2};
    float f_data = 3.14;
};

class MyBaseClass {
public:
    int base_value = 1;
    virtual ~MyBaseClass() {} // Make the base class polymorphic
};
MyBaseClass g_base_obj;

class MyBaseClass2 {
public:
    struct Nested_t
    {
        int nested_int = 3;
    };
    int base2_value = 2;
    Nested_t nested;

};

class MyDerivedClass : public MyBaseClass, public MyBaseClass2 {
    enum class Day_t {
        Mon,
        Tue,
        Wed,
        Thurs,
        Fri,
        Sat,
        Sun
    };
    union Num_t {
        int int_val;
        float f_val;
    };

    Day_t day_enum = Day_t::Fri;
    Day_t days[2] = {Day_t::Sat, Day_t::Wed};
    MyDataClass data;
    MyDataClass data_list[2];

    Num_t num_union = {.int_val = 1};

    int i_value = -20;
    unsigned int uint_value = 10;
    int list[3] = {1,2,3};

    float f_val = 3.3;
    double d_val = 3.3;

    int* null_int_ptr = nullptr;
    unsigned int* uint_ptr = &uint_value;
    MyBaseClass* b_ptr = &g_base_obj;
    MyDataClass* d_ptr = &data;

    std::string std_str = "C++ string";
    std::string str_array[4] = {"value1", "value2", "value3", "value4"};
    char* char_ptr = nullptr;
    const char char_arr[10] = {'n' ,'o', 't', ' ', 's', 't', 'r', 'i', 'n', 'g'};
    const char char_str[9] = "C string";
    const char* c_str = "C string";


    std::pair<int, float> pair_val = {0, 3.1415};
    std::vector<int> vec = {1, 2, 3};
    std::list<float> linklist = {-1.1, -2.2, -3.3};
    std::map<std::string, float> std_map = { {"1", 1.1}, {"2", 2.2}, {"3",3.3}};
    std::set<Day_t> std_set = {Day_t::Mon, Day_t::Sat, Day_t::Thurs};
};

void anchor() {
    // as an anchor point for gdb break point
}

int main() {
    MyDerivedClass obj;
    anchor();
    return 0;
}


