### install
```
pip install -r requirements.txt
```

Create .env file from .env.example

Fake files expected in /data/

### Run 
For SQL:
```
python main.py sql <max_page>
```
Data save in db. Query for request full table in src.sql - GET_TABLE

For CSV:
```
python main.py csv <max_page>
```