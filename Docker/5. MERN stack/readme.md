# MERN Stack Application

## Overview
This project demonstrates a simple **MERN stack** setup using Docker Compose, which includes:

- **MongoDB** as the database
- **Express.js** as the backend framework
- **React** as the frontend application
- **Node.js** as the runtime environment
- **Mongo Express** as a web UI for MongoDB management

---

## Stack Architecture

```
frontend (React) --> backend (Express.js + Node.js) --> MongoDB
                                         ↳ mongo-express (DB GUI)
```

---

## Docker Compose Configuration

### docker-compose.yml

```yaml
services:
  mongodb: 
    image: mongo:4.4
    ports:
      - 27017:27017
    restart: always
    environment:
       MONGO_INITDB_ROOT_USERNAME: ${MONGO_INITDB_ROOT_USERNAME}
       MONGO_INITDB_ROOT_PASSWORD: ${MONGO_INITDB_ROOT_PASSWORD}

  backend:
    build: ./backend
    ports:
      - 5000:5000
    environment:
      - MONGO_URI=mongodb://${MONGO_INITDB_ROOT_USERNAME}:${MONGO_INITDB_ROOT_PASSWORD}@mongodb:27017/?authSource=admin
    depends_on:
      - mongodb

  frontend:
    build: ./frontend
    ports:
      - 3000:3000
    depends_on:
      - backend

  mongo_express:
    image: mongo-express
    ports:
      - 8081:8081
    environment:
      - ME_CONFIG_MONGODB_PORT=27017
      - ME_CONFIG_MONGODB_SERVER=mongodb
      - ME_CONFIG_MONGODB_ADMINUSERNAME=${MONGO_INITDB_ROOT_USERNAME}
      - ME_CONFIG_MONGODB_ADMINPASSWORD=${MONGO_INITDB_ROOT_PASSWORD}
    depends_on:
      - mongodb
```

---

## Frontend Dockerfile (React)

```dockerfile
FROM node:18

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

RUN npm run build

RUN npm install -g serve

EXPOSE 3000

CMD ["serve", "-s", "build", "-l", "3000"]
```

---

## Backend Dockerfile (Express.js)

```dockerfile
FROM node

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 5000

CMD ["node", "app.js"]
```

---

## Usage

### 1. Create a `.env` file:

```
MONGO_INITDB_ROOT_USERNAME=root
MONGO_INITDB_ROOT_PASSWORD=supersecret123!
```

### 2. Build and start the containers:

```bash
docker compose up --build -d
```

### 3. Access the services:

- **Frontend (React):** [http://localhost:3000](http://localhost:3000)
- **Backend (Express):** [http://localhost:5000](http://localhost:5000)
- **Mongo Express:** [http://localhost:8081](http://localhost:8081)

---

## Notes

- The React frontend connects to the Express backend via `http://backend:5000` inside the Docker network.
- Mongo Express allows you to visually inspect your MongoDB collections.
- You can modify the ports or credentials in `.env` if needed.

---

## Stop & Cleanup

```bash
docker compose down -v
```

---
