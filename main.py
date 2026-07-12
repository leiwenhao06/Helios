from src.llm.ollama_loader import get_llm
from src.memory.short_term import get_short_term_memory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory

def main():
    print("[Helios] 短期记忆测试模式，输入 'exit' 退出")

    llm = get_llm()
    memory = get_short_term_memory()

    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个名为 Helios 的智能助手，请用简洁的中文回答。"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ])

    chain = prompt | llm

    # 为 RunnableWithMessageHistory 提供可调用的历史工厂
    def get_session_history(session_id: str):
        return memory

    chain_with_history = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
    )

    while True:
        user_input = input("你: ")
        if user_input.lower() == "exit":
            break

        response = chain_with_history.invoke(
            {"input": user_input},
            config={"configurable": {"session_id": "default"}},
        )
        print(f"[Helios]: {response.content}")

if __name__ == "__main__":
    main()