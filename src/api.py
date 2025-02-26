from typing import List
import json


def read_json(page_str: int) -> List[dict]:
    with open(f'leads_response_{page_str}.json', 'r', encoding='utf-8') as file:
        return json.load(file)
    

def api_fake_request(page: int) -> List[dict]:
    if page in (1, 2):
        return read_json(page)
    else:
        return {'page': page,
                '_embedded' : { 'leads' : []}} 