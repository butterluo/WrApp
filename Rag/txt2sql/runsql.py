
from promptflow import tool
from db.utils import *

# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def my_python_tool(input1: str) -> str:
    print(input1)
    sql = input1.split('```sql')[1].strip().split('```')[0].strip()
    print(f">>>{sql}<<<")
    res = str(execute_sql(sql))
    print(f"*>{res}<*")
    return res
