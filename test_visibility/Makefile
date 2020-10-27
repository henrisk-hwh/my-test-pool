#CROSS = /home1/heweihong/workspace/R328-S1-FreeRTOS/lichee/rtos/tools/gcc-arm-melis-eabi-8-2019-q3-update/bin/arm-melis-eabi-
CC = $(CROSS)gcc
CXX = $(CROSS)g++
AR = $(CROSS)ar
LD = $(CROSS)ld
STRIP = $(CROSS)strip
OBJCOPY = $(CROSS)objcopy

FLAGS = -Wall

CLOUD = cloud_server
OBJ += cloud_server.o

LIB := libccloud.a
LIBSRC = cloud_client.c cloud_client_internal.c
LIBOBJ = cloud_client.o cloud_client_internal.o

all: $(LIB) $(CLOUD)

$(LIBOBJ):$(LIBSRC)
	$(CC) $(FLAGS) -c $(LIBSRC) -fvisibility=hidden

$(LIB):$(LIBOBJ)
	$(LD) -r $(LIBOBJ) -o liball.o
	$(STRIP) --strip-unneeded liball.o
	$(OBJCOPY) --localize-hidden liball.o liball_hidden.o
	$(AR) cq $@ liball_hidden.o


$(LIB)1:$(LIBOBJ)
	$(AR) cq $@ $^

$(CLOUD):$(OBJ)
	$(CC) $(OBJ) $(LIB) -o $@ $(FLAGS)

%.o:%.c %.h
	$(CC)   $^ -o $@  $(FLAGS)

.PHONY:clean

clean:
	 rm cloud_server *.o *.a -r
