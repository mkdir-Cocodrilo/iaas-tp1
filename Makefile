build-image:
	docker build -t youtube-api-job .

build-container:
	docker run -d -p 8080:8080 youtube-api-job