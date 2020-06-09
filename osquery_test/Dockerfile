FROM dactiv/osquery:4.3.0-ubuntu20.04
COPY ./key.pem /home/root/key.pem
COPY ./cert.pem /home/root/cert.pem
CMD osqueryd --tls_hostname localhost:5000 --tls_client_cert=cert.pem --enroll_secret_env c2e8f53d-63b9-4836 --config_plugin=tls