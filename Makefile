export IMAGE_NAME=freundallein/autocomplete:latest

init:
	git config core.hooksPath .githooks
activate:
	/bin/bash -c "source .env/bin/activate"
run:
	python app.py
test:
	echo "Test
dockerbuild:
	docker build -t $$IMAGE_NAME -f Dockerfile .
distribute:
	echo "$$DOCKER_PASSWORD" | docker login -u "$$DOCKER_USERNAME" --password-stdin
	docker build -t $$IMAGE_NAME .
	docker push $$IMAGE_NAME