import os, json
from typing import Sequence

from langchain_core.messages import message_to_dict, messages_from_dict, BaseMessage
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_community.chat_models import ChatTongyi
from dotenv import load_dotenv

load_dotenv()

# message_to_dict：single msg obj（BaseMessage initialization） -> dict
# messages_from_dict：[dict, dict...]  -> [msg, msg...]
# AIMessage、HumanMessage、SystemMessage are all subclasses of BaseMessage

class FileChatMessageHistory(BaseChatMessageHistory):
    def __init__(self, session_id, storage_path):
        self.session_id = session_id
        self.storage_path = storage_path

        # complete file path
        self.file_path = os.path.join(self.storage_path, self.session_id)

        # ensure the folder exists, if not, create it
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        # Sequence is like list or tuple
        all_messages = list(self.messages)      # msg already in the history
        all_messages.extend(messages)           # new msg + old msg = all msg

        # sync the data to local file
        # obj -> binary
        # to make it easier, we can convert BaseMessage to dict (using json module to write as json string)
        # official message_to_dict: single msg obj (BaseMessage initialization) -> dict
        # new_message = []
        # for msg in all_messages:
        #     d = message_to_dict(msg)
        #     new_message.append(d)

        new_messages = [message_to_dict(d) for d in all_messages]
        # write data to file
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(new_messages, f, ensure_ascii=False)

    # property decorator turns the messages method into a member property
    @property
    def messages(self) -> list[BaseMessage]:
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                # the return value is: list[dict]
                messages_data = json.load(f)
                return messages_from_dict(messages_data)
        except FileNotFoundError:
            return []

    def clear(self) -> None:
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([], f)


model = ChatTongyi(model="qwen3-max")
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "you need to answer user questions based on chat history. Chat history: "),
        MessagesPlaceholder("chat_history"),
        ("human", "please answer the following question: {input}")
    ]
)

str_parser = StrOutputParser()

def print_prompt(full_prompt):
    print("="*20, full_prompt.to_string(), "="*20)
    return full_prompt

base_chain = prompt | print_prompt | model | str_parser

def get_history(session_id):
    return FileChatMessageHistory(session_id, storage_path="./chat_history")

# create a new chain that enhances the original chain: automatically append historical messages
conversation_chain = RunnableWithMessageHistory(
    base_chain,     # the original chain to be enhanced
    get_history,    # function to get the corresponding FileChatMessageHistory object based on session_id
    input_messages_key="input",             # indicates the placeholder for user input in the template
    history_messages_key="chat_history"     # indicates the placeholder for chat history in the template
)

if __name__ == '__main__':
    # fixed format, add LangChain configuration to configure the session_id for the current program
    session_config = {
        "configurable": {
            "session_id": "user_001"
        }
    }

    res = conversation_chain.invoke({"input": "Mike has 2 cats."}, session_config)
    print("First execution:", res)

    res = conversation_chain.invoke({"input": "John has 1 dog."}, session_config)
    print("Second execution:", res)

    res = conversation_chain.invoke({"input": "How many pets are there in total?"}, session_config)
    print("Third execution:", res)