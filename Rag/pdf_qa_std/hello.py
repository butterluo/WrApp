# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

from promptflow.core import tool

# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need


@tool
def my_python_tool(input1: str) -> str:
    return "Prompt: " + input1


if __name__ == "__main__":
    a = "Prompt: 用户的问题中包含了两个产品：\n\n1. AIA Voluntary Health Insurance Flexi\n2. AIA Voluntary Health Insurance Privilege Ultra"
    print(a.split("\n"))