from dotenv import load_dotenv
import os
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

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

model = AzureChatOpenAI(
    deployment_name=chat_model_name,
    temperature='0.1'
)

def completion(messages, max_tokens=50, temperature=0.0):
    model = AzureChatOpenAI(
        deployment_name=chat_model_name,
        temperature=temperature,
        max_tokens=max_tokens
    )

    human = HumanMessage(content=messages['user'])
    system = SystemMessage(content=messages['system'])

    completion = model.invoke([system, human])
    return completion.content

if __name__ == "__main__":
    print("Loaded environment variables")
    print(f"Azure API Key: {azure_api_key}")
    print(f"Azure Endpoint: {azure_endpoint}")
    print(f"Azure API Version: {azure_api_version}")
    print(f"Chat Model Name: {chat_model_name}")
    print(f"LangSmith API Key: {os.getenv('LANGCHAIN_API_KEY')}")
    print(f"LangSmith Project: {os.getenv('LANGCHAIN_PROJECT')}")

    com = completion({
        'user': 'What is the meaning of life?',
    'system': 'The meaning of life is to live and learn. Output only this and nothing else. DO NOT OUTPUT ANYTHING ELSE.'
    }, max_tokens=100, temperature=0.0)