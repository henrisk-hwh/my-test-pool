all: clean test

test: kfifo.c main.c
	gcc $^ -I. -o $@
	
clean:
	rm -rf test