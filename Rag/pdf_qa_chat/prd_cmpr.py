import os
from typing import List
from promptflow import tool
from promptflow.core import Prompty

# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def my_python_tool(scor_ls1: List, scor_ls2: List, usr_q:str) -> str:
    ttl_ls = []
    ttl_ls.extend(scor_ls1)
    ttl_ls.extend(scor_ls2)
    scor = 0
    prefer = None
    for d in ttl_ls:
        if d["score"] > scor:
            prefer = d
            scor = d["score"]
    cmpr_prd_prmp = Prompty.load(source=os.path.normpath(os.path.join(os.path.abspath(__file__),"..","prd_cmpr_e.prompty")))
    result = cmpr_prd_prmp(usr_q=usr_q, prdname=prefer["prdname"], reason=prefer["resultstr"])
    return result
