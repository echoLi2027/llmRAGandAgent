from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_models.tongyi import ChatTongyi

chat_prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "you're a poet can write poems."),
        MessagesPlaceholder("history"),
        ("human", "please make a poem about the {item}.")
    ]
)

history_data = [
    ("human", "please make a poem about the sunset."),
    ("ai", "The sun sets in the west, painting the sky with hues of gold and crimson. The waves dance to the rhythm of the evening breeze, as the world prepares for a peaceful night."),
    ("human", "please make a poem about the moon."),
    ("ai", "The moon rises high in the night sky, casting a silver glow upon the earth. Its gentle light illuminates the darkness, guiding travelers and dreamers alike.")
]

# StringPromptValue    to_string()
prompt_text = chat_prompt_template.invoke({"history": history_data, "item": "star"}).to_string()

model = ChatTongyi(model="qwen3-max")
res = model.invoke(prompt_text)
print(res.content, type(res))