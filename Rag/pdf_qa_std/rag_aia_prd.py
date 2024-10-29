import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizableTextQuery
from promptflow.core import Prompty

prd_idx_map = { #@# REFACTOR 使用相似度/编辑距离等模糊判断prd
    "AIA Voluntary Health Insurance Flexi": "aia_avf",
    "AIA Voluntary Health Insurance Privilege Ultra": "aia_avpu"
}

load_dotenv(os.path.normpath(os.path.join(os.path.abspath(__file__),"..","..","..",".env"))) # take environment variables from .env.

def extract_score(result_str):
    a = result_str.split(":")[-1]
    c = a.split('**')[0]
    return int(c)



def rag_score_prd(idxname, analyz_result_ls):
    search_endpoint = os.environ["AZURE_SEARCH_SERVICE_ENDPOINT"]
    search_credential = AzureKeyCredential(os.environ["AZURE_SEARCH_ADMIN_KEY"]) if len(os.environ["AZURE_SEARCH_ADMIN_KEY"]) > 0 else DefaultAzureCredential()
    search_client = SearchClient(endpoint=search_endpoint, index_name=idxname, credential=search_credential)

    chunk_set = set()
    rag_ls = []
    for query in analyz_result_ls:
        vector_query_1 = VectorizableTextQuery(text=query, k_nearest_neighbors=1, fields="titleVector", weight=1)
        vector_query_2 = VectorizableTextQuery(text=query, k_nearest_neighbors=1, fields="chunkVector", weight=1)

        results = search_client.search(  
            search_text=None,  
            vector_queries=[vector_query_1, vector_query_2],
            select=["title", "chunk", "chunk_id"],
            # query_type=QueryType.SEMANTIC, semantic_configuration_name='my-semantic-config', query_caption=QueryCaptionType.EXTRACTIVE, query_answer=QueryAnswerType.EXTRACTIVE,
            top=2
        )
        for result in results: 
            chunkid = result['chunk_id']
            if chunkid in chunk_set:
                continue
            else:
                title = result['title']
                ctnt = result['chunk']
                rag_ls.append( {"title":title, "content":ctnt} )
                chunk_set.add(chunkid)
        # for result in results:  
        #     print(f"Title: {result['title']}")  
        #     print(f"Score: {result['@search.score']}")  
        #     print(f"Content: {result['chunk']}")  
        #     print(f"Category: {result['chunk_id']}")  
        #     # print(f"Reranker Score: {result['@search.reranker_score']}")
        #     # captions = result["@search.captions"]
        #     # if captions:
        #     #     caption = captions[0]
        #     #     if caption.highlights:
        #     #         print(f"Caption: {caption.highlights}")
        #     #     else:
        #     #         print(f"Caption: {caption.text}")
        #     print("\n")
    
    scro_prd_prmp = Prompty.load(source=os.path.normpath(os.path.join(os.path.abspath(__file__),"..","scro_prd.prompty")))
    resultstr = scro_prd_prmp(usr_requirment=analyz_result_ls, rag_result=rag_ls)
    return resultstr


if __name__ == "__main__":
    a = [
        """1. **Personal and Family Needs:**
   - The user is interested in health insurance products, indicating a need for health coverage for herself and possibly her children. """,
        """2. **Family Financial Situation:**
   - The user is a housewife, which might suggest reliance on a partner's income. However, specific financial details are not provided. """,
        """3. **Children's Needs:**
   - The user has two children, aged 7 and 5, which may imply a need for family health coverage. """,
        """4. **Budget and Financial Planning:**
   - The user is considering two specific products, suggesting she has a budget in mind, but exact financial constraints are not mentioned. """,
        """In summary, the user is looking for health insurance options suitable for a family with young children, focusing on health coverage needs. Further details about financial situation and existing coverage would help in making a more tailored recommendation. """
    ]
    b = rag_score_prd('aia_avpu',a)
    print(b)
