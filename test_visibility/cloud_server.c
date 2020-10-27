#include <stdio.h>

int foo_internal() {
    return 10086;
}

extern int foo();
extern int bar();
int main(int argc, char* argv[]) {
    printf("foo: %d, bar: %d\n", foo(), bar());

    return 0;
}
