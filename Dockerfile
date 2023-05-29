FROM ghcr.io/winstxnhdw/nllb-api:main

ENV SERVER_PORT 7860
ENV TRANSFORMERS_CACHE /cache

RUN mkdir /cache
RUN chmod 777 /cache
