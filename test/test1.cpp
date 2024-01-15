#include <string>
#include <utility>
#include <vector>
#include <deque>
#include <forward_list>
#include <list>
#include <stack>
#include <queue>
#include <set>
#include <unordered_set>
#include <map>
#include <unordered_map>



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
    std::tuple<int, float, MyDataClass> tuple_val = {0, 3.1415, {}};

    std::array<int, 2> std_array = {1, 2};
    std::vector<int> vec = {1, 2, 3};
    std::deque<int> dque = {4, 5, 6};
    std::list<float> linklist = {-1.1, -2.2, -3.3};
    std::forward_list<float> forwd_linklist = {-1.1, -2.2, -3.3};

    std::stack<int> st = std::stack<int>(dque);
    std::queue<int> que = std::queue<int>(dque);
    std::priority_queue<int> pri_que = std::priority_queue<int>(dque.begin(), dque.end());

    std::set<int> std_set =               {2,2,1,3};
    std::multiset<int> m_set =            {2,2,1,3};
    std::unordered_set<int> u_set =       {2,2,1,3};
    std::unordered_multiset<int> um_set = {2,2,1,3};

    std::map<int, float> std_map =               { {1, 1.1}, {2, 2.2}, {1, 1.1} };
    std::multimap<int, float> m_map =            { {1, 1.1}, {2, 2.2}, {1, 1.1} };
    std::unordered_map<int, float> u_map =       { {1, 1.1}, {2, 2.2}, {1, 1.1} };
    std::unordered_multimap<int, float> um_map = { {1, 1.1}, {2, 2.2}, {1, 1.1} };
};

void anchor() {
    // as an anchor point for gdb break point
}

int main() {
    MyDerivedClass obj;
    anchor();
    return 0;
}


