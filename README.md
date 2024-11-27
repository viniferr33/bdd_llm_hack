# Terraform BDD Scenario Generator API

This Flask API generates Behavior-Driven Development (BDD) scenarios in Gherkin syntax for cloud infrastructure security. The API leverages **Gemini 1.5 Flash** for natural language generation and a pre-built vector index for document querying.

## Features

- Generates Gherkin-based BDD scenarios for Terraform configurations.
- Accepts cloud `provider` and `service` as inputs.
- Uses a pre-persisted vector index and **Gemini 1.5 Flash** LLM for responses.

## Requirements

- Python 3.8+
- A `GOOGLE_API_KEY` environment variable with access to **Gemini 1.5 Flash**.
- Pre-built index stored in the `./storage` directory.

## Setup

### Prerequisites

Ensure you have the following installed:

- [Python](https://www.python.org/downloads/)
- [Pip](https://pip.pypa.io/en/stable/installation/)
- [Flask](https://flask.palletsprojects.com/)
- Other Python dependencies listed in the `requirements.txt`.

### Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/your-repository/terraform-bdd-api.git
   cd terraform-bdd-api
   ```

2. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set the Environment Variable**:
   Create a `.env` file in the root directory:

   ```bash
   echo "GOOGLE_API_KEY=your_google_api_key" > .env
   ```

   Replace `your_google_api_key` with your valid API key.

4. **Ensure the Persisted Index**:
   Place the pre-built index files in the `./storage` directory.

### Pre-Built Index

This API relies on a vector index created using `llama-index`. Make sure your `./storage` directory contains the persisted index files (`docstore.json`, `index_store.json`, etc.). Use `StorageContext.from_defaults(persist_dir="./storage")` during indexing.

## Usage

### Running the API

Start the Flask app:

```bash
python app.py
```

The API will run locally at `http://127.0.0.1:5000`.

### Endpoint

#### `POST /generate_scenario`

Generate BDD scenarios for a specified cloud `provider` and `service`.

- **Request**:

  ```json
  {
    "provider": "GCP",
    "service": "Storage Bucket"
  }
  ```

- **Response**:
  Returns a string containing the Gherkin-based BDD scenario.

  **Example**:

  ```json
  Scenario: Mitigating public access vulnerability in Storage Bucket
      Given a configuration for Storage Bucket on GCP
      When permissions are set to allow public access
      Then restrict bucket access to authorized users only to prevent unauthorized access
  ```

### Testing with `curl`

```bash
curl -X POST http://127.0.0.1:5000/generate_scenario      -H "Content-Type: application/json"      -d '{"provider": "AWS", "service": "S3 Bucket"}'
```

## Project Structure

```
├── app.py                 # Flask API implementation
├── storage/               # Persisted index files (pre-built)
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
└── .env                   # Environment variables
```

## Dependencies

- [Flask](https://flask.palletsprojects.com/)
- [llama-index](https://github.com/jerryjliu/llama_index)
- [huggingface/transformers](https://huggingface.co/docs/transformers)
- [dotenv](https://pypi.org/project/python-dotenv/)

## Environment Variables

- `GOOGLE_API_KEY`: Required for **Gemini 1.5 Flash** API access.

## Troubleshooting

1. **Missing API Key**:
   Ensure the `.env` file contains the correct `GOOGLE_API_KEY`.

2. **Index Not Found**:
   Verify the `./storage` directory contains the persisted index files.

3. **Flask Errors**:
   - Ensure all dependencies are installed.
   - Check for typos in the request payload.

## License

This project is licensed under the [MIT License](LICENSE).
