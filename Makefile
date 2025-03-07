all:
	docker build -f Dockerfile.build -t nllb-api .
	docker run --init --rm -e SERVER_PORT=7860 -e TRANSLATOR_THREADS=4 -p 7860:7860 nllb-api

gpu:
	docker build -f Dockerfile.cuda-build -t nllb-api .
	docker run --init --rm --gpus all -e SERVER_PORT=7860 -e TRANSLATOR_THREADS=4 -p 7860:7860 nllb-api

hf:
	docker build -t nllb-api .
	docker run --init --rm -p 7860:7860 nllb-api

stub:
	STUB_TRANSLATOR=True STUB_LANGUAGE_DETECTOR=True python main.py
