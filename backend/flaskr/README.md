API Reference

Getting Started

Base URL: At the moment, the app can only run loacally. The backend is hosted at the default http://127.0.0.1:5000/ which is also set as the proxy for the frontend configuration.

Error Handling

Errors were returned as JSON in the folowing format:

     (
            jsonify({"success": False, "error": 404, "message": "method not allowed"}),
            404,
        )

The API will return these error types when requests fail.

404 -Not Found
400 - Bad Request
422 - Unprocessible 

Endpoints
GET /categories

It fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category

Sample: curl http://127.0.0.1:5000/categories

{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}


GET /questions

It fetches a paginated set of questions, a total number of questions, all categories and current category string.

SAMPLE: curl http://127.0.0.1:5000/questions?page=2

{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}
(venv)
jonh@BREEZY MINGW64 ~/trivia/triviaapp/backend (main)
$ curl http://127.0.0.1:5000/questions?page=2
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "questions": [
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    },
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of
optical illusions?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "One",
      "category": 2,
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    },
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    },
    {
      "answer": "Scarab",
      "category": 4,
      "difficulty": 4,
      "id": 23,
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    }
  ],
  "success": true,
  "total_questions": 19
}

DELETE /questions/<int:question_id>

it deletes a specified question using the id of the question

SAMPLE: curl -X DELETE http://127.0.0.1:5000/questions/3

},
    'deleted':3,
    'success':True,
    'totaL_questions:18
    }

POST /questions

It sends a post request in order to add a new question

Sample: curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d "{'question':'what is your name', 'answer':'Abraham', 'category':'1', 'difficulty':'2'}"

{,
    'questions": {
        'question': 'what is your name',
        'answer':'Abraham',
        'category':'1',
        'difficulty':'2'
    }
    'success':True,
    'total_questions':19
    }

POST '/questions/searchTerm'

It search for a question using the submitted search term. Returns the results, success value, total questions.


Sample `curl -X POST -H "Content-Type: application/json" -d '{"searchTerm":"name"}' http://localhost:5000/search


{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "questions": [
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius
Clay?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }
  ],
  "success": true,
  "total_questions": 2
}

GET '/categories/<int:category_id>/questions'

It fetches questions for a cateogry specified by id request argument

Sample: curl http://127.0.0.1:5000/categories/2/questions

{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": 2,
  "questions": [
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "One",
      "category": 2,
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }
  ],
  "success": true,
  "total_questions": 4
}

POST /quizzes

it retrieves the actual question and the category and returns the next question in the same category and success value.


Sample: curl -X POST -H "Content-Type: application/json" -d '{"quiz_category":{"type":"Hisory","id":"4"}, "previous_questions":[6]}' http://localhost:5000/quizzes


{
  "previousQuestion": [
    6
  ],
  "question": {
    "answer": "Scarab",
    "category": 4,
    "difficulty": 4,
    "id": 23,
    "question": "Which dung beetle was worshipped by the
ancient Egyptians?"
  },
  "success": true
}