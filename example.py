#!/usr/bin/env python3
"""
Example usage of the timely reply messaging system.
"""
import time
from datetime import datetime, timedelta
from messaging import Message, TimelyReply


def main():
    print("=== Timely Reply Messaging System Demo ===\n")
    
    # Create a timely reply handler with 2-second timeout
    reply_handler = TimelyReply(reply_timeout_seconds=2.0)
    
    # Simulate receiving messages
    print("1. Receiving messages...")
    msg1 = Message(sender="Alice", content="Hi, I have a question about the product.")
    reply_handler.receive_message(msg1)
    print(f"   Received: {msg1.content}")
    
    msg2 = Message(sender="Bob", content="When will my order arrive?")
    reply_handler.receive_message(msg2)
    print(f"   Received: {msg2.content}")
    
    # Check pending messages immediately
    print(f"\n2. Pending messages: {len(reply_handler.get_pending_messages())}")
    
    # Wait a bit but not long enough for auto-reply
    print("\n3. Waiting 1 second...")
    time.sleep(1)
    
    # Process messages - should not trigger auto-reply yet
    replies = reply_handler.process_pending_messages()
    print(f"   Auto-replies sent: {len(replies)}")
    
    # Wait long enough for auto-reply
    print("\n4. Waiting another 2 seconds...")
    time.sleep(2)
    
    # Process messages - should trigger auto-replies
    replies = reply_handler.process_pending_messages()
    print(f"   Auto-replies sent: {len(replies)}")
    for reply in replies:
        print(f"   -> {reply.content}")
    
    # Check pending messages after auto-reply
    print(f"\n5. Pending messages after auto-reply: {len(reply_handler.get_pending_messages())}")
    
    # Simulate receiving a new message and manually replying
    print("\n6. Receiving new message and sending manual reply...")
    msg3 = Message(sender="Charlie", content="I need help!")
    reply_handler.receive_message(msg3)
    print(f"   Received: {msg3.content}")
    
    manual_reply = reply_handler.send_reply(msg3, reply_content="I'm here to help! What do you need?")
    print(f"   Manual reply sent: {manual_reply.content}")
    
    # Try to process - should not send another auto-reply
    replies = reply_handler.process_pending_messages()
    print(f"   Additional auto-replies: {len(replies)}")
    
    print("\n=== Demo Complete ===")


if __name__ == '__main__':
    main()
