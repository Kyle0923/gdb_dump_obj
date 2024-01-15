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

void anchor() {
    // as an anchor point for gdb break point
}

int main() {
    MyData obj;
    anchor();
    return 0;
}


