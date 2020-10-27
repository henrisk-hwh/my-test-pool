#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "kfifo.h"

#define MAXSIZE 50000
int main(int argc, char* argv[]) {
	int i;
	char in[MAXSIZE];
	char out[MAXSIZE];
	struct kfifo fifo;
	kfifo_new(&fifo, MAXSIZE);
	
	for (int i = 0; i < sizeof(in); i++) {
		in[i] = i;
	}
	
	while(1) {
		int idx = 0;
		int len = 0;
		memset(out, 0, sizeof(out));
		len = kfifo_push(&fifo, in, sizeof(in));
		if(len != sizeof(in)) {
			printf("push len: %d\n", len);
			exit(0);
		}
		kfifo_pop(&fifo, out, sizeof(out));
		
		for (idx = 0; idx < sizeof(in); idx++) {
			if (in[idx] != out[idx]) {
				printf("in: %d, out: %d\n", in[idx], out[idx]);
				exit(0);
			}
		}
		
	}
	return 0;
}