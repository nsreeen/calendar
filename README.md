# calendar

## Set up
 Create a venv:
 `python3 -m venv venv`

Install requirements:
`python -m pip install -r requirements.txt`

Start the venv
 `source venv/bin/activate`


 ## Run
Start the service:
 `uvicorn main:app --reload`

 Open index.html.


## Todos
- allow add events input
- place events in grid with times
- timezones (show times in viewers timezone)
- user data: online times
- only owner can add events/ change online times?
