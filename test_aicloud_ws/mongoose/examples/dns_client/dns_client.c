/*
 * Copyright (c) 2014 Cesanta Software Limited
 * All rights reserved
 */

/*
 * Try it out with:
 * $ dig -t A www.google.com -4 @localhost -p 5533
 */

#include "../../mongoose.h"

#include <stdio.h>

static int s_exit_flag = 0;

static void resolve_cb(struct mg_dns_message *msg, void *data,
                       enum mg_resolve_err e) {
  int i;
  //size_t j;
  (void)data;
  //printf("msg: %p e: %d\n", msg, e);
  switch(e) {
    case MG_RESOLVE_OK:
      printf("resolve ok\n");
      break;
    case MG_RESOLVE_EXCEEDED_RETRY_COUNT:
      printf("retry end\n");
      break;
    case MG_RESOLVE_TIMEOUT:
      printf("timeout\n");
      break;
    case MG_RESOLVE_NO_ANSWERS:
      printf("no answers\n");
      break;
    }
  if (e == MG_RESOLVE_OK && msg != NULL) {
    /*
     * Take the first DNS A answer and run...
     */
    for (i = 0; i < msg->num_answers; i++) {
      printf("rtype: %d\n", msg->answers[i].rtype);
      if (msg->answers[i].rtype == MG_DNS_A_RECORD) {
        struct sockaddr_in sa;
        mg_dns_parse_record_data(msg, &msg->answers[i], &sa.sin_addr, 4);
        printf("IPv4地址:%s, ttl: %d\n", inet_ntoa(sa.sin_addr), msg->answers[i].ttl);
      }
    }
  }

  s_exit_flag = 1;
}

int main(int argc, char *argv[]) {
  struct mg_mgr mgr;

  if (argc  < 2) {
    printf("args error: %s [dns-server-addr] [target-addr]\n", argv[0]);
    return 0;
  }
  /*
  char buf[1024];
  mg_resolve(argv[2], buf, 1024);
  printf("IPv4地址:%s \n", buf);
  return -1;
  */
  mg_mgr_init(&mgr, NULL);
  struct mg_resolve_async_opts o;
  memset(&o, 0, sizeof(o));
  o.nameserver = argv[1];
  o.timeout = 5;
  o.max_retries = 10;
  mg_resolve_async_opt(&mgr, argv[2], MG_DNS_A_RECORD, resolve_cb, NULL, o);

  while (s_exit_flag == 0) {
    //printf("poll\n");
    mg_mgr_poll(&mgr, 1000);
  }
  mg_mgr_free(&mgr);

  return 0;
}
