# import os
# from dotenv import load_dotenv

# load_dotenv(os.path.normpath(os.path.join(os.path.abspath(__file__),"..","..","..",".env"))) # take environment variables from .env.

from rag_aia_prd import rag_score_prd, prd_idx_map
from rag_aia_prd import extract_score

from typing import List
from promptflow import tool

# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def my_python_tool(prd_ls: List[str], analyz_result:str) -> str:
    prdname = prd_ls[0].strip()
    # prdname = "AIA Voluntary Health Insurance Flexi"
    idxname = prd_idx_map[prdname] #"aia_avf"

    analyz_result_ls = analyz_result.split("\n\n")[1:]

    resultstr = rag_score_prd(idxname, analyz_result_ls)
    return {"score":extract_score(resultstr), "resultstr":resultstr}




if __name__ == "__main__":
    print(os.path.normpath(os.path.join(os.path.abspath(__file__),"..","..",".env")))