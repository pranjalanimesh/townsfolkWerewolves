from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")
azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
azure_api_version = os.getenv("AZURE_OPENAI_API_VERSION")
chat_model_name = "GPT35-turboA"

# print(f"azure_api: {azure_api_key}")
# print(f"azure_endpoint: {azure_endpoint}")
# print(f"azure_api_version: {azure_api_version}")

# Set the environment variables for the Azure OpenAI service
os.environ["OPENAI_API_VERSION"] = azure_api_version
os.environ["AZURE_OPENAI_ENDPOINT"] = azure_endpoint
os.environ["AZURE_OPENAI_API_KEY"] = azure_api_key

# # Initialize LangSmith
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_PROJECT"] = "Langchain Agent Demo"


from langchain_openai import AzureChatOpenAI

model = AzureChatOpenAI(
    deployment_name=chat_model_name,
    temperature='0.1'
)

if __name__ == "__main__":
    print("Loaded environment variables")
    print(f"Azure API Key: {azure_api_key}")
    print(f"Azure Endpoint: {azure_endpoint}")
    print(f"Azure API Version: {azure_api_version}")
    print(f"Chat Model Name: {chat_model_name}")
    print(f"LangSmith API Key: {os.getenv('LANGCHAIN_API_KEY')}")
    print(f"LangSmith Project: {os.getenv('LANGCHAIN_PROJECT')}")