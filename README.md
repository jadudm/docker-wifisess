# docker-wifisess

## to launch

```
make up
```

The first time this is run, the database init seems to take too long, and directus gets impatient. I have no idea why it won't wait.

CTRL-C, and run it again. Should be fine.

This sets the username and password for directus to `admin@wifisess.gov`. This is assumed to only be used in a local config.

## to cleanup/reset

make clean

## to populate

## to run selenium to populate admin users in umbrella...

```
docker build -t 18f/selenium umbrella-setup
```

and to run

```
docker run --net host -v ${PWD}/umbrella-setup:/src 18f/selenium create_admin_user.py 192.168.1.146
```
