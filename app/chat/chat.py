import random
from langchain.chat_models import ChatOpenAI
from app.chat.models import ChatArgs
from app.chat.vector_stores import retriever_map
from app.chat.llms import llm_map
from app.chat.memories import memory_map
from app.chat.chains.retrieval import StreamingConversationalRetrievalChain
from app.web.api import (
    set_conversation_components,
    get_conversation_components
)
from app.chat.score import random_component_by_score
from app.chat.tracking.tracking import langfuse
from langfuse.model import CreateTrace

# Select the component for the given chat arguments
def select_component(
    component_type, component_map, chat_args
):
    # Get the components for the given conversation id
    components = get_conversation_components(
        chat_args.conversation_id
    )
    # Get the previous component for the given component type
    previous_component = components[component_type]
    # If the previous component is not None, return the previous component and the builder
    # Otherwise, select a random component and return the random component and the builder
    if previous_component:
        builder = component_map[previous_component]
        return previous_component, builder(chat_args)
    else:
        random_name = random_component_by_score(component_type, component_map)
        builder = component_map[random_name]
        return random_name, builder(chat_args)

# Build the chat for the given chat arguments
def build_chat(chat_args: ChatArgs):
    # Select the retriever for the given chat arguments
    retriever_name, retriever = select_component(
        "retriever",
        retriever_map,
        chat_args
    )
    # Select the LLM for the given chat arguments
    llm_name, llm = select_component(
        "llm",
        llm_map,
        chat_args
    )
    # Select the memory for the given chat arguments
    memory_name, memory = select_component(
        "memory",
        memory_map,
        chat_args
    )
    set_conversation_components(
        chat_args.conversation_id,
        llm=llm_name,
        retriever=retriever_name,
        memory=memory_name
    )

    # Create a condense question LLM
    condense_question_llm = ChatOpenAI(streaming=False)

    # Create a trace for the given conversation id
    trace = langfuse.trace(
        CreateTrace(
            id=chat_args.conversation_id,
            metadata=chat_args.metadata,
        )
    )
    # Return the streaming conversational retrieval chain
    return StreamingConversationalRetrievalChain.from_llm(
        llm=llm,
        condense_question_llm=condense_question_llm,
        memory=memory,
        retriever=retriever,
        callbacks=[trace.getNewHandler()]
    )
