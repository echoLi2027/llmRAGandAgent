from langchain_community.chat_models.tongyi import ChatTongyi

# 不用qwen3-max，因为qwen3-max是聊天模型，qwen-max是大语言模型
model = ChatTongyi(model="qwen3-max")

# prepare messages
messages = [
    ("system","你是一个边塞诗人。"),
    ("human","写一首唐诗"),
    ("ai","锄禾日当午，汗滴禾下土，谁知盘中餐，粒粒皆辛苦。"),
    ("human","按照你上一个回复的格式，在写一首唐诗。")
]

# 调用invoke向模型提问
res = model.stream(input=messages)

# for循环迭代打印输出，通过.content来获取到内容
for chunk in res:
    print(chunk.content, end="", flush=True)
