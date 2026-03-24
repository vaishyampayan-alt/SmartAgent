"""
main.py — Command-line interface for SmartAgent.

Run with:
    python main.py

Type 'exit' or 'quit' to stop the session.
"""

from agent import build_agent


def main() -> None:
    print("=" * 60)
    print("  SmartAgent 🤖  —  powered by Groq + LangChain")
    print("  Type 'exit' or 'quit' to end the session.")
    print("=" * 60)
    print()

    try:
        agent_executor = build_agent()
    except EnvironmentError as e:
        print(f"[Error] {e}")
        return

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        try:
            response = agent_executor.invoke({"input": user_input})
            print(f"\nSmartAgent: {response['output']}\n")
        except Exception as e:
            print(f"\n[Agent error] {e}\n")


if __name__ == "__main__":
    main()
