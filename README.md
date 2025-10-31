# AI Chatbot

An intelligent, AI-based chatbot with both command-line and web interfaces. This chatbot can engage in conversations using rule-based responses or integrate with OpenAI's API for more advanced interactions.

## Features

- 🤖 **Intelligent Conversations**: Engage in natural conversations with context awareness
- 💻 **Command-Line Interface**: Simple CLI for terminal-based interactions
- 🌐 **Web Interface**: Beautiful, modern web UI built with Flask
- 🧠 **Dual Mode Operation**: 
  - Rule-based responses (works out of the box)
  - OpenAI API integration (optional, requires API key)
- 📝 **Conversation History**: Track and save conversation sessions
- 🎨 **Responsive Design**: Mobile-friendly web interface
- 🔒 **Session Management**: Separate conversations for different users

## Installation

1. Clone the repository:
```bash
git clone https://github.com/AnukeerthiReddy/AIChatbot.git
cd AIChatbot
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Set up OpenAI API:
```bash
# Create a .env file and add your OpenAI API key
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

## Usage

### Command-Line Interface

Run the chatbot in your terminal:

```bash
# Basic usage (rule-based)
python cli.py

# With OpenAI API
python cli.py --openai

# Custom bot name
python cli.py --name "MyBot"
```

**CLI Commands:**
- Type your message and press Enter to chat
- `quit` or `exit` - End the conversation
- `clear` - Clear conversation history
- `history` - View conversation history

### Web Interface

Start the web server:

```bash
python app.py
```

Then open your browser and navigate to:
```
http://localhost:5000
```

The web interface provides:
- Real-time chat interface
- Message history
- Clear conversation button
- Typing indicators
- Responsive design for mobile devices

## Project Structure

```
AIChatbot/
├── chatbot.py          # Core chatbot logic
├── cli.py              # Command-line interface
├── app.py              # Flask web application
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (create this)
├── .gitignore         # Git ignore rules
├── templates/
│   └── index.html     # Web interface HTML
├── static/
│   ├── style.css      # Web interface styles
│   └── script.js      # Web interface JavaScript
└── README.md          # This file
```

## How It Works

### Rule-Based Mode (Default)

The chatbot uses a knowledge base of predefined responses to handle common queries:
- Greetings (hello, hi, how are you)
- Questions about the bot (who are you, what can you do)
- Gratitude (thank you, thanks)
- Farewells (bye, goodbye)
- And more...

For queries not in the knowledge base, it provides intelligent fallback responses.

### OpenAI Mode (Optional)

When configured with an OpenAI API key, the chatbot uses GPT-3.5-turbo for more advanced, context-aware responses. This mode:
- Understands complex queries
- Maintains conversation context
- Provides more natural, human-like responses
- Falls back to rule-based mode if API calls fail

## Example Conversations

**Example 1 - Basic Interaction:**
```
You: Hello
Bot: Hello! I'm AI Assistant, your AI assistant. How can I help you today?

You: What can you do?
Bot: I can answer questions, have conversations, and help you with various topics. Try asking me anything!

You: Tell me a joke
Bot: Why did the chatbot go to therapy? Because it had too many issues to resolve! 😄
```

**Example 2 - With OpenAI:**
```
You: What's the capital of France?
Bot: The capital of France is Paris. It's a beautiful city known for its art, culture, and landmarks like the Eiffel Tower.

You: How many people live there?
Bot: Paris has a population of approximately 2.1 million people within the city limits, and about 12 million in the greater metropolitan area.
```

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Optional: OpenAI API Key for advanced AI features
OPENAI_API_KEY=sk-your-api-key-here
```

### Customization

You can customize the chatbot by modifying:

- `chatbot.py` - Add more responses to the knowledge base
- `templates/index.html` - Modify the web interface layout
- `static/style.css` - Change the appearance and styling
- `static/script.js` - Add new frontend features

## Dependencies

- **Flask** (3.0.0) - Web framework
- **OpenAI** (1.3.0) - AI integration (optional)
- **python-dotenv** (1.0.0) - Environment variable management

## Requirements

- Python 3.7 or higher
- pip (Python package manager)

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

## Future Enhancements

Potential improvements for future versions:
- Voice input/output
- Multi-language support
- Integration with other AI services
- Database storage for conversations
- User authentication
- Chat export functionality
- Sentiment analysis
- Custom training on specific domains

---

**Enjoy chatting with your AI assistant! 🤖**
