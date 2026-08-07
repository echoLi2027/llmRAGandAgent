from langchain_ollama import OllamaLLM

# 不用qwen3-max，因为qwen3-max是聊天模型，qwen-max是大语言模型
model = OllamaLLM(model="deepseek-r1:8b")

# 调用invoke向模型提问
res = model.invoke(input="你是谁呀能做什么？")

print(res)