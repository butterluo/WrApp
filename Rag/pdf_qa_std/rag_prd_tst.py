import os
from promptflow.core import Prompty

prmpath = os.path.normpath(os.path.join(os.path.abspath(__file__),"..","rag_prd_tst.prompty"))
print(prmpath)
prmp = Prompty.load(source=prmpath)
res = prmp()

print(res)