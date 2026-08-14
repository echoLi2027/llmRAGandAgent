from langchain_community.document_loaders import CSVLoader

loader = CSVLoader(
    file_path="./data/stu.csv",
    csv_args={
        # assigned delimiter, in case of CSV files, it's usually a comma, but if the file uses a different delimiter,
        # you can specify it here but be careful, if the delimiter is not specified correctly, it may lead to
        # incorrect parsing of the CSV file
        "delimiter": ",",
        # assigned quotechar, in case of CSV files, it's usually a double quote, but if the file uses a different quote character,
        # you can specify it here but be careful, if the quotechar is not specified correctly, it may lead to
        "quotechar": '"',
        # If the CSV file has a header row, you don't need to specify fieldnames, but if it doesn't, you can specify them here
        # "fieldnames": ['name', 'age', 'gender', 'hobby']
    },
    # encoding="utf-8"
)

# batch loading .load()   ->  [Document, Document, ...]
# but if the CSV file is too large, it may cause memory issues
# docs = loader.load()
#
# for doc in docs:
#     print(doc)
#     print(type(doc), "\n")

# lazy loading .lazy_load()  ->  iterator[Document] lazy_load method will get a generator object, which can be used
# to iterate over the documents one by one, which is more memory efficient can also avoid if the CSV file is too
# large, it may cause memory issues
for doc in loader.lazy_load():
    print(doc)
    print(type(doc), "\n")
