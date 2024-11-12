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
    
    scro_prd_prmp = Prompty.load(source=os.path.normpath(os.path.join(os.path.abspath(__file__),"..","scro_prd.prompty")))
    resultstr = scro_prd_prmp(usr_requirment=analyz_result_ls, rag_result=rag_ls)
    return resultstr

from typing import List
from promptflow import tool

@tool
def my_python_tool(prd_ls: List[str], analyz_result:str) -> str:
    prdname = prd_ls[1].strip()
    # prdname = "AIA Voluntary Health Insurance Privilege Ultra"
    idxname = prd_idx_map[prdname] #"aia_avpu"

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
    
    scro_prd_prmp = Prompty.load(source=os.path.normpath(os.path.join(os.path.abspath(__file__),"..","scro_prd_e.prompty")))
    resultstr = scro_prd_prmp(usr_requirment=analyz_result_ls, rag_result=rag_ls)

    return [{"score":extract_score(resultstr), "resultstr":resultstr, "prdname":prdname}]



