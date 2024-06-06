all: cache
	docker build -f Dockerfile.build -t nllb-api .
	docker run --rm -v ./cache:/home/user/.cache -e APP_PORT=7860 -p 7860:7860 nllb-api

gpu: cache
	docker build -f Dockerfile.cuda-build -t nllb-api .
	docker run --rm --gpus all -e APP_PORT=7860 -p 7860:7860 -v ./cache:/home/user/.cache nllb-api

hf: cache
	docker build -t nllb-api .
	docker run --rm -v ./cache:/home/user/.cache -p 7860:7860 nllb-api

cache:
	mkdir cache
	chmod 775 cache
