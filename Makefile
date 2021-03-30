.PHONY: clean

up:
	docker-compose up

clean:
	docker-compose rm -f 
	rm -rf directus
	rm -rf umbrella/db
	rm -rf umbrella/log