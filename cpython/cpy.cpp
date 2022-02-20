#include <iostream>

using namespace std;

class Foo {
    public:
        void bar() {
            for(int i = 0; i <= 1000; i++) {
                cout << i << endl;
            }
        }
};

extern "C" {
    Foo* Foo_new(){ return new Foo(); }
    void Foo_bar(Foo* foo){ foo->bar(); }
}
