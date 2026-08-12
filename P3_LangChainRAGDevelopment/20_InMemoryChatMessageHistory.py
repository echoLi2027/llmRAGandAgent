from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_models.tongyi import ChatTongyi
from dotenv import load_dotenv
from langchain_core.runnables.history import RunnableWithMessageHistory

load_dotenv()

model = ChatTongyi(model="qwen3-max")

# prompt = ChatPromptTemplate.from_message(
#     "you need to answer user questions based on chat history. Chat history: {chat_history}, user question: {input}, please answer concisely."
# )

prompt = ChatPromptTemplate.from_messages([
    ("system", "you're an AI assistant and you answer question concisely."),
    MessagesPlaceholder("chat_history"),
    ("human", "please answer the following question: {input}")
])

# the prompt should return as the input otherwise the chain will not work
def print_prompt(full_prompt):
    print("="*20, full_prompt.to_string(), "="*20)
    return full_prompt
# this chain has the prompt structure, but the injected params is not there yet
chain = prompt | print_prompt | model | StrOutputParser()

chat_history_store = {}

# for InMemoryChatMessageHistory() is giving a temporal memory for current session,
# according to the session_id, we can get the corresponding InMemoryChatMessageHistory() object
# if current session_id is not in the chat_history_store,
# we create a new InMemoryChatMessageHistory() object and store it in the chat_history_store
def get_history(session_id):
    if session_id not in chat_history_store:
        chat_history_store[session_id] = InMemoryChatMessageHistory()
    return chat_history_store[session_id]

# create a new chain that enhances the original chain: automatically append historical messages
# also inject the last input from user, but here be aware that in the get_history function,
# we need to inject session_id to get the corresponding InMemoryChatMessageHistory() object,
# otherwise it'll throw error
conversation_chain = RunnableWithMessageHistory(
    chain,
    get_history,
    input_messages_key="input",
    history_messages_key="chat_history"
)

if __name__ == '__main__':

    session_config = {
        "configurable": {
            "session_id": "user_001"
        }
    }

    # the first execution, the history is empty, so the model will only see the current input
    # and the session_id is injected automatically, this param is respective with the RunnableConfig param,
    # so that the get_history function can get the corresponding InMemoryChatMessageHistory() object
    # and current input will also automatically be appended to the InMemoryChatMessageHistory() object
    # respective with the session_id
    res = conversation_chain.invoke({"input": "Mike has 2 cats"}, session_config)
    print("First execution:", res)

    # now the history is not empty, the model will see the previous input and the current input
    # but also need to inject the session_id to get the corresponding InMemoryChatMessageHistory() object
    # and this input and AI conversation will also automatically be appended to the InMemoryChatMessageHistory() object
    # respective with the session_id
    res = conversation_chain.invoke({"input": "John has 1 dog"}, session_config)
    print("Second execution:", res)

    res = conversation_chain.invoke({"input": "How many pets are there in total?"}, session_config)
    print("Third execution:", res)