from ast import List


from typing import List

def get_funds(query : List[str]):
    return f"Worked! You searched for {query}"

def get_fund(fund_id : str):
    return f"You gave {fund_id}"