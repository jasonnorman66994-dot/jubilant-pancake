"""
Simple messaging system with timely reply feature.
"""
import time
from datetime import datetime, timedelta
from typing import Optional, List


class Message:
    """Represents a message in the messaging system."""
    
    def __init__(self, sender: str, content: str, timestamp: Optional[datetime] = None):
        """
        Initialize a message.
        
        Args:
            sender: The sender of the message
            content: The content of the message
            timestamp: When the message was sent (defaults to current time)
        """
        self.sender = sender
        self.content = content
        self.timestamp = timestamp or datetime.now()
        self.replied = False
        
    def __repr__(self):
        return f"Message(sender='{self.sender}', content='{self.content}', timestamp={self.timestamp})"


class TimelyReply:
    """
    Handles automatic timely replies to messages.
    
    This class monitors messages and sends automatic replies
    within a specified timeframe if no manual reply is sent.
    """
    
    def __init__(self, reply_timeout_seconds: float = 5.0):
        """
        Initialize the timely reply handler.
        
        Args:
            reply_timeout_seconds: Maximum time to wait before sending an auto-reply
        """
        self.reply_timeout_seconds = reply_timeout_seconds
        self.messages: List[Message] = []
        self.auto_reply_template = "Thank you for your message. I'll get back to you shortly."
        
    def receive_message(self, message: Message) -> None:
        """
        Receive a new message.
        
        Args:
            message: The message to receive
        """
        self.messages.append(message)
        
    def should_auto_reply(self, message: Message) -> bool:
        """
        Check if a message should receive an auto-reply.
        
        Args:
            message: The message to check
            
        Returns:
            True if an auto-reply should be sent, False otherwise
        """
        if message.replied:
            return False
            
        time_since_received = (datetime.now() - message.timestamp).total_seconds()
        return time_since_received >= self.reply_timeout_seconds
        
    def send_reply(self, message: Message, reply_content: Optional[str] = None) -> Message:
        """
        Send a reply to a message.
        
        Args:
            message: The message to reply to
            reply_content: The content of the reply (uses auto-reply template if None)
            
        Returns:
            The reply message
        """
        if reply_content is None:
            reply_content = self.auto_reply_template
            
        reply = Message(
            sender="AutoReply",
            content=reply_content,
            timestamp=datetime.now()
        )
        message.replied = True
        return reply
        
    def process_pending_messages(self) -> List[Message]:
        """
        Process all pending messages and send auto-replies where needed.
        
        Returns:
            List of auto-reply messages that were sent
        """
        replies = []
        for message in self.messages:
            if self.should_auto_reply(message):
                reply = self.send_reply(message)
                replies.append(reply)
        return replies
        
    def get_pending_messages(self) -> List[Message]:
        """
        Get all messages that haven't been replied to.
        
        Returns:
            List of unreplied messages
        """
        return [msg for msg in self.messages if not msg.replied]
