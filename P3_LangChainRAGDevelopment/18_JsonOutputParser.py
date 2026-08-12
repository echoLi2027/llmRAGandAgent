from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models.tongyi import ChatTongyi
from dotenv import load_dotenv

load_dotenv()
# StrOutputParser is for parsing the output of a language model into a string.
# JsonOutputParser is for parsing the output of a language model into a dictionary.

str_parser = StrOutputParser()
json_parser = JsonOutputParser()

model = ChatTongyi(model="qwen3-max")

first_prompt = PromptTemplate.from_template("find me a classical {country} literature, and return the result in JSON format with key 'title', "
                             "value is the book's name, please strictly follow the format requirement.")

second_prompt = PromptTemplate.from_template("please give me the book {title}'s story outline, summarize it concisely.")

# dict(that input we give to invoke the chain) -> PromptValue -> AIMessage -> dict -> PromptValue -> AIMessage -> str
chain = first_prompt | model | json_parser | second_prompt | model | str_parser

for chunk in chain.stream(input={"country": "German"}):
    print(chunk, end="", flush=True)



