all: cache
	docker build -f Dockerfile.build -t nllb-api .
	docker run --rm -v ./cache:/home/user/.cache -e APP_PORT=7860 -p 7860:7860 nllb-api

cache:
	mkdir cache
	chmod 775 cache
