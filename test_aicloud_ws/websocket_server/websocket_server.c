/*
 * Copyright (c) 2014 Cesanta Software Limited
 * All rights reserved
 */
#include <string.h>
#include <stdio.h>

#include "cJSON.h"
#include "mongoose.h"

#define FLAGS_MASK_OP 0x0f
static sig_atomic_t s_signal_received = 0;
static struct mg_serve_http_opts s_http_server_opts;

#if MG_ENABLE_SSL
static const char *s_http_port = "8443";
static const char *s_ssl_cert = "server.pem";
static const char *s_ssl_key = "server.key";
#else
static const char *s_http_port = "8000";
#endif

static void signal_handler(int sig_num) {
  signal(sig_num, signal_handler);  // Reinstantiate signal handler
  s_signal_received = sig_num;
}

static int is_websocket(const struct mg_connection *nc) {
  return nc->flags & MG_F_IS_WEBSOCKET;
}

static void broadcast(struct mg_connection *nc, const struct mg_str msg) {
  struct mg_connection *c;
  char buf[500];
  char addr[32];
  mg_sock_addr_to_str(&nc->sa, addr, sizeof(addr),
                      MG_SOCK_STRINGIFY_IP | MG_SOCK_STRINGIFY_PORT);

  snprintf(buf, sizeof(buf), "%s %.*s", addr, (int) msg.len, msg.p);
  printf("%s\n", buf); /* Local echo. */
  for (c = mg_next(nc->mgr, NULL); c != NULL; c = mg_next(nc->mgr, c)) {
    if (c == nc) continue; /* Don't send to the sender. */
    mg_send_websocket_frame(c, WEBSOCKET_OP_TEXT, buf, strlen(buf));
  }
}

static void mg_server_error(struct mg_connection *nc)
{
  char *buf = "{\"code\":404, \"msg\": \"websocket recieve invalid frame, please check\"}";
  mg_send_websocket_frame(nc, WEBSOCKET_OP_TEXT, buf, strlen(buf));  
}

static void mg_server_replay(struct mg_connection *nc, const struct mg_str msg)
{
    FILE *fp = NULL;
    cJSON *root = cJSON_Parse(msg.p);
    if(!root){
      printf("Could not parse websocket frame to json\n");
      mg_server_error(nc);
      return;
    }
    
    cJSON *topic = cJSON_GetObjectItem(root, "topic");
    if(!topic){
      printf("Could not get topic\n");
      goto err;
    }

    if(!strcasecmp(topic->valuestring, "cloud.ota.status")){
      cJSON *param = cJSON_GetObjectItem(root, "params");
      if(!param){
        param = cJSON_GetObjectItem(root, "data");
        if(!param){
          printf("Could not get parameter\n");
          goto err;
        }
      }
      cJSON *otaStatus = cJSON_GetObjectItem(param, "otaStatus");
      if(!otaStatus){
        goto err;
      }
      if(!strcasecmp(otaStatus->valuestring, "willUpgrade")){
          fp = fopen("cloud.ota.upgrade", "r");
      }
    }
    else {
      fp = fopen(topic->valuestring, "r");
    }
    
    if(fp == NULL){
        printf("Could not get topic reply file\n");
        goto err;
    }
    /* read reply message from file and send to websocket client */
    fseek(fp, 0, SEEK_END);
    long f_size = ftell(fp);
    char *text = (char *)malloc(f_size + 1);
    if(!text){
      goto err;
    }
    rewind(fp);

    fread(text, sizeof(char), f_size, fp);
    text[f_size] = '\0';

    mg_send_websocket_frame(nc, WEBSOCKET_OP_TEXT, text, strlen(text));
    free(text);
    goto out;
err:
    mg_server_error(nc);
out:
    cJSON_Delete(root);
	if(fp){
		fclose(fp);
	}
    return;
}

static void ev_handler(struct mg_connection *nc, int ev, void *ev_data) {
  switch (ev) {
    case MG_EV_WEBSOCKET_HANDSHAKE_DONE: {
      /* New websocket connection. Tell everybody. */
      broadcast(nc, mg_mk_str("++ joined"));
      break;
    }
    case MG_EV_WEBSOCKET_FRAME: {
      struct websocket_message *wm = (struct websocket_message *) ev_data;
      /* New websocket message. Tell everybody. */
      switch (wm->flags & FLAGS_MASK_OP){
        case WEBSOCKET_OP_TEXT:{
          struct mg_str d = {(char *) wm->data, wm->size};
          printf("recieve>\n%s\n", d.p);
          broadcast(nc, d);
          mg_server_replay(nc, d);
          break;
        }
        case WEBSOCKET_OP_PING:{
          mg_send_websocket_frame(nc, WEBSOCKET_OP_PONG, wm->data, wm->size);
          break;
        }
        default: {
          printf("not support websocket frame\n");
          break;
        }
      }
      break;
    }
    case MG_EV_HTTP_REQUEST: {
      mg_serve_http(nc, (struct http_message *) ev_data, s_http_server_opts);
      break;
    }
    case MG_EV_CLOSE: {
      /* Disconnect. Tell everybody. */
      if (is_websocket(nc)) {
        broadcast(nc, mg_mk_str("-- left"));
      }
      break;
    }
  }
}

int main(void) {
  struct mg_mgr mgr;
  struct mg_connection *nc;
  struct mg_bind_opts bind_opts;
  const char *err;

  signal(SIGTERM, signal_handler);
  signal(SIGINT, signal_handler);
  setvbuf(stdout, NULL, _IOLBF, 0);
  setvbuf(stderr, NULL, _IOLBF, 0);

  mg_mgr_init(&mgr, NULL);

  memset(&bind_opts, 0, sizeof(bind_opts));

#if MG_ENABLE_SSL
  bind_opts.ssl_cert = s_ssl_cert;
  bind_opts.ssl_key = s_ssl_key;
  printf("Starting SSL server on port %s, cert from %s, key from %s\n",
         s_http_port, bind_opts.ssl_cert, bind_opts.ssl_key);
#endif
  bind_opts.error_string = &err;


  nc = mg_bind_opt(&mgr, s_http_port, ev_handler, bind_opts);
  if (nc == NULL) {
    printf("Failed to create listener: %s\n", err);
    return 1;
  }

  mg_set_protocol_http_websocket(nc);
  s_http_server_opts.document_root = ".";  // Serve current directory
  s_http_server_opts.enable_directory_listing = "yes";

  printf("Started on port %s\n", s_http_port);
  while (s_signal_received == 0) {
    mg_mgr_poll(&mgr, 200);
  }
  mg_mgr_free(&mgr);

  return 0;
}
