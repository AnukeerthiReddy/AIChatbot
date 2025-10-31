"""
Command-line interface for the AI Chatbot
"""
import argparse
import sys
from chatbot import ChatBot, OpenAIChatBot
from dotenv import load_dotenv


def print_welcome():
    """Print welcome message."""
    print("=" * 60)
    print("Welcome to AI Chatbot!")
    print("=" * 60)
    print("Type 'quit' or 'exit' to end the conversation")
    print("Type 'clear' to clear conversation history")
    print("Type 'history' to view conversation history")
    print("=" * 60)
    print()


def print_message(role: str, message: str):
    """
    Print a formatted message.
    
    Args:
        role: The role (user or bot)
        message: The message to print
    """
    if role == "user":
        print(f"You: {message}")
    else:
        print(f"Bot: {message}")
    print()


def run_cli(use_openai: bool = False, bot_name: str = "AI Assistant"):
    """
    Run the command-line interface for the chatbot.
    
    Args:
        use_openai: Whether to use OpenAI API
        bot_name: Name of the chatbot
    """
    # Load environment variables
    load_dotenv()
    
    # Initialize chatbot
    if use_openai:
        bot = OpenAIChatBot(name=bot_name)
    else:
        bot = ChatBot(name=bot_name)
    
    print_welcome()
    
    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            # Check for special commands
            if user_input.lower() in ['quit', 'exit']:
                print_message("bot", "Goodbye! Thanks for chatting with me.")
                break
            
            elif user_input.lower() == 'clear':
                bot.clear_history()
                print("Conversation history cleared.")
                print()
                continue
            
            elif user_input.lower() == 'history':
                print("\n--- Conversation History ---")
                history = bot.get_conversation_history()
                if not history:
                    print("No conversation history yet.")
                else:
                    for msg in history:
                        role = "You" if msg["role"] == "user" else "Bot"
                        print(f"{role}: {msg['content']}")
                print("--- End of History ---\n")
                continue
            
            # Get bot response
            response = bot.get_response(user_input)
            print_message("bot", response)
            
        except KeyboardInterrupt:
            print("\n\nGoodbye! Thanks for chatting with me.")
            break
        except EOFError:
            print("\n\nGoodbye! Thanks for chatting with me.")
            break
        except Exception as e:
            print(f"\nError: {e}")
            print("Please try again.\n")


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(description="AI Chatbot - Command Line Interface")
    parser.add_argument(
        "--openai",
        action="store_true",
        help="Use OpenAI API (requires OPENAI_API_KEY environment variable)"
    )
    parser.add_argument(
        "--name",
        type=str,
        default="AI Assistant",
        help="Name of the chatbot (default: AI Assistant)"
    )
    
    args = parser.parse_args()
    
    run_cli(use_openai=args.openai, bot_name=args.name)


if __name__ == "__main__":
    main()
