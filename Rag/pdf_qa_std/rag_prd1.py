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

# from rag_aia_prd import rag_score_prd, prd_idx_map
# from rag_aia_prd import extract_score

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

    return [{"score":extract_score(resultstr), "resultstr":resultstr, "prdname":prdname}]




if __name__ == "__main__":
    print(os.path.normpath(os.path.join(os.path.abspath(__file__),"..","..",".env")))