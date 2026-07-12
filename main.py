from src.llm.ollama_loader import get_llm

def test_llm_connection():
    llm = get_llm()
    response = llm.invoke("Who are you?")
    print(response.content)

def main():
    print("Helios has initialized.")
    print("llm connection test: ")
    test_llm_connection()

if __name__ == "__main__":
    main()