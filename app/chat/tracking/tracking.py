import os
from langfuse.client import Langfuse

# Connects to the Langfuse server
langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host="https://prod-langfuse.fly.dev"
)