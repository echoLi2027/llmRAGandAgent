from langchain_core.prompts import PromptTemplate
from langchain_community.llms.tongyi import Tongyi
from dotenv import load_dotenv

load_dotenv()

prompt = PromptTemplate.from_template("you're an AI assistant")
model = Tongyi(model="qwen-max")

# but if we check the invoke and stream method in the end their parent class is Runnable,
# which means they can both be called on the chain object directly, and the chain object is also a Runnable,
# so we can use the invoke and stream method directly on the chain object

# chain = prompt | model | prompt | model
# chain.invoke({})
# chain.stream({})
# print(type(chain))
chain = prompt | model
print(chain.invoke({}))
for chunk in chain.stream({}):
    print(chunk, end="", flush=True)
print("\n",type(chain.invoke({})))