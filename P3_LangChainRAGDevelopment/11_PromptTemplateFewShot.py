from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate
from langchain_community.llms.tongyi import Tongyi

# zero-shot
example_template = PromptTemplate.from_template(
    "单词：{word}, 反义词：{antonym}"
)

example_data = [
    {"word": "大", "antonym": "小"},
    {"word": "上", "antonym": "下"},
]

few_shot_template = FewShotPromptTemplate(
    # prompt template, also contain input_variables
    example_prompt=example_template,
    # example data for input_variables, list of dict
    examples=example_data,
    # prompt before examples, can contain input_variables
    prefix="告知我单词的反义词，我提供如下的示例：",
    # prompt after examples, can contain input_variables
    suffix="基于前面的示例告知我，{input_word}的反义词是？",
    # claimed in prefix or suffix, the variable name to be injected
    input_variables=['input_word']
)

prompt_text = few_shot_template.invoke(input={"input_word": "左"}).to_string()
print(prompt_text)

model = Tongyi(model="qwen-max")
print(model.invoke(input=prompt_text))