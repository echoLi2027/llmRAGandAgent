from langchain_core.prompts import PromptTemplate
from langchain_community.llms.tongyi import Tongyi

# zero-shot
prompt_format = PromptTemplate.from_template(
    "我的邻居姓{lastname}, 刚生了{gender}, 你帮我起个名字，简单回答。"
)

model = Tongyi(model="qwen-max")

# invoke format method to inject information, then use invoke to call the model
# prompt_text = prompt_format.format(lastname="张", gender="女儿")
# res = model.invoke(input=prompt_text)
# print(res)

chain = prompt_format | model
# caveat: the input variable names in the prompt template must match the keys in the input dictionary, otherwise it
# will raise an error
res = chain.invoke(input={"lastname": "张", "gender": "女儿"})
print(res)
