import sys
from src.api import api_fake_request

from src.db import create_tables, write_db
from src.csv_pandas import pandas_csv


def get_data(page: int):
    response = api_fake_request(page)
    if '_embedded' in response.keys():
        if 'leads' in response['_embedded'].keys():
            data = response['_embedded']['leads']
            return data
    return []
    

def to_sql(max_page: int):
    create_tables()
    for page in range(max_page):
        data = get_data(page)
        write_db(data)

def to_csv(max_page: int):
    data = []
    for page in range(max_page):
        data.extend(get_data(page))
    pandas_csv(data)


def main():
    max_page = int(sys.argv[2])
    if sys.argv[1] == 'csv':
        to_csv(max_page)
    elif sys.argv[1] == 'sql':
        to_sql(max_page)


if __name__ == "__main__":
    main()