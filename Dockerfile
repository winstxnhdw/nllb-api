FROM ghcr.io/winstxnhdw/nllb-api:main

ENV SERVER_PORT 7860
ENV HUGGINGFACE_HUB_CACHE /cache

RUN mkdir /cache
RUN chmod 777 /cache
