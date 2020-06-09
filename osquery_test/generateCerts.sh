#!/bin/bash
 openssl req -x509 \
   -newkey rsa:4096 \
   -nodes \
   -out cert.pem \
   -keyout key.pem \
   -days 365 \
   -subj "/C=US/ST=Colorado/L=Boulder/O=sm1te/OU=Org/CN=127.0.0.1"
