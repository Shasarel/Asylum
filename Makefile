APP_NAME := asylum_web
VERSION := 1

build:
	docker build --tag $(APP_NAME):$(VERSION) .

