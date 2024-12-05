import os

from flask import Flask
from llama_cpp import Llama

app = Flask(__name__)

llm = Llama.from_pretrained(
 repo_id="IlyaGusev/saiga_nemo_12b_gguf",
 filename="saiga_nemo_12b.Q4_K_S.gguf",
    verbose=False,
    n_gpu_lчayers=-1,
    n_ctx=1024
)



from application import routes