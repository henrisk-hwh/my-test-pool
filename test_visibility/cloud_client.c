
extern int foo_internal();
extern int bar_internal();
__attribute__ ((visibility ("default"))) int foo() {
    return 43 + foo_internal();
}

__attribute__ ((visibility ("default"))) int bar() {
    return 34 + bar_internal();
}
