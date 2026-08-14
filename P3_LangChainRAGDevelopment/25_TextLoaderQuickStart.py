from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

loader = TextLoader(
    "./data/PythonBasicSyntax.txt"
)


docs = loader.load()        # [Document]

# due to the txt file being too large, we can use the text splitter to split it into smaller segments for processing
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,         # maximum number of characters per segment
    chunk_overlap=50,       # number of overlapping characters between segments
    # symbols used to determine natural paragraph breaks in the text
    separators=["\n\n", "\n", ".", "!", "?", " ", ""],
    length_function=len,    # function used to count characters
)

split_docs = splitter.split_documents(docs)
i = 0
for doc in split_docs:
    i += 1
    print(doc)
    print("="*20, i, "="*20)