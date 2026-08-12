from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models.tongyi import ChatTongyi
from dotenv import load_dotenv
from langchain_core.runnables import RunnableLambda

load_dotenv()
# StrOutputParser is for parsing the output of a language model into a string. JsonOutputParser is for parsing the
# output of a language model into a dictionary. other than using JsonOutputParser, you can also use RunnableLambda to
# convert the output of a language model into a dictionary. By RunnableLambda, we can convert our customized Lambda
# anonymous function which can customize the output data conversion and this RunnableLambda can convert this function
# obj into RunnableSerializable obj, which can be put into the chain, and this RunnableSerializable obj can be
# serialized and deserialized, which can be used in distributed scenarios.

str_parser = StrOutputParser()

first_prompt = PromptTemplate.from_template(
    "please find me a country which is suitable to go in {season} time. just generate the name no other info."
)

second_prompt = PromptTemplate.from_template(
    "please tell me this {country}'s tourism attractions and the best time to go there."
)

# define a RunnableLambda obj, which can convert the output of a language model into a dictionary.
# The input of the lambda function is an AIMessage obj, and the output of the lambda function is a dictionary obj.
# The key of the dictionary is "country", and the value of the dictionary is the content of the AIMessage obj.
my_func = RunnableLambda(lambda ai_msg: {"country": ai_msg.content})

model = ChatTongyi(model="qwen3-max")

chain = first_prompt | model | my_func | second_prompt | model | str_parser

# can also directly use lambda function to convert the output of a language model into a dictionary.
# the substance of the substance is that it can automatically convert the function into RunnableLambda obj,
# which can be put into the chain.
# chain = first_prompt | model | (lambda ai_msg: {"country": ai_msg.content}) | second_prompt | model | str_parser

for chunk in chain.invoke(input={"season": "winter"}):
    print(chunk, end="", flush=True)

