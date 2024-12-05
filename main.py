import os

from flask import Flask, request, jsonify
from llama_index.core import load_index_from_storage, StorageContext

from llama_index.llms.gemini import Gemini
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings

from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.node_parser import TokenTextSplitter

google_api_key = os.getenv("GOOGLE_API_KEY")

if not google_api_key:
    raise Exception("MISSING GOOGLE API KEY!")


llm = Gemini(
    model="models/gemini-1.5-flash",
    temperature=0.3,
    top_p=1,
    top_k=32,
    api_key=google_api_key,
)

embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
text_splitter = SentenceSplitter(chunk_size=1024, chunk_overlap=20)
splitter = TokenTextSplitter(chunk_size=1024, chunk_overlap=20)


Settings.llm = llm
Settings.embed_model = embed_model
Settings.text_splitter = text_splitter
index = load_index_from_storage(StorageContext.from_defaults(persist_dir="./storage"))

query_engine = index.as_query_engine()

app = Flask(__name__)


def generate_bdd_scenario_template(provider, service):
    # Define the template for your prompt
    template = f"""
You are an expert in cloud infrastructure security, focused on writing Behavior-Driven Development (BDD) scenarios
to mitigate common vulnerabilities in Terraform configurations. Your task is to generate BDD scenarios in Gherkin syntax
specifically for the {service} resource provided by {provider}.

For each scenario, identify a potential security vulnerability and then describe expected secure behavior using the BDD format below:

- Given (the initial context or configuration)
- When (an action occurs)
- Then (the expected secure outcome)

Output each scenario in Gherkin syntax.
    """
    return template


# Define the POST endpoint
@app.route("/generate_scenario_v2", methods=["POST"])
def generate_scenario_v2():
    data = request.get_json()
    provider = data.get("provider")
    service = data.get("resource")

    if not provider or not service:
        return jsonify(
            {"error": "Both 'provider' and 'resource' are required fields"}
        ), 400

    response = query_engine.query(generate_bdd_scenario_template(provider, service))

    return str(response)


# Define the POST endpoint
@app.route("/generate_scenario", methods=["POST"])
def generate_scenario():
    data = request.get_json()
    provider = data.get("provider")
    service = data.get("resource")

    if not provider or not service:
        return jsonify(
            {"error": "Both 'provider' and 'resource' are required fields"}
        ), 400

    response = llm.complete(generate_bdd_scenario_template(provider, service))

    return str(response)


# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
