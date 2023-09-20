import os

from langchain import OpenAI
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.chains import RetrievalQA
import pinecone

pinecone.init(api_key="23559263-9c43-4b49-a98b-65f531cfaa0e", environment="gcp-starter")

if __name__ == "__main__":
    print("Hello vector chain")
    loader = TextLoader("mediumblogs.txt")
    # loader = loader.encoding("ISO-8859-1")
    document = loader.load()
    print(document)

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(document)
    print(len(texts))

    embeddings = OpenAIEmbeddings(openai_api_key=os.environ.get("OPENAI_API_KEY"))
    docsearch = Pinecone.from_documents(texts, embeddings, index_name="medium-blogs-embeddings-index")
    qa = RetrievalQA.from_chain_type(
        llm=OpenAI(), chain_type="stuff", retriever=docsearch.as_retriever(), return_source_documents=True
    )
    query = "What is a vector database give me a 15 word asnwer for beginner"
    result = qa({"query": query})
    print(result)
