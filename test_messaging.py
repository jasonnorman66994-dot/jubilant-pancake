"""
Tests for the messaging system with timely reply feature.
"""
import unittest
import time
from datetime import datetime, timedelta
from messaging import Message, TimelyReply


class TestMessage(unittest.TestCase):
    """Test cases for the Message class."""
    
    def test_message_creation(self):
        """Test creating a message."""
        msg = Message(sender="Alice", content="Hello!")
        self.assertEqual(msg.sender, "Alice")
        self.assertEqual(msg.content, "Hello!")
        self.assertIsNotNone(msg.timestamp)
        self.assertFalse(msg.replied)
        
    def test_message_with_custom_timestamp(self):
        """Test creating a message with a custom timestamp."""
        custom_time = datetime(2026, 1, 1, 12, 0, 0)
        msg = Message(sender="Bob", content="Hi", timestamp=custom_time)
        self.assertEqual(msg.timestamp, custom_time)


class TestTimelyReply(unittest.TestCase):
    """Test cases for the TimelyReply class."""
    
    def test_receive_message(self):
        """Test receiving a message."""
        reply_handler = TimelyReply()
        msg = Message(sender="Alice", content="Hello!")
        reply_handler.receive_message(msg)
        self.assertEqual(len(reply_handler.messages), 1)
        self.assertEqual(reply_handler.messages[0], msg)
        
    def test_should_auto_reply_immediate(self):
        """Test that auto-reply is not triggered immediately."""
        reply_handler = TimelyReply(reply_timeout_seconds=1.0)
        msg = Message(sender="Alice", content="Hello!")
        reply_handler.receive_message(msg)
        self.assertFalse(reply_handler.should_auto_reply(msg))
        
    def test_should_auto_reply_after_timeout(self):
        """Test that auto-reply is triggered after timeout."""
        reply_handler = TimelyReply(reply_timeout_seconds=0.5)
        # Create a message with a timestamp in the past
        past_time = datetime.now() - timedelta(seconds=1)
        msg = Message(sender="Alice", content="Hello!", timestamp=past_time)
        reply_handler.receive_message(msg)
        self.assertTrue(reply_handler.should_auto_reply(msg))
        
    def test_should_not_auto_reply_if_already_replied(self):
        """Test that auto-reply is not sent to already replied messages."""
        reply_handler = TimelyReply(reply_timeout_seconds=0.5)
        past_time = datetime.now() - timedelta(seconds=1)
        msg = Message(sender="Alice", content="Hello!", timestamp=past_time)
        msg.replied = True
        reply_handler.receive_message(msg)
        self.assertFalse(reply_handler.should_auto_reply(msg))
        
    def test_send_reply(self):
        """Test sending a reply to a message."""
        reply_handler = TimelyReply()
        msg = Message(sender="Alice", content="Hello!")
        reply = reply_handler.send_reply(msg)
        
        self.assertEqual(reply.sender, "AutoReply")
        self.assertEqual(reply.content, reply_handler.auto_reply_template)
        self.assertTrue(msg.replied)
        
    def test_send_custom_reply(self):
        """Test sending a custom reply."""
        reply_handler = TimelyReply()
        msg = Message(sender="Alice", content="Hello!")
        custom_content = "Thanks for reaching out!"
        reply = reply_handler.send_reply(msg, reply_content=custom_content)
        
        self.assertEqual(reply.content, custom_content)
        self.assertTrue(msg.replied)
        
    def test_process_pending_messages(self):
        """Test processing pending messages."""
        reply_handler = TimelyReply(reply_timeout_seconds=0.5)
        
        # Add an old message that needs auto-reply
        past_time = datetime.now() - timedelta(seconds=1)
        old_msg = Message(sender="Alice", content="Old message", timestamp=past_time)
        reply_handler.receive_message(old_msg)
        
        # Add a new message that doesn't need auto-reply yet
        new_msg = Message(sender="Bob", content="New message")
        reply_handler.receive_message(new_msg)
        
        replies = reply_handler.process_pending_messages()
        
        self.assertEqual(len(replies), 1)
        self.assertTrue(old_msg.replied)
        self.assertFalse(new_msg.replied)
        
    def test_get_pending_messages(self):
        """Test getting pending messages."""
        reply_handler = TimelyReply()
        
        msg1 = Message(sender="Alice", content="Message 1")
        msg2 = Message(sender="Bob", content="Message 2")
        msg2.replied = True
        msg3 = Message(sender="Charlie", content="Message 3")
        
        reply_handler.receive_message(msg1)
        reply_handler.receive_message(msg2)
        reply_handler.receive_message(msg3)
        
        pending = reply_handler.get_pending_messages()
        
        self.assertEqual(len(pending), 2)
        self.assertIn(msg1, pending)
        self.assertIn(msg3, pending)
        self.assertNotIn(msg2, pending)


if __name__ == '__main__':
    unittest.main()
