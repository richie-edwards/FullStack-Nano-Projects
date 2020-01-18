# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## API Reference

### Getting Started
Base URL: This application is currently not hosted and can only be run locally.
Authentication: This version of the application does not require authentication.

### Error Handling
Error are returned as JSON objects in the following format:
```
{
    "success": False,
    "error": 404,
    "message": "not found"
}
```

The API will return the following request error types:

- 400: Bad Request
- 404: Resource Not Found
- 405: Method Not Allowed
- 422: Unprocessable Entity

### Endpoints
- GET /categories
- GET /questions
- DELETE /questions/{int:question_id}
- POST /questions
- POST /questions/search_results
- GET /categories/{int:category_id}/questions
- POST /quizzes

#### GET /categories
- General:
- - Returns categories object and success value
- Sample: ```curl http://127.0.0.1:5000/categories```
```
{ 
    "categories":{ 
        "1":"Science",
        "2":"Art",
        "3":"Geography",
        "4":"History",
        "5":"Entertainment",
        "6":"Sports"
    },
    "success":true
}
```

#### GET /questions
- General:
    - Returns a list of questions, number of total questions, current category, categories. success value
- Sample: ```curl http://127.0.0.1:5000/questions```
```
{ 
    "categories":{ 
        "1":"Science",
        "2":"Art",
        "3":"Geography",
        "4":"History",
        "5":"Entertainment",
        "6":"Sports"
    },
    "current_category":"hard coded category",
    "questions":[ 
        { 
            "answer":"Apollo 13",
            "category":5,
            "difficulty":4,
            "id":2,
            "question":"What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        { 
            "answer":"Tom Cruise",
            "category":5,
            "difficulty":4,
            "id":4,
            "question":"What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
        { 
            "answer":"Maya Angelou",
            "category":4,
            "difficulty":2,
            "id":5,
            "question":"Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        { 
            "answer":"Edward Scissorhands",
            "category":5,
            "difficulty":3,
            "id":6,
            "question":"What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        },
        { 
            "answer":"Muhammad Ali",
            "category":4,
            "difficulty":1,
            "id":9,
            "question":"What boxer's original name is Cassius Clay?"
        },
        { 
            "answer":"Brazil",
            "category":6,
            "difficulty":3,
            "id":10,
            "question":"Which is the only team to play in every soccer World Cup tournament?"
        },
        { 
            "answer":"Uruguay",
            "category":6,
            "difficulty":4,
            "id":11,
            "question":"Which country won the first ever soccer World Cup in 1930?"
        },
        { 
            "answer":"George Washington Carver",
            "category":4,
            "difficulty":2,
            "id":12,
            "question":"Who invented Peanut Butter?"
        },
        { 
            "answer":"Lake Victoria",
            "category":3,
            "difficulty":2,
            "id":13,
            "question":"What is the largest lake in Africa?"
        },
        { 
            "answer":"Agra",
            "category":3,
            "difficulty":2,
            "id":15,
            "question":"The Taj Mahal is located in which Indian city?"
        }
    ],
    "success":true,
    "total_questions":19
}
```

#### DELETE /questions/{int:question_id}
- General:
    - Deletes the question that is of the ID provided in the request.
    - Returns the ID of the delete question, a list of questions based on page (10 items per page), number of total questions and success value.
- Sample: ```curl -X DELETE http://127.0.0.1:5000/questions/13```
```
{     
    "deleted": 13,
    "questions":[ 
        { 
            "answer":"Apollo 13",
            "category":5,
            "difficulty":4,
            "id":2,
            "question":"What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        { 
            "answer":"Tom Cruise",
            "category":5,
            "difficulty":4,
            "id":4,
            "question":"What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
        { 
            "answer":"Maya Angelou",
            "category":4,
            "difficulty":2,
            "id":5,
            "question":"Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        { 
            "answer":"Edward Scissorhands",
            "category":5,
            "difficulty":3,
            "id":6,
            "question":"What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        },
        { 
            "answer":"Muhammad Ali",
            "category":4,
            "difficulty":1,
            "id":9,
            "question":"What boxer's original name is Cassius Clay?"
        },
        { 
            "answer":"Brazil",
            "category":6,
            "difficulty":3,
            "id":10,
            "question":"Which is the only team to play in every soccer World Cup tournament?"
        },
        { 
            "answer":"Uruguay",
            "category":6,
            "difficulty":4,
            "id":11,
            "question":"Which country won the first ever soccer World Cup in 1930?"
        },
        { 
            "answer":"George Washington Carver",
            "category":4,
            "difficulty":2,
            "id":12,
            "question":"Who invented Peanut Butter?"
        },       
        { 
            "answer":"Agra",
            "category":3,
            "difficulty":2,
            "id":15,
            "question":"The Taj Mahal is located in which Indian city?"
        }
    ],
    "success":true,
    "total_questions":18
}
```

#### POST /questions
- General:
    - Creates a new question.
    - Returns a list of questions, number of total questions, current category, categories. success value
- Sample: ```curl -X POST http://127.0.0.1:5000/questions -H "Content-Type: application/json" -d '{"question":"test question?","answer":"test answer", "category":1, "difficulty":3}'```

```
{
    "question":"test question?",
    "success":true
}
```

#### POST /questions/search_results
- General:
    - Returns questions that contain the given search term.
    - Returns a list of questions, number of total questions that match, current category and success value.
- Sample: ```curl -X POST http://127.0.0.1:5000/questions/search_results -H "Content-Type: application/json" -d '{"searchTerm":"soccer"}'```

```
{ 
    "current_category":"",
    "questions":[ 
        { 
            "answer":"Brazil",
            "category":6,
            "difficulty":3,
            "id":10,
            "question":"Which is the only team to play in every soccer World Cup tournament?"
        },
        { 
            "answer":"Uruguay",
            "category":6,
            "difficulty":4,
            "id":11,
            "question":"Which country won the first ever soccer World Cup in 1930?"
        }
    ],
    "success":true,
    "total_questions":2
}
```

#### GET /categories/{int:category_id}/questions
- General:
    - Returns a list of questions (answer, category, difficulty, id, question) and success value.
- Sample: ```curl http://127.0.0.1:5000/categories/3/questions```
```
{ 
    "questions":[ 
        { 
            "answer":"Agra",
            "category":3,
            "difficulty":2,
            "id":15,
            "question":"The Taj Mahal is located in which Indian city?"
        },
        { 
            "answer":"Haiti",
            "category":3,
            "difficulty":3,
            "id":26,
            "question":"What country shares the island with Dominican Republic?"
        }
    ],
    "success":true
}
```

#### POST /quizzes
- General:
    - Gets questions to play the quiz. This endpoint takes category and previous question parameters and returns a random questions within the given category, if provided, that is not one of the previous questions.
- Sample: ```curl -X POST http://127.0.0.1:5000/quizzes -H "Content-Type: application/json" -d '{"previous_questions":[],"quiz_category":{"type":"Science","id":"1"}}'```
```
{ 
    "question":{ 
        "answer":"Blood",
        "category":1,
        "difficulty":4,
        "id":22,
        "question":"Hematology is a branch of medicine involving the study of what?"
    },
    "success":true
}
```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```