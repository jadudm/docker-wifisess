# docker-wifisess

To get started quickly:

```
make clean
```

for good measure. This wipes `directus` and `umbrella` local state, which is stored in the filesystem.

```
make up
```

This will run, and directus will bail. CTRL-C after the DB is finished doing its thing.

```
make up
```

This will run a second time; Postgres will be much quicker, and therefore Directus will happily bootstrap.

Now, to create the admin user for `umbrella`:

```
make firstrun
```

This builds a docker container with `selenium`, and runs it against the umbrella container. It creates an admin user with a password so that we can begin using the API to configure umbrella in a repeatable way.


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
docker run --net host -it -v ${PWD}/umbrella-setup:/src 18f/selenium create_admin_user.py localhost
```
