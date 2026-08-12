from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models.tongyi import ChatTongyi
from dotenv import load_dotenv

load_dotenv()
# StrOutputParser is for parsing the output of a language model into a string. It is useful when you want to extract
# specific information from the model's response and convert it into a string format for further processing or display.


parser = StrOutputParser()
model = ChatTongyi(model="qwen3-max")
prompt = PromptTemplate.from_template(
    "I will visit {place}, please list me several places to visit there, just the name no other info required."
)

chain = prompt | model | parser | model | parser

res: str = chain.invoke(input={"place": "New York"})
print(res)
print(type(res))


