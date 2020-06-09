#!/bin/bash
osqueryd --verbose --ephemeral --disable_database \
  --tls_hostname 127.0.0.1:8080 \
  --tls_server_certs ./cert.pem \
  --config_plugin tls \
  --config_tls_endpoint /config \
  --logger_tls_endpoint /logger \
  --logger_plugin tls  \
  --enroll_tls_endpoint /enrollment \
  --enroll_secret_path ./enrollment_secret.txt