# LangChain 1.0 Syntax Guide

This document provides comprehensive syntax examples and patterns for LangChain 1.0, covering the core features and best practices.

## Table of Contents

- [Introduction](#introduction)
- [LCEL (LangChain Expression Language)](#lcel-langchain-expression-language)
- [Prompts and Templates](#prompts-and-templates)
- [Chains](#chains)
- [Agents](#agents)
- [Tools](#tools)
- [Memory](#memory)
- [Structured Output](#structured-output)
- [Streaming](#streaming)
- [RAG (Retrieval-Augmented Generation)](#rag-retrieval-augmented-generation)

---

## Introduction

LangChain 1.0 is a framework for developing applications powered by language models. It provides tools and interfaces for building complex LLM workflows through a declarative expression language.

### Key Changes in LangChain 1.0

- **LCEL (LangChain Expression Language)**: Declarative way to compose chains
- **Unified Agent API**: Simplified agent creation with `create_agent`
- **Structured Output**: Native support for structured data extraction
- **Middleware System**: Flexible way to customize agent behavior
- **Enhanced Streaming**: Better support for streaming responses and tool calls

---

## LCEL (LangChain Expression Language)

LCEL allows you to declaratively define processing pipelines by chaining components together using the pipe operator (`|`).

### Basic Chain

```python
from langchain_core.prompts import PromptTemplate

template = """Question: {question}

Answer: Let's think step by step."""
prompt = PromptTemplate.from_template(template)

chain = prompt | llm

question = "How much is 2+2?"
print(chain.invoke({"question": question}))
```

### Chain with Output Parser

```python
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate.from_template("Tell me a joke about {topic}")
chain = prompt | llm | StrOutputParser()

result = chain.invoke({"topic": "programming"})
print(result)
```

### Chain with RunnablePassthrough

```python
from langchain_core.runnables import RunnablePassthrough

chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)
```

### Parallel Execution

```python
from langchain_core.runnables import RunnableParallel

chain = RunnableParallel(
    summary = prompt1 | llm | StrOutputParser(),
    analysis = prompt2 | llm | StrOutputParser()
)

result = chain.invoke({"text": "Your text here"})
```

---

## Prompts and Templates

### PromptTemplate

```python
from langchain_core.prompts import PromptTemplate

template = """Question: {question}

Answer: Let's think step by step."""
prompt = PromptTemplate.from_template(template)

# Invoke with variables
formatted = prompt.invoke({"question": "What is electroencephalography?"})
```

### ChatPromptTemplate

```python
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that translates {input_language} to {output_language}."),
    ("human", "{text}"),
])

chain = prompt | model | StrOutputParser()

result = chain.invoke({
    "input_language": "English",
    "output_language": "Spanish",
    "text": "Hello, how are you?"
})
print(result)
```

### ChatPromptTemplate with Placeholder

```python
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate(
    [
        ("system", "You are a helpful assistant."),
        ("human", "{user_input}"),
        ("placeholder", "{messages}"),
    ]
)
```

### Dynamic System Prompts with Middleware

```python
from langchain.agents import create_agent
from langchain.agents.middleware import dynamic_prompt, ModelRequest
from typing import TypedDict


class CustomContext(TypedDict):
    user_name: str


@dynamic_prompt
def dynamic_system_prompt(request: ModelRequest) -> str:
    user_name = request.runtime.context["user_name"]
    system_prompt = f"You are a helpful assistant. Address the user as {user_name}."
    return system_prompt


agent = create_agent(
    model="gpt-5-nano",
    tools=[get_weather],
    middleware=[dynamic_system_prompt],
    context_schema=CustomContext,
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What is the weather in SF?"}]},
    context=CustomContext(user_name="John Smith"),
)
```

---

## Chains

### Simple Chain

```python
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt = PromptTemplate.from_template("Tell me a joke about {topic}")
chain = prompt | llm | StrOutputParser()

result = chain.invoke({"topic": "programming"})
```

### RAG Chain

```python
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

prompt = ChatPromptTemplate.from_template(
    """Answer the question based only on the context provided.

Context: {context}

Question: {question}"""
)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)
```

### Tool-Calling Chain

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableConfig, chain

prompt = ChatPromptTemplate(
    [
        ("system", "You are a helpful assistant."),
        ("human", "{user_input}"),
        ("placeholder", "{messages}"),
    ]
)

# Bind tools to model with tool_choice
model_with_tools = model.bind_tools([search_tool], tool_choice=search_tool.name)

model_chain = prompt | model_with_tools


@chain
def tool_chain(user_input: str, config: RunnableConfig):
    input_ = {"user_input": user_input}
    ai_msg = model_chain.invoke(input_, config=config)
    tool_msgs = search_tool.batch(ai_msg.tool_calls, config=config)
    return model_chain.invoke({**input_, "messages": [ai_msg, *tool_msgs]}, config=config)


tool_chain.invoke("Tell me the email addresses from Sophie Müller from Berlin.")
```

---

## Agents

### Basic Agent Creation

```python
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent("openai:gpt-5.2", tools=[get_weather])

result = agent.invoke({
    "messages": [{"role": "user", "content": "What is the weather in Boston?"}]
})
```

### Agent with Memory

```python
from langchain.agents import create_agent
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import MemorySaver

agent = create_agent(
    model="gpt-5",
    tools=[get_weather],
    checkpointer=MemorySaver(),
)

config: RunnableConfig = {"configurable": {"thread_id": "my-session"}}

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What is the weather in Boston?"}]},
    config=config,
)
```

### Agent with Middleware

```python
from langchain.agents import create_agent
from langchain_anthropic.middleware import StateClaudeMemoryMiddleware
from langgraph.checkpoint.memory import MemorySaver

agent = create_agent(
    model=ChatAnthropic(model="claude-sonnet-4-5-20250929"),
    tools=[],
    middleware=[StateClaudeMemoryMiddleware()],
    checkpointer=MemorySaver(),
)

config: RunnableConfig = {"configurable": {"thread_id": "my-session"}}

result = agent.invoke(
    {"messages": [{"role": "user", "content": "Remember that my favorite color is blue, then confirm what you stored."}]},
    config=config,
)
```

### Agent with Multiple Middleware

```python
from langchain_anthropic.middleware import (
    StateClaudeMemoryMiddleware,
    StateFileSearchMiddleware,
)

agent = create_agent(
    model=ChatAnthropic(model="claude-sonnet-4-5-20250929"),
    tools=[],
    middleware=[
        StateClaudeMemoryMiddleware(),
        StateFileSearchMiddleware(state_key="memory_files"),
    ],
    checkpointer=MemorySaver(),
)
```

---

## Tools

### Defining a Simple Tool

```python
def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent("openai:gpt-5.2", tools=[get_weather])
```

### Using Tools with Agents

```python
from langchain.agents import create_agent

def search_database(query: str) -> str:
    """Search the database for information."""
    return f"Results for: {query}"

def calculate(expression: str) -> str:
    """Calculate a mathematical expression."""
    return str(eval(expression))

agent = create_agent(
    model="gpt-5",
    tools=[search_database, calculate],
)
```

### Tool Binding

```python
# Bind tools to model with tool_choice
model_with_tools = model.bind_tools([search_tool], tool_choice=search_tool.name)

# Use in chain
model_chain = prompt | model_with_tools
```

---

## Memory

### Memory with Checkpointer

```python
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver

agent = create_agent(
    model="gpt-5",
    tools=[],
    checkpointer=MemorySaver(),
)

config = {"configurable": {"thread_id": "session-1"}}

# First message
agent.invoke(
    {"messages": [{"role": "user", "content": "My name is Alice"}]},
    config=config,
)

# Second message - agent remembers
agent.invoke(
    {"messages": [{"role": "user", "content": "What's my name?"}]},
    config=config,
)
```

### State-Based Memory Middleware

```python
from langchain_anthropic.middleware import StateClaudeMemoryMiddleware

agent = create_agent(
    model=ChatAnthropic(model="claude-sonnet-4-5-20250929"),
    tools=[],
    middleware=[StateClaudeMemoryMiddleware()],
    checkpointer=MemorySaver(),
)

config = {"configurable": {"thread_id": "my-session"}}

result = agent.invoke(
    {"messages": [{"role": "user", "content": "Remember that my favorite color is blue"}]},
    config=config,
)
```

### Memory File Search

```python
from langchain_anthropic.middleware import (
    StateClaudeMemoryMiddleware,
    StateFileSearchMiddleware,
)

agent = create_agent(
    model=ChatAnthropic(model="claude-sonnet-4-5-20250929"),
    tools=[],
    middleware=[
        StateClaudeMemoryMiddleware(),
        StateFileSearchMiddleware(state_key="memory_files"),
    ],
    checkpointer=MemorySaver(),
)

# Record memories
agent.invoke(
    {"messages": [HumanMessage("Remember that the project deadline is March 15th")]},
    config=config,
)

# Search memories
agent.invoke(
    {"messages": [HumanMessage("What is the project deadline?")]},
    config=config,
)
```

---

## Structured Output

### Using Pydantic Model

```python
from pydantic import BaseModel
from langchain.agents import create_agent


class ContactInfo(BaseModel):
    """Contact information for a person."""
    name: str = Field(description="The name of the person")
    email: str = Field(description="The email address of the person")
    phone: str = Field(description="The phone number of the person")

agent = create_agent(
    model="gpt-5",
    response_format=ContactInfo  # Auto-selects ProviderStrategy
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "Extract contact info from: John Doe, john@example.com, (555) 123-4567"}]
})

print(result["structured_response"])
# ContactInfo(name='John Doe', email='john@example.com', phone='(555) 123-4567')
```

### Using Dataclass

```python
from dataclasses import dataclass


@dataclass
class ContactInfo:
    """Contact information for a person."""
    name: str
    email: str
    phone: str

agent = create_agent(
    model="gpt-5",
    response_format=ContactInfo
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "Extract contact info from: John Doe, john@example.com, (555) 123-4567"}]
})

result["structured_response"]
```

### Using TypedDict

```python
from typing_extensions import TypedDict


class ContactInfo(TypedDict):
    """Contact information for a person."""
    name: str
    email: str
    phone: str

agent = create_agent(
    model="gpt-5",
    response_format=ContactInfo
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "Extract contact info from: John Doe, john@example.com, (555) 123-4567"}]
})

