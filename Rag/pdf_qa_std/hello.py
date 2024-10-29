# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

from promptflow.core import tool

# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need


@tool
def my_python_tool(input1: str) -> str:
    p = input1
    prd_ls = p.split("\n")
    return prd_ls


if __name__ == "__main__":
    p = "Prompt: 用户的问题中包含了两个产品：\n\n1. AIA Voluntary Health Insurance Flexi\n2. AIA Voluntary Health Insurance Privilege Ultra"
    p = """ 
Based on the information provided, here's what we can infer:

1. **Personal and Family Needs:**
   - The user is interested in health insurance products, indicating a need for health coverage for herself and possibly her children.

2. **Family Financial Situation:**
   - The user is a housewife, which might suggest reliance on a partner's income. However, specific financial details are not provided.

3. **Children's Needs:**
   - The user has two children, aged 7 and 5, which may imply a need for family health coverage.

4. **Budget and Financial Planning:**
   - The user is considering two specific products, suggesting she has a budget in mind, but exact financial constraints are not mentioned.

In summary, the user is looking for health insurance options suitable for a family with young children, focusing on health coverage needs. Further details about financial situation and existing coverage would help in making a more tailored recommendation.
"""
    p = """### Conclusion:

Given the user's need for health coverage for himself and his children, the AIA Voluntary Health Insurance Flexi Scheme seems to align well with his requirements. The comprehensive coverage, tax benefits, and flexibility make it a strong candidate. However, the lack of specific premium cost information and the lifetime payment requirement could be potential concerns.

**Score: 8**
    """
    a = p.split(":")[-1]
    print(a)
    c = a.split('**')[0]
    print(int(c))