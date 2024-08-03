# Appstore Project

## Prerequisite

- Support of `Make` file to run instruction commands.

## Run Project

```shell
cd to/projct/directory

# Create docker network.
docker network create appstore_network

# Create env files using their templates.
make copy_env_files

# Adjust env variables with appropriate values - using an editor like vim.
vim ./envs/app.env
vim ./envs/db.env
vim ./.env

# To build and up docker images:
make run
# or in case for detached mode, run following:
make run_detach

# For more information and examples:
make help
```

## Run Unit-Tests

```shell
make tests_all v=2
```

## More Information

```shell
make help
```

## Documents

- [Github Repository](https://github.com/ykh/appstore)
- [Project Structure]()
- [Project Management Board - Trello](https://trello.com/b/1qFsjJK5/appstore)
- [API Doc - Postman](https://www.postman.com/develozerg/workspace/appstore-api/collection/2184809-f72fca16-b1ec-4e08-bba6-d59745b27aeb?action=share&creator=2184809)
- [Dashboard Service Design]()
