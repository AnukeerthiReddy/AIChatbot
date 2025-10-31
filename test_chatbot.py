"""
Simple tests for the AI Chatbot
Run with: python test_chatbot.py
"""
from chatbot import ChatBot


def test_initialization():
    """Test chatbot initialization."""
    bot = ChatBot(name="TestBot")
    assert bot.name == "TestBot"
    assert len(bot.conversation_history) == 0
    print("✓ Initialization test passed")


def test_basic_responses():
    """Test basic responses."""
    bot = ChatBot()
    
    # Test hello
    response = bot.get_response("hello")
    assert "hello" in response.lower()
    assert bot.name in response
    
    # Test capabilities
    response = bot.get_response("what can you do?")
    assert "questions" in response.lower() or "help" in response.lower()
    
    # Test thanks
    response = bot.get_response("thanks")
    assert "welcome" in response.lower() or "happy" in response.lower()
    
    print("✓ Basic responses test passed")


def test_conversation_history():
    """Test conversation history tracking."""
    bot = ChatBot()
    
    # Initial history should be empty
    assert len(bot.get_conversation_history()) == 0
    
    # Add some messages
    bot.get_response("hello")
    assert len(bot.get_conversation_history()) == 2  # user + bot
    
    bot.get_response("how are you")
    assert len(bot.get_conversation_history()) == 4  # 2 more messages
    
    # Clear history
    bot.clear_history()
    assert len(bot.get_conversation_history()) == 0
    
    print("✓ Conversation history test passed")


def test_fallback_response():
    """Test fallback for unknown inputs."""
    bot = ChatBot()
    
    response = bot.get_response("askdjfhaksjdhfkajsdhf")
    assert len(response) > 0  # Should provide some response
    
    print("✓ Fallback response test passed")


def test_case_insensitivity():
    """Test case-insensitive matching."""
    bot = ChatBot()
    
    response1 = bot.get_response("HELLO")
    response2 = bot.get_response("hello")
    response3 = bot.get_response("HeLLo")
    
    # All should trigger the hello response
    assert "hello" in response1.lower()
    assert "hello" in response2.lower()
    assert "hello" in response3.lower()
    
    print("✓ Case insensitivity test passed")


def run_all_tests():
    """Run all tests."""
    print("Running chatbot tests...\n")
    
    try:
        test_initialization()
        test_basic_responses()
        test_conversation_history()
        test_fallback_response()
        test_case_insensitivity()
        
        print("\n" + "=" * 50)
        print("All tests passed! ✓")
        print("=" * 50)
        return True
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return False
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
