# Social Networking Website/App Feed System

This is a web application built with Flask that implements a basic social networking feed system where users can interact with groups, create posts, like, and comment on posts.

## Overview
The application allows users to:
- Browse a feed/timeline of posts from groups they have joined.
- Post inside a group and browse this group's posts.
- Like a post.
- Comment on a post.

## Setup

### 1. Clone the repository
```bash
    git clone
```

### Important Note:
    1. Create .env file & add these variables in .env file in the root directory before running the server.
    
        db_uri="postgresql://postgres:postgres@flask_service_db_1:5432/social_db"
        secret_key="social_secret_key"
    
    2. Some of Below endpoints require authorization plesae add bearer token before hitting same. Create user doesn't asks for authenticaion.


### 2. Build and Run the Server with Docker
In the **flask_service** directory, you will find two files: **Dockerfile** and **docker-compose.yml**

#### Run below commands to build and run the server:
```bash
  docker-compose build
  docker-compose up
```
 ##### To run in daemon mode
    docker-compose up -d 


### 2. Database Setup
```bash
  # Search for Db Docker Container
  docker ps
  # Go inside db docker container
  docker exec -it <db_container_id> /bin/bash
  # Connect to db server
  psql -U postgres
  # List databases
  \l
  # create New Database
  create database social_db;
  # Connect to Database
  \c social_db
```


### create schema
```bash
  # Search for Db Docker Container
  docker ps
  # Go inside web docker container
  docker exec -it <web_container_id> /bin/bash
  # Connect to db server
  run python lib/model.py
```


## Accessing Endpoints

### Health Check Endpoint
To verify if the server is running, send a GET request to:
```bash
http://{{local_ip_address}}:8123/api/v1/health-check 
or
http://0.0.0.0:8123/api/v1/health-check
```

## Create Endpoints
```bash
  http://0.0.0.0:8123/api/v1/create
```

### 1. Create User
Include the following JSON payload in the request body:
```json
{
    "create_type": "user",
    "data": {
        "username": "binitkumar_4",
        "password": "12345678",
        "email": "binitkumar_4@gmail.com"
    }
}
```

#### Expected response:
```json
{
    "data": {
        "created_at": "Fri, 09 Aug 2024 19:24:36 GMT",
        "email": "binitkumar_4@gmail.com",
        "id": 5,
        "is_active": true,
        "password": "25d55ad283aa400af464c76d713c07ad",
        "soft_delete": false,
        "updated_at": "Fri, 09 Aug 2024 19:24:36 GMT",
        "username": "binitkumar_4"
    },
    "status": "success"
}
```

### 2. Create Group

```json
{
    "create_type": "group",
    "data": {
        "name": "Group 3"
    }
}
```

#### Expected response:
```json
{
    "data": {
        "created_at": "Fri, 09 Aug 2024 18:53:04 GMT",
        "id": 3,
        "name": "Group 3",
        "soft_delete": false,
        "updated_at": "Fri, 09 Aug 2024 18:53:04 GMT"
    },
    "status": "success"
}
```

### 2. Create Group Membership

```json
{
    "create_type": "group_membership",
    "data": {
        "c_user_id": 2,
        "group_id": 1
    }
}
```

#### Expected response:
```json
{
    "data": {
        "created_at": "Fri, 09 Aug 2024 19:43:27 GMT",
        "group_id": 1,
        "id": 7,
        "soft_delete": false,
        "updated_at": "Fri, 09 Aug 2024 19:43:27 GMT",
        "user_id": 4
    },
    "status": "success"
}
```


### 2. Create Post

```json
{
    "create_type": "post",
    "data": {
        "content": "Group 3: This content belongs to group 3.",
        "group_id": 3
    }
}
```

#### Expected response:
```json
{
    "data": {
        "comment_count": 0,
        "content": "Group 3: This content belongs to group 3.",
        "created_at": "Fri, 09 Aug 2024 18:53:23 GMT",
        "group_id": 3,
        "id": 4,
        "like_count": 0,
        "soft_delete": false,
        "timestamp": "Fri, 09 Aug 2024 18:53:23 GMT",
        "updated_at": "Fri, 09 Aug 2024 18:53:23 GMT",
        "user_id": 1
    },
    "status": "success"
}
```

## Search Endpoints
```bash
  http://0.0.0.0:8123/api/v1/search
```

### 1. Search Post

```json
{
    "search_type": "post",
    "filter_by": {},
    "limit": 10,
    "offset": 0
}
```

#### Expected response:
```json
{
    "data": [
        {
            "content": "Group 1: This content belongs to group 1.",
            "created_at": "Fri, 09 Aug 2024 12:22:54 GMT",
            "group_id": 1,
            "id": 2,
            "soft_delete": false,
            "timestamp": "Fri, 09 Aug 2024 12:22:54 GMT",
            "updated_at": "Fri, 09 Aug 2024 12:22:54 GMT",
            "user_id": 1
        },
        {
            "content": "Group 2: This content belongs to group 2.",
            "created_at": "Fri, 09 Aug 2024 12:23:30 GMT",
            "group_id": 2,
            "id": 3,
            "soft_delete": false,
            "timestamp": "Fri, 09 Aug 2024 12:23:30 GMT",
            "updated_at": "Fri, 09 Aug 2024 12:23:30 GMT",
            "user_id": 1
        },
        {
            "content": "Group 1: This content belongs to group 1.",
            "created_at": "Fri, 09 Aug 2024 12:06:56 GMT",
            "group_id": 1,
            "id": 1,
            "soft_delete": false,
            "timestamp": "Fri, 09 Aug 2024 12:06:56 GMT",
            "updated_at": "Fri, 09 Aug 2024 18:49:27 GMT",
            "user_id": 1
        }
    ],
    "meta": {
        "count": 3
    },
    "status": "success"
}
```

## Update Endpoints
```bash
  http://0.0.0.0:8123/api/v1/update
```

### 1. Like Post

```json
{
    "update_type": "like_post",
    "data": {
        "post_id": 1
    }
}
```

#### Expected response:
```json
{
    "data": {
        "comment_count": 0,
        "content": "Group 1: This content belongs to group 1.",
        "created_at": "Fri, 09 Aug 2024 12:22:54 GMT",
        "group_id": 1,
        "id": 2,
        "like_count": 1,
        "soft_delete": false,
        "timestamp": "Fri, 09 Aug 2024 12:22:54 GMT",
        "updated_at": "Fri, 09 Aug 2024 19:31:42 GMT",
        "user_id": 1
    },
    "status": "success"
}
```


### 1. Comment Post

```json
{
    "update_type": "comment_post",
    "data": {
        "content": "comment_2",
        "post_id": 1
    }
}
```

#### Expected response:
```json
{
    "data": {
        "content": "comment_2",
        "created_at": "Fri, 09 Aug 2024 18:49:27 GMT",
        "id": 2,
        "post_id": 1,
        "soft_delete": false,
        "timestamp": "Fri, 09 Aug 2024 18:49:27 GMT",
        "updated_at": "Fri, 09 Aug 2024 18:49:27 GMT",
        "user_id": 2
    },
    "status": "success"
}
```

