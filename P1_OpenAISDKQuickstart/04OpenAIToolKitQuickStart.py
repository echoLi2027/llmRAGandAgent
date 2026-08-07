from openai import OpenAI

# 1. create the connection
client = OpenAI(
    base_url="https://ws-fsgmy61k7al0ufws.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)

# 2. send msg to llm
completion = client.chat.completions.create(
    model="qwen3.7-plus",
    messages=[
        # {"role": "system","content": "you're python developer, and speak clearly and concisely."},
        # {"role": "assistant","content": "what can I help you?"},
        # {"role": "user","content": "please write me a code which count number from 1 to 10"}

        # multiple round will give a context to llm to answer the question with better quality
        {"role": "system", "content": "you're ai assistant, and answering clearly and concisely."},
        {"role": "assistant", "content": "what can I help you?"},
        {"role": "user", "content": "I have 2 dogs."},
        {"role": "assistant", "content": "ok"},
        {"role": "user", "content": "I have 3 cats."},
        {"role": "assistant", "content": "ok"},
        {"role": "user", "content": "How many pets I have."}

    ],
    extra_body={"enable_thinking": True},
    stream=True
)
is_answering = False # whether entering response stage
# 3. process the response
for chunk in completion:
    if chunk.usage:
        print("\n" + "=" * 20 + "usage" + "=" * 20)
        print("completion_tokens:" + str(chunk.usage.completion_tokens))

    if not chunk.choices:
        continue

    delta = chunk.choices[0].delta

    reasoning = getattr(delta, "reasoning_content", None)
    if reasoning:
        print(delta.reasoning_content, end="", flush=True)

    if delta.content:
        if not is_answering:
            print("\n" + "=" * 20 + "complete response" + "=" * 20)
            is_answering = True
        print(delta.content, end="", flush=True)