result["structured_response"]
# {'name': 'John Doe', 'email': 'john@example.com', 'phone': '(555) 123-4567'}
```

### Using JSON Schema

```python
from langchain.agents import create_agent


contact_info_schema = {
    "type": "object",
    "description": "Contact information for a person.",
    "properties": {
        "name": {"type": "string", "description": "The name of the person"},
        "email": {"type": "string", "description": "The email address of the person"},
        "phone": {"type": "string", "description": "The phone number of the person"}
    },
    "required": ["name", "email", "phone"]
}

agent = create_agent(
    model="gpt-5",
    response_format=ProviderStrategy(contact_info_schema)
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "Extract contact info from: John Doe, john@example.com, (555) 123-4567"}]
})

result["structured_response"]
```

### with_structured_output Method

```python
from pydantic import BaseModel


class AnswerWithJustification(BaseModel):
    answer: str
    justification: str


_model = model.with_structured_output(AnswerWithJustification)
result = _model.invoke("What weighs more, a pound of bricks or a pound of feathers?")
```

---

## Streaming

### Streaming Messages

```python
from langchain.agents import create_agent
from langchain.messages import AIMessageChunk

agent = create_agent("openai:gpt-5.2", tools=[get_weather])

for chunk in agent.stream({
    "messages": [{"role": "user", "content": "Tell me a story"}]
}):
    if isinstance(chunk, AIMessageChunk):
        print(chunk.text, end="")
