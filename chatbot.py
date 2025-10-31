"""
AI Chatbot - Core chatbot functionality
This module provides the core chatbot logic with AI integration.
"""
import os
from typing import List, Dict, Optional
import json


class ChatBot:
    """
    A simple AI-based chatbot that uses pattern matching and context awareness.
    This is a rule-based chatbot that can be extended with OpenAI API integration.
    """
    
    def __init__(self, name: str = "AI Assistant"):
        """
        Initialize the chatbot with a name and knowledge base.
        
        Args:
            name: The name of the chatbot
        """
        self.name = name
        self.conversation_history: List[Dict[str, str]] = []
        self.knowledge_base = self._load_knowledge_base()
        
    def _load_knowledge_base(self) -> Dict[str, str]:
        """Load the knowledge base with predefined responses."""
        return {
            "hello": "Hello! I'm {}, your AI assistant. How can I help you today?",
            "hi": "Hi there! I'm {} and I'm here to help. What can I do for you?",
            "how are you": "I'm doing great, thank you for asking! I'm here and ready to assist you.",
            "what is your name": "My name is {}. I'm an AI chatbot designed to help you with various tasks.",
            "who are you": "I am {}, an AI-powered chatbot. I'm here to answer your questions and assist you.",
            "help": "I can help you with various topics. Just ask me a question and I'll do my best to assist you!",
            "bye": "Goodbye! It was nice talking to you. Have a great day!",
            "goodbye": "Farewell! Feel free to come back if you need any help in the future.",
            "thank you": "You're welcome! Is there anything else I can help you with?",
            "thanks": "Happy to help! Let me know if you need anything else.",
            "what can you do": "I can answer questions, have conversations, and help you with various topics. Try asking me anything!",
            "tell me a joke": "Why did the chatbot go to therapy? Because it had too many issues to resolve! 😄",
        }
    
    def get_response(self, user_input: str) -> str:
        """
        Generate a response to the user's input.
        
        Args:
            user_input: The user's message
            
        Returns:
            The chatbot's response
        """
        # Store the conversation
        self.conversation_history.append({
            "role": "user",
            "content": user_input
        })
        
        # Convert input to lowercase for matching
        user_input_lower = user_input.lower().strip()
        
        # Check for exact matches in knowledge base
        if user_input_lower in self.knowledge_base:
            response = self.knowledge_base[user_input_lower].format(self.name)
        # Check for partial matches
        else:
            response = self._find_best_match(user_input_lower)
        
        # Store the response
        self.conversation_history.append({
            "role": "assistant",
            "content": response
        })
        
        return response
    
    def _find_best_match(self, user_input: str) -> str:
        """
        Find the best matching response from the knowledge base.
        
        Args:
            user_input: The user's message in lowercase
            
        Returns:
            The best matching response or a default response
        """
        # Check if any keyword from knowledge base is in user input
        for key, value in self.knowledge_base.items():
            if key in user_input:
                return value.format(self.name)
        
        # Context-aware responses
        if "?" in user_input:
            return "That's an interesting question! While I may not have all the answers, I'm here to help. Could you rephrase or ask something else?"
        
        # Default response
        return f"I understand you're saying: '{user_input}'. I'm still learning, but I'll do my best to help. Can you tell me more or ask in a different way?"
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """
        Get the full conversation history.
        
        Returns:
            List of conversation messages
        """
        return self.conversation_history
    
    def clear_history(self):
        """Clear the conversation history."""
        self.conversation_history = []
    
    def save_conversation(self, filename: str):
        """
        Save the conversation history to a file.
        
        Args:
            filename: Path to save the conversation
        """
        with open(filename, 'w') as f:
            json.dump(self.conversation_history, f, indent=2)
    
    def load_conversation(self, filename: str):
        """
        Load a conversation history from a file.
        
        Args:
            filename: Path to load the conversation from
        """
        with open(filename, 'r') as f:
            self.conversation_history = json.load(f)


class OpenAIChatBot(ChatBot):
    """
    An advanced chatbot using OpenAI's API.
    Requires OPENAI_API_KEY environment variable.
    """
    
    def __init__(self, name: str = "AI Assistant", model: str = "gpt-3.5-turbo"):
        """
        Initialize the OpenAI chatbot.
        
        Args:
            name: The name of the chatbot
            model: The OpenAI model to use
        """
        super().__init__(name)
        self.model = model
        self.use_openai = False
        
        # Try to initialize OpenAI
        try:
            import openai
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key:
                self.client = openai.OpenAI(api_key=api_key)
                self.use_openai = True
            else:
                print("Note: OPENAI_API_KEY not found. Using rule-based responses.")
        except ImportError:
            print("Note: OpenAI library not installed. Using rule-based responses.")
    
    def get_response(self, user_input: str) -> str:
        """
        Generate a response using OpenAI API if available, otherwise use rule-based.
        
        Args:
            user_input: The user's message
            
        Returns:
            The chatbot's response
        """
        if not self.use_openai:
            return super().get_response(user_input)
        
        # Store the user input
        self.conversation_history.append({
            "role": "user",
            "content": user_input
        })
        
        try:
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": f"You are {self.name}, a helpful AI assistant."},
                    *self.conversation_history
                ],
                max_tokens=150,
                temperature=0.7
            )
            
            assistant_message = response.choices[0].message.content
            
            # Store the response
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            return assistant_message
            
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            # Fallback to rule-based response
            self.conversation_history.pop()  # Remove the user message we just added
            return super().get_response(user_input)
