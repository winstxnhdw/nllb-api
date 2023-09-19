FROM ghcr.io/winstxnhdw/nllb-api:main

ENV SERVER_PORT 5000
ENV BACKEND_INTERNAL_URL http://localhost:5000
ENV BACKEND_URL http://localhost:7860

EXPOSE 7860
