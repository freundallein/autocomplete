export IMAGE_NAME=freundallein/autocomplete:latest

init:
	git config core.hooksPath .githooks
run:
	python app.py
test:
	pytest -m "not slow"
test-full:
	pytest
dockerbuild:
	docker build -t $$IMAGE_NAME -f Dockerfile .
distribute:
	echo "$$DOCKER_PASSWORD" | docker login -u "$$DOCKER_USERNAME" --password-stdin
	docker build -t $$IMAGE_NAME .
	docker push $$IMAGE_NAME