```

### Streaming Tool Calls and Updates

```python
from typing import Any
from langchain.agents import create_agent
from langchain.messages import AIMessage, AIMessageChunk, AnyMessage, ToolMessage


def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"


agent = create_agent("openai:gpt-5.2", tools=[get_weather])


def _render_message_chunk(token: AIMessageChunk) -> None:
    if token.text:
        print(token.text, end="|")
    if token.tool_call_chunks:
        print(token.tool_call_chunks)


def _render_completed_message(message: AnyMessage) -> None:
    if isinstance(message, AIMessage) and message.tool_calls:
        print(f"Tool calls: {message.tool_calls}")
    if isinstance(message, ToolMessage):
        print(f"Tool response: {message.content_blocks}")


input_message = {"role": "user", "content": "What is the weather in Boston?"}
for stream_mode, data in agent.stream(
    {"messages": [input_message]},
    stream_mode=["messages", "updates"],
):
    if stream_mode == "messages":
        token, metadata = data
        if isinstance(token, AIMessageChunk):
            _render_message_chunk(token)
    if stream_mode == "updates":
        for source, update in data.items():
            if source in ("model", "tools"):
                _render_completed_message(update["messages"][-1])
```

---

## RAG (Retrieval-Augmented Generation)

### Basic RAG Pipeline

```python
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

