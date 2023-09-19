import os

from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone


if __name__ == "__main__":
    print("Hello vector chain")
    loader = TextLoader("C:/Users/varsh/Desktop/python/intro-to-vector/mediumblogs.txt", autodetect_encoding=True)
    #loader = loader.encoding("ISO-8859-1")
    document = loader.load()
    print(document)

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(document)
    print(len(texts))

    embeddings = OpenAIEmbeddings(openai_api_key = os.environ.get("OPENAI_API_KEY"))



