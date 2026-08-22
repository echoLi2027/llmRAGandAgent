from langchain_chroma import Chroma
from langchain_community.document_loaders import CSVLoader
from langchain_community.embeddings import DashScopeEmbeddings
from dotenv import load_dotenv

load_dotenv()

# Chroma is a light vector database.
# Make sure you have installed the langchain-chroma and chromadb libraries. If not, please install them using pip.

vector_store = Chroma(
    collection_name="test", # give vector storage a name, similar to a table name in a database
    embedding_function=DashScopeEmbeddings(),  # embedding model
    persist_directory="./chroma_db"  # specify the folder where data is stored
)

loader = CSVLoader(
    file_path="./data/info.csv",
    encoding="utf-8",
    source_column="source"
)

docs = loader.load()

vector_store.add_documents(
    documents=docs, # documents to be added, type: list[Document]
    ids=["id"+str(i) for i in range(1, len(docs)+1)] # provide ids for the added documents (strings)  list[str]
)

vector_store.delete(["id1", "id2"])

res = vector_store.similarity_search(
    "is Python easy to learn?",
    3, # how many results to retrieve
    # in this case you will only get the data with source "EduSpark" when you do similarity_search
    filter={"source": "EduSpark"}
)

print(res)
