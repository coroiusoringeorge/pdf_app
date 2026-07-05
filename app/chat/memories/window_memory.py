from langchain.memory import ConversationBufferWindowMemory
from app.chat.memories.histories.sql_history import SqlMessageHistory

# Build the window buffer memory for the given chat arguments
def window_buffer_memory_builder(chat_args):
    # Build the window buffer memory for the given chat arguments
    return ConversationBufferWindowMemory(
        memory_key="chat_history",
        output_key="answer",
        return_messages=True,
        chat_memory=SqlMessageHistory(
            conversation_id=chat_args.conversation_id
        ),
        k=2 # The number of messages to keep in the window
    )