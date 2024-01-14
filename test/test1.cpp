#include <string>
#include <vector>
#include <map>
#include <set>
#include <utility>

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
    union Num_t {
        int int_val;
        float f_val;
    };

    Day_t dd[2] = {Day_t::Sat, Day_t::Wed};
    MyDataClass data[2];
    int der_value = 20;
    int list[3] = {1,2,3};
    std::string a_str = "value0";
    std::string my_str[4] = {"value1", "value2", "value3", "value4"};
    char* p = nullptr;
    const char char_arr[12] = {'s', 't', 'r', 'i', 'n', 'g', ' ', 'c', 'o', 'n', 's', 't'};
    const char* str = "string const";
    Num_t num_union = {.int_val = 1};
    std::pair<int, float> pair_val = {0, 3.1415};
    std::vector<int> vec = {1,2,3};
    std::map<std::string, float> m = { {"1", 1.1}, {"2", 2.2}, {"3",3.3}};
    std::set<Day_t> s = {Day_t::Mon, Day_t::Sat, Day_t::Thurs};
};

void anchor() {
    // as an anchor point for gdb break point
}

int main() {
    MyDerivedClass obj;
    anchor();
    return 0;
}


