# coding: utf-8

"""
FILE: sample_analyze_result_pdf.py

DESCRIPTION:
    This sample demonstrates how to convert an analog PDF into a PDF with embedded text.

    This sample uses Read model to demonstrate.

    See pricing: https://azure.microsoft.com/pricing/details/ai-document-intelligence/.

USAGE:
    python sample_analyze_result_pdf.py

    Set the environment variables with your own values before running the sample:
    1) DOCUMENTINTELLIGENCE_ENDPOINT - the endpoint to your Document Intelligence resource.
    2) DOCUMENTINTELLIGENCE_API_KEY - your Document Intelligence API key.
"""

import os


def analyze_result_pdf():
    path_to_sample_documents = os.path.abspath(
        os.path.join(
            os.path.abspath(__file__),
            "..",
            "data/AIA_Voluntary_Health_Insurance_Flexi.pdf",
        )
    )
    # [START analyze_result_pdf]
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.documentintelligence import DocumentIntelligenceClient
    from azure.ai.documentintelligence.models import AnalyzeOutputOption, AnalyzeResult
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.documentintelligence import DocumentIntelligenceClient
    from azure.ai.documentintelligence.models import AnalyzeDocumentRequest, ContentFormat, AnalyzeResult

    endpoint = os.environ["DOCUMENTINTELLIGENCE_ENDPOINT"]
    key = os.environ["DOCUMENTINTELLIGENCE_API_KEY"]

    document_intelligence_client = DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    with open(path_to_sample_documents, "rb") as f:
        poller = document_intelligence_client.begin_analyze_document(
            "prebuilt-layout",
            analyze_request=f,
            # output=[AnalyzeOutputOption.PDF],
            output_content_format=ContentFormat.MARKDOWN,
            content_type="application/octet-stream",
        )
    result: AnalyzeResult = poller.result()
    # operation_id = poller.details["operation_id"]
    #
    # response = document_intelligence_client.get_analyze_result_pdf(model_id=result.model_id, result_id=operation_id)
    # with open("analyze_result.pdf", "wb") as writer:
    #     writer.writelines(response)
    # [END analyze_result_pdf]
    print(f"Here's the full content in format {result.content_format}:\n")
    print(result.content)
    print("-------------------"*10)
    print(result.pages)
    print(result.sections)
    print(result.paragraphs)
    print(result.figures)
    print(result.tables) # and many other attributes

def analyze_result_pdf2(book_file_path, output_dir, prdShort):
    from langchain import hub
    from langchain_openai import AzureChatOpenAI
    from langchain_community.document_loaders import AzureAIDocumentIntelligenceLoader
    from langchain_openai import AzureOpenAIEmbeddings
    from langchain.schema import StrOutputParser
    from langchain.schema.runnable import RunnablePassthrough
    from langchain.text_splitter import MarkdownHeaderTextSplitter
    from langchain.vectorstores.azuresearch import AzureSearch

    endpoint = os.environ["DOCUMENTINTELLIGENCE_ENDPOINT"]
    key = os.environ["DOCUMENTINTELLIGENCE_API_KEY"]

    # Initiate Azure AI Document Intelligence to load the document. You can either specify file_path or url_path to load the document.
    loader = AzureAIDocumentIntelligenceLoader(
        file_path=book_file_path, 
        api_key = key, 
        api_endpoint = endpoint, 
        api_model="prebuilt-layout")

    # analysis_features=["ocr_high_resolution"]
    # Specify the pages to analyze as an optional parameter
    # analyze_options = {
    #     "pages": "10-16",  # This specifies that only pages 1 through 52 should be analyzed
    #     "reading_order": "natural",  # 自然阅读顺序
    #     "text_angle": True,  # 检测文本角度
    #     "ocr_high_resolution": True  # 启用高分辨率OCR
    # }

    # Set the analyze options via a method or directly if the load method does not support extra parameters

    docs = loader.load()

    # Split the document into chunks base on markdown headers.
    headers_to_split_on = [
        ("#", "Header_1"),
        ("##", "Header_2"),
        ("###", "Header_3"),
    ]
    text_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)

    docs_string = docs[0].page_content
    splits = text_splitter.split_text(docs_string)

    print("Length of splits: " + str(len(splits)))

    

    max_index_length = len(str(len(splits) - 1))

    for index, document in enumerate(splits):
        # Construct the file name
        padded_index = f"{index:0{max_index_length}d}"
        file_name = f"{prdShort}-{padded_index}.md"
        file_path = os.path.join(output_dir, file_name)
        
        # Write the chunk to the file
        with open(file_path, 'w') as file:
            h1 = document.metadata.get('Header_1','')
            h2 = document.metadata.get('Header_2','')
            h3 = document.metadata.get('Header_3','')
            #@# REFACTOR 最好给MD文档,纯文本,少格式变化和各种炫酷图标
            #@# REFACTOR 过滤掉页头页尾断页等无用标记, 把figure图片换成gpt-4o生成的描述.因一些figure不在文档结构内且解析后会出现乱符号形成噪音.
            #@# REFACTOR Header_3的内容少则往上一级合并成一个文件,Header_2也是
            content = f"{h1}. {h2}. {h3}. \n\n{document.page_content}"
            file.write(content)

if __name__ == "__main__":
    from azure.core.exceptions import HttpResponseError
    from dotenv import find_dotenv, load_dotenv

    book_file_path="/mnt/d/BT/SRC/MS/DEMO/WrApp/TMP/data/AIA_Voluntary_Health_Insurance_Privilege_Ultra.pdf"
    output_dir = "/mnt/d/BT/SRC/MS/DEMO/WrApp/TMP/data/AIA_AVPU"
    prdShort = 'AIAAVPU'

    try:
        load_dotenv(find_dotenv())
        analyze_result_pdf2(book_file_path, output_dir, prdShort)
    except HttpResponseError as error:
        # Examples of how to check an HttpResponseError
        # Check by error code:
        if error.error is not None:
            if error.error.code == "InvalidImage":
                print(f"Received an invalid image error: {error.error}")
            if error.error.code == "InvalidRequest":
                print(f"Received an invalid request error: {error.error}")
            # Raise the error again after printing it
            raise
        # If the inner error is None and then it is possible to check the message to get more information:
        if "Invalid request".casefold() in error.message.casefold():
            print(f"Uh-oh! Seems there was an invalid request: {error}")
        # Raise the error again
        raise