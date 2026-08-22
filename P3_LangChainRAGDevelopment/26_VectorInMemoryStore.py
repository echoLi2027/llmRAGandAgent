from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.document_loaders import CSVLoader
from dotenv import load_dotenv

load_dotenv()
# open a space for vector storage, to initialize the vector store, you need to provide an embedding model
vector_store = InMemoryVectorStore(
    embedding=DashScopeEmbeddings()
)

loader = CSVLoader(
    file_path="./data/info.csv",
    encoding="utf-8",
    # in this case you can do filter={"source": "example1"} to filter the data,
    # in that case you can get the data with source "example1" when you do similarity_search
    source_column="source",     # specify the source of this data
)

docs = loader.load()

# Add documents to the vector store,
# you need to provide a list of Document objects and a list of corresponding ids (strings)
vector_store.add_documents(
    documents=docs,       # documents to be added, type: list[Document]
    # provide ids for the added documents (strings)  list[str]
    ids=["id"+str(i) for i in range(1, len(docs)+1)]
)

# Delete documents from the vector store, you need to provide a list of ids (strings)
vector_store.delete(["id1", "id2"])

# Retrieve documents from the vector store, returns a list of Document objects
res = vector_store.similarity_search(
    "find a method to lose weight",
    2
)

print(res)
