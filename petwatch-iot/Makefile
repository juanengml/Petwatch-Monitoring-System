# Variáveis
IMAGE_NAME = petwatch-iot:latest
CAMERA = 0

# Comandos
build:
	docker build -t $(IMAGE_NAME) .

run:
	docker run --rm  -p 3030:3030 -e CAMERA=$(CAMERA) -v /home/juannascimento/Petwatch-Monitoring-System/petwatch-iot/output:/app/output $(IMAGE_NAME)

purge:
	docker stop $(IMAGE_NAME) || true
	docker rm $(IMAGE_NAME) || true
	docker rmi $(IMAGE_NAME) || true

.PHONY: build run purge
