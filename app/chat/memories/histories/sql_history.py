from pydantic import BaseModel
from langchain.schema import BaseChatMessageHistory

from app.web.api import add_message_to_conversation, get_messages_by_conversation_id

# SQL Message History
class SqlMessageHistory(BaseChatMessageHistory, BaseModel):
    conversation_id: str

    # Get the messages for the given conversation id
    @property
    def messages(self):
        return get_messages_by_conversation_id(self.conversation_id)
    
    # Add a message to the given conversation id
    def add_message(self, message):
        # Add the message to the conversation
        return add_message_to_conversation(
            conversation_id=self.conversation_id,
            role=message.type,
            content=message.content
        )

    # Clear the messages for the given conversation id
    def clear(self):
        pass