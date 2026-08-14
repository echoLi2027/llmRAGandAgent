from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader(
    file_path="./data/pdf1.pdf",
    # by default is page mode, each page forms a Document object,
    # single mode returns only 1 Document object regardless of the number of pages
    # mode="single",
    mode="page",
    # if the PDF is password protected, you can provide the password here
    # password="itheima"
)

i = 0
for doc in loader.lazy_load():
    i += 1
    print(doc)
    print("="*20, i, "="*20)