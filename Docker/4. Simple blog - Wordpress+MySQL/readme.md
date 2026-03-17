# wordpress-mysql-phpmyadmin  
Dockerized WordPress + MySQL + phpMyAdmin stack


## Environment setup

Create a `.env` file in the root directory:

```bash
MYSQL_ROOT_PASSWORD=root123
MYSQL_DATABASE=wordpress_db
MYSQL_USER=wp_user
MYSQL_PASSWORD=wp_pass123
```
or use
```bash
EXPORT $variable_name=value
```

## Start the services

```bash
docker compose up -d --build
```

This will start:
- **WordPress** on [http://localhost:8080](http://localhost:8080)
- **phpMyAdmin** on [http://localhost:8081](http://localhost:8081)
- **MySQL** database accessible internally at `mysql:3306`

## Default credentials

| Service       | Username   | Password     | Notes |
|----------------|------------|--------------|--------|
| WordPress DB   | `wp_user`  | `wp_pass123` | As defined in `.env` |
| MySQL Root     | `root`     | `root123`    | As defined in `.env` |
| phpMyAdmin     | Use DB creds | — | Login with `wp_user` / `wp_pass123` |

## Accessing phpMyAdmin

Open [http://localhost:8081](http://localhost:8081)  
and log in using:
```
Server: mysql
Username: wp_user
Password: wp_pass123
```

## Stopping and cleaning up

Stop all running containers:

```bash
docker compose down
```

Remove containers and volumes (⚠️ deletes database data):

```bash
docker compose down -v
```

## Directory structure

```
wordpress-mysql-phpmyadmin/
├── docker-compose.yml
├── .env
└── README.md
```
---

✅ **After setup:**  
1. Visit [http://localhost:8080](http://localhost:8080)  
2. Complete WordPress installation (choose a site name, admin user, etc.)  
3. Log in and enjoy your Dockerized WordPress environment 🎉
