"""
Web interface for the AI Chatbot using Flask
"""
from flask import Flask, render_template, request, jsonify, session
import secrets
import os
from chatbot import ChatBot, OpenAIChatBot
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Store chatbot instances per session
chatbots = {}


def get_chatbot(session_id: str, use_openai: bool = False):
    """
    Get or create a chatbot instance for the session.
    
    Args:
        session_id: The session identifier
        use_openai: Whether to use OpenAI API
        
    Returns:
        ChatBot instance
    """
    if session_id not in chatbots:
        if use_openai:
            chatbots[session_id] = OpenAIChatBot()
        else:
            chatbots[session_id] = ChatBot()
    return chatbots[session_id]


@app.route('/')
def index():
    """Render the main chat interface."""
    if 'session_id' not in session:
        session['session_id'] = secrets.token_hex(16)
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    """
    Handle chat messages from the user.
    
    Returns:
        JSON response with the bot's reply
    """
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Empty message'}), 400
        
        # Get session ID
        session_id = session.get('session_id', secrets.token_hex(16))
        session['session_id'] = session_id
        
        # Check if OpenAI should be used
        use_openai = os.getenv('OPENAI_API_KEY') is not None
        
        # Get chatbot and generate response
        bot = get_chatbot(session_id, use_openai=use_openai)
        response = bot.get_response(user_message)
        
        return jsonify({
            'response': response,
            'status': 'success'
        })
    
    except Exception as e:
        # Log error internally but don't expose details to user
        print(f"Error in chat endpoint: {e}")
        return jsonify({
            'error': 'An error occurred while processing your message',
            'status': 'error'
        }), 500


@app.route('/clear', methods=['POST'])
def clear():
    """Clear the conversation history for the current session."""
    try:
        session_id = session.get('session_id')
        if session_id and session_id in chatbots:
            chatbots[session_id].clear_history()
            return jsonify({
                'status': 'success',
                'message': 'Conversation history cleared'
            })
        return jsonify({
            'status': 'success',
            'message': 'No conversation to clear'
        })
    except Exception as e:
        # Log error internally but don't expose details to user
        print(f"Error in clear endpoint: {e}")
        return jsonify({
            'error': 'An error occurred while clearing conversation',
            'status': 'error'
        }), 500


@app.route('/history', methods=['GET'])
def history():
    """Get the conversation history for the current session."""
    try:
        session_id = session.get('session_id')
        if session_id and session_id in chatbots:
            bot = chatbots[session_id]
            return jsonify({
                'history': bot.get_conversation_history(),
                'status': 'success'
            })
        return jsonify({
            'history': [],
            'status': 'success'
        })
    except Exception as e:
        # Log error internally but don't expose details to user
        print(f"Error in history endpoint: {e}")
        return jsonify({
            'error': 'An error occurred while loading history',
            'status': 'error'
        }), 500


if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    # Run the app (debug mode should be disabled in production)
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
