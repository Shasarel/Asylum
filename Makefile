build: build-web build-cron

build-web:
	podman build --tag asylum_web -f web.dockerfile .

build-cron:
	podman build --tag asylum_cron -f cron.dockerfile .
