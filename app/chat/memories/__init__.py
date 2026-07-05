from .sql_memory import build_memory
from .window_memory import window_buffer_memory_builder
  
# The memory map is a dictionary that maps the memory type to the function that builds the memory
memory_map = {
    "sql_buffer_memory": build_memory, # Build the SQL buffer memory
    "sql_window_memory": window_buffer_memory_builder # Build the SQL window memory
}