
# Bewise-test

### Setting environment:
```
nano .env  
```
```
DB_USER=db_user
DB_PASSWORD=db_password
DB_HOST=localhost
DB_NAME=db_name
```


### Build and run Docker containers
```
docker-compose build
docker-compose up
```


### Request example!
```
POST 0.0.0.0:8080/load_questions 
BODY: {
    "questions_num": 1
}
RESPONSE: {
    "status": "success",
    "data": [
        {
            "id": "139566",
            "answer": "Jefferson and Wilson",
            "question": "The 2 Thomases (one went by his middle name)",
            "category_id": "16132",
            "created_at": "2023-10-16 14:22:30.441844+00:00"
        }
    ]
}
```