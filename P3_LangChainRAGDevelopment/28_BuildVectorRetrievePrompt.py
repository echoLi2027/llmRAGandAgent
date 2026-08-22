from dotenv import load_dotenv
from langchain_community.chat_models import ChatTongyi
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

def print_prompt(prompt):
    print("=" * 20)
    print(prompt.to_string())
    print("=" * 20)
    return prompt

model = ChatTongyi(model="qwen3-max")
prompt = ChatPromptTemplate.from_messages(
    [
        ("system","based on the known reference materials I provide, answer the user's question concisely and professionally. Reference materials:{context}."),
        ("user","user question:{input}")
    ]
)

vector_store = InMemoryVectorStore(embedding=DashScopeEmbeddings(model="text-embedding-v4"))

# prepare some reference materials (data in the vector store)
# here we didn't use add_documents, but add_texts, which takes a list of strings more proper here
vector_store.add_texts(
    ["Losing weight is about eating less and exercising more", "During the fat loss period, it is important to eat, eat light and low-fat, control calorie intake and exercise", "Running is a good exercise"]
)

input_text = "how to lose weight?"

# retrieve reference materials from the vector store
res = vector_store.similarity_search(
    input_text,
    2
)
reference_text = "["
for doc in res:
    reference_text += doc.page_content
reference_text += "]"

chain = prompt | print_prompt | model | StrOutputParser()

result = chain.invoke({"input": input_text, "context": reference_text})
print(result)