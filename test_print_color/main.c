#include <stdio.h>
#include <string.h>

static char *lvl_color[] = {
    "\033[0;32;31m",    //'F'
    "\033[1;31m",  //'A'
    "\033[1;33m",  //'C'
    "\033[1;33m",  //'E'
    "\033[1;34m",  //'W'
    "\033[0;35m",  //'N'
    "\033[1;36m",  //'I'
    "\033[0;37m",  //'D'
};

#define COLOR_START(l) lvl_color[l]
#define COLOR_END "\033[0m"

int main() {
    const char *p = NULL;
    int len = strlen(NULL);
    printf("-- %d\n", len);
    int color_size = sizeof(lvl_color) / sizeof(char *);
    for(int i = 0; i < color_size; i++) {
        printf("%stest%s\n", COLOR_START(i), COLOR_END);
    }

    return 0;
}
