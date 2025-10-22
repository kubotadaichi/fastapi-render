from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")



def get_gemini_response(prompt: str ) -> str:
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )

    response = llm.invoke(prompt)
    return response

def get_answer_from_gemini(messages) -> str:
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )

    prompt = messages = [
    (
        "system",
        "You are a helpful assistant. サッカーのことについて詳しく、とても喋りたがりです。",
    ),
    ("human", messages),
    ]

    response = llm.invoke(prompt)
    return response.content

if __name__ == "__main__":
    prompt = "こんにちは、元気ですか？"
    print(get_answer_from_gemini(prompt))

