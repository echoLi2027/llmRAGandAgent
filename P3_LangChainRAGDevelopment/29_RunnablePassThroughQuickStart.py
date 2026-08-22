from langchain_community.chat_models import ChatTongyi
from langchain_core.documents import Document
from langchain_core.runnables import RunnablePassthrough
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

def print_prompt(prompt):
    print("="*20)
    print(prompt.to_string())
    print("="*20)
    return prompt

model = ChatTongyi(model="qwen3-max")
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "please answer the user's question concisely and professionally based on the known reference materials I provide. Reference materials:{context}."),
        ("user", "user question:{input}")
    ]
)

vector_store = InMemoryVectorStore(embedding=DashScopeEmbeddings(model="text-embedding-v4"))


# prepare some reference materials (data in the vector store)
# input a list of strings to add_texts, list[str]
vector_store.add_texts(
    ["Losing weight is about eating less and exercising more", "During the fat loss period, it is important to eat, eat light and low-fat, control calorie intake and exercise", "Running is a good exercise"]
)

input_str = "how to lose weight?"

docs = vector_store.similarity_search(
    input_str,
    2
)

# langchain intermediate vector store object has a method: as_retriever,
# which can return an instance object of a subclass of the Runnable interface
retriever = vector_store.as_retriever(search_kwargs={"k": 2})

def format_func(docs: list[Document]):
    if not docs:
        return "no relevant reference materials"

    formatted_str = "["
    for doc in docs:
        formatted_str += doc.page_content
    formatted_str += "]"

    return formatted_str

# chains are embedded in a chain
# in {..} can regard as a chain, the RunnablePassthrough() is a Runnable that can pass through(block) the input that gives in retriver(the vector store)
# the "context" is a input for format_func, which is the function to format the retrieved docs
# but prompt needs 2 inputs, so we need to use the "input" and "context" as the input for prompt
# so RunnablePassthrough() is used to copy the input to the retriever,
# and the retriever also get the input_str will return the docs, which will be passed to format_func to format the docs,
# and then the formatted docs will be passed to prompt as "context", and the original input will be passed to prompt as "input"
chain = (
    {"input": RunnablePassthrough(), "context": retriever | format_func} | prompt | print_prompt | model | StrOutputParser()
)

res = chain.invoke(input_str)
print(res)

