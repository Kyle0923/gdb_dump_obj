
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

void anchor() {
    // as an anchor point for gdb break point
}

int main() {
    MyData obj;
    anchor();
    return 0;
}


