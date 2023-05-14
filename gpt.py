# use whatever model you want to use
from gpt4allj import Model
import re

model = Model('./model/ggml-gpt4all-j.bin')


def gen_response(prompt):
    response = model.generate(prompt)
    response = response.replace('\\', '\\\\')
    response = response.replace('"', "'").replace('\t','').replace('\n',"\\n")
    response = re.sub(r'( [1-9]\))', r'\\n\1', response)
    response = re.sub(r'\.( [1-9]\))', r'\.\\n\1', response)
    response = re.sub(r'\. ([1-9]\))', r'\.\\n\1', response)
    return response


def simple_gen_response(prompt):
    return model.generate(prompt)