prompt = ChatPromptTemplate.from_template(
    """Answer the question based only on the context provided.

Context: {context}

Question: {question}"""
)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

result = chain.invoke("What is the capital of France?")
```

### Complete RAG Setup

```python
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

# Load documents
loader = PyPDFLoader("document.pdf")
documents = loader.load()

# Split documents
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
splits = text_splitter.split_documents(documents)

# Create vector store
vectorstore = Chroma.from_documents(
    documents=splits,
    embedding=OpenAIEmbeddings()
)
retriever = vectorstore.as_retriever()

# Create RAG chain
prompt = ChatPromptTemplate.from_template(
    """Answer the question based only on the context provided.

Context: {context}

Question: {question}"""
)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | ChatOpenAI(model="gpt-4")
    | StrOutputParser()
)

# Query
result = chain.invoke("What is the main topic of the document?")
print(result)
```

---

## Best Practices

### 1. Use Type Hints

```python
from typing import TypedDict

class InputSchema(TypedDict):
    question: str
    context: str

chain = prompt | llm | StrOutputParser()
result: str = chain.invoke(InputSchema(
    question="What is X?",
    context="Context here"
))
```

### 2. Error Handling

```python
try:
    result = chain.invoke({"question": "test"})
except Exception as e:
    print(f"Error: {e}")
    # Handle error appropriately
```

### 3. Configurable Chains

```python
from langchain_core.runnables import RunnableConfig

config = RunnableConfig(
    tags=["production"],
    metadata={"user_id": "123"}
)

result = chain.invoke({"question": "test"}, config=config)
```

### 4. Batch Processing

```python
questions = [
    {"question": "What is AI?"},
    {"question": "What is ML?"},
    {"question": "What is DL?"}
]

results = chain.batch(questions)
```

---

## Migration from LangChain 0.x

### Old Syntax (0.x)

```python
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

prompt = PromptTemplate(
    template="Tell me a joke about {topic}",
    input_variables=["topic"]
)

chain = LLMChain(llm=llm, prompt=prompt)
result = chain.run("programming")
```

### New Syntax (1.0)

```python
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt = PromptTemplate.from_template("Tell me a joke about {topic}")
chain = prompt | llm | StrOutputParser()

result = chain.invoke({"topic": "programming"})
```

---

## Additional Resources

- [LangChain Official Documentation](https://python.langchain.com/)
- [LCEL Documentation](https://python.langchain.com/docs/expression_language/)
- [Agents Documentation](https://python.langchain.com/docs/modules/agents/)
- [Context7 LangChain Examples](https://github.com/context7/langchain_oss_python)

---

## License

This documentation is provided as a reference guide for LangChain 1.0 syntax and patterns.
