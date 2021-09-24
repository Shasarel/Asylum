build: build-web build-cron

build-web:
	docker build --tag asylum_web -f web.dockerfile .

build-cron:
	docker build --tag asylum_cron -f cron.dockerfile .
