from langchain_community.document_loaders import JSONLoader

# loader = JSONLoader(
#     file_path="./data/stu.json",
#
#     # in this case the extracted content is a string, so we can use the key to extract the value
#     # jq_schema=".name",
#
#     # in this case the extracted content is a list, 'hobby' is a list, so we need to specify the index of the element
#     # we want to extract
#     # jq_schema=".hobby[2]",
#
#     # in this case the extracted content is a dict, so we can use the key to extract the value
#     jq_schema=".other.addr"
#
#     # in this case the extracted content is a string, so we can leave the text_content parameter as default True
#     # text_content=True,
# )


# loader = JSONLoader(
#     # file_path="./data/stu.json",
#     file_path="./data/stus.json",
#
#     # take the whole content of the JSON file, in this case,
#     # we can use "." to indicate that we want to extract the whole content
#     # jq_schema=".",
#
#     # in this case the extracted content is a list, 'hobby' is a list, so we need to specify the index of the element
#     # jq_schema=".hobby",
#
#     # in this case the extracted content is a list of dicts,
#     # so we can use ".[]" to fetch all the dicts in the list, and then we can use the key to extract the value
#     # jq_schema=".[]",
#
#     # get all names from the list of dicts
#     # jq_schema=".[].name",
#
#     # get the 2nd name from the list of dicts, index starts from 0
#     jq_schema=".[1].name",
#
#     text_content=False,     # set False to indicate that the extracted content is not a string, by default it is True
# )

loader = JSONLoader(
    file_path="./data/stu_json_lines.json",
    jq_schema=".",
    text_content=False,
    json_lines=True         # indicate that this is a JSONLines file (each line is a separate standard JSON)
)

for doc in loader.lazy_load():
    print(doc)
