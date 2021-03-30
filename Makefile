.PHONY: clean umbrella

up:
	docker-compose up

firstrun:
	docker build -t 18f/selenium umbrella-setup
	docker run --net host -it -v ${PWD}/umbrella-setup:/src 18f/selenium create_admin_user.py localhost

clean:
	docker-compose rm -f 
	rm -rf directus
	rm -rf umbrella/db
	rm -rf umbrella/log

umbrella:
	rm -rf umbrella/db
	rm -rf umbrella/log
	mkdir -p umbrella/db umbrella/log
	docker run -it \
		-v ${PWD}/umbrella/db:/opt/api-umbrella/var/db \
		-v ${PWD}/umbrella/log:/opt/api-umbrella/var/log \
		-v ${PWD}/umbrella/config:/etc/api-umbrella \
		-p "80:80" \
		-p "443:443" \
		nrel/api-umbrella:0.15.1