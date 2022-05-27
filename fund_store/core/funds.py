from ast import List


from typing import List

from flask import request

def get_funds():
    query = request.args.get('query')
    return f"Worked! You searched for {query}"

def get_fund(fund_id : str):
    return f"You gave {fund_id}"