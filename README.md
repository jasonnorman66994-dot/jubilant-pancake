# jubilant-pancake

A simple messaging system with automatic timely reply feature.

## Features

- **Message Management**: Send and receive messages with timestamps
- **Timely Auto-Reply**: Automatically sends replies to messages that haven't been responded to within a configurable timeframe
- **Flexible Configuration**: Customize the auto-reply timeout and message template

## Usage

### Basic Example

```python
from messaging import Message, TimelyReply

# Create a timely reply handler with 5-second timeout
reply_handler = TimelyReply(reply_timeout_seconds=5.0)

# Receive a message
msg = Message(sender="Alice", content="Hello, I need help!")
reply_handler.receive_message(msg)

# Process pending messages (sends auto-replies after timeout)
replies = reply_handler.process_pending_messages()

# Or send a manual reply
manual_reply = reply_handler.send_reply(msg, reply_content="How can I help you?")
```

### Running the Demo

```bash
python example.py
```

### Running Tests

```bash
python -m unittest test_messaging.py
```

## API Reference

### Message

Represents a message in the system.

- `sender`: The sender of the message
- `content`: The message content
- `timestamp`: When the message was sent
- `replied`: Whether the message has been replied to

### TimelyReply

Handles automatic timely replies to messages.

- `__init__(reply_timeout_seconds)`: Create a new handler with specified timeout
- `receive_message(message)`: Receive a new message
- `send_reply(message, reply_content)`: Send a reply (manual or auto)
- `process_pending_messages()`: Process all pending messages and send auto-replies
- `get_pending_messages()`: Get all unreplied messages