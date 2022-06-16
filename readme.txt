to run,

create a .env file like .env.example

activate virtual env
mac/linux : source bin/activate
windows : .\Scripts\activate


install requirements:
pip install -r requirements.txt

run locally:
uvicorn src.app:app --reload --port 3000