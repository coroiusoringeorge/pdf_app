# Overview

This is a full-stack PDF chat application that lets users upload documents and ask questions about their contents. It uses LangChain for retrieval-augmented generation, with OpenAI embeddings stored in Pinecone and streamed responses powered by ChatGPT. A Flask API and Celery worker handle document processing and chat orchestration, while a Svelte frontend provides the UI for uploading PDFs and conversing with them. Redis backs real-time chat state, and Langfuse tracks conversation traces for observability. The app also supports A/B testing different LLM, retriever, and memory configurations via a scoring system.

This project is part of the [ChatGPT and LangChain: The Complete Developer's Masterclass](https://www.udemy.com/course/chatgpt-and-langchain-the-complete-developers-masterclass/) course on Udemy. Course completion includes a certificate — [view certificate](https://www.udemy.com/certificate/UC-da9cb968-65e8-4eee-b91a-80417eaeae84/).

# Technical Stack

## Backend

| Technology | Version |
| --- | --- |
| Python | 3.11 |
| Flask | 2.3.1 |
| Flask-SQLAlchemy | 3.0.3 |
| Celery | 5.3.1 |
| LangChain | 0.0.352 |
| langchain-openai | 0.0.5 |
| langchain-community | 0.0.19 |
| Pinecone client | 3.2.2 |
| Redis (client) | 5.0.0 |
| Langfuse | 1.0.18 |
| pypdf | 3.15.4 |

## Frontend

| Technology | Version |
| --- | --- |
| Svelte | 3.54 |
| SvelteKit | 1.5 |
| TypeScript | 5.0 |
| Vite | 4.3 |
| Tailwind CSS | 3.3 |
| pdfjs-dist | 3.5 |
| Chart.js | 4.4 |

## External Services

| Service | Purpose |
| --- | --- |
| OpenAI | LLMs (`gpt-4`, `gpt-3.5-turbo`) and embeddings |
| Pinecone | Vector store for document retrieval |
| Redis | Celery broker and chat session state |
| SQLite | Application database |
| Langfuse | LLM trace and observability (optional) |

# First Time Setup

## 1. External Services

Before running the app, set up the following external services and collect the credentials you will need for `.env`.

### OpenAI

1. Create an account at [platform.openai.com](https://platform.openai.com).
2. Generate an API key from the [API keys page](https://platform.openai.com/api-keys).
3. Set `OPENAI_API_KEY` in your `.env` file.

The app uses OpenAI for embeddings and chat models (`gpt-4`, `gpt-3.5-turbo`).

### Pinecone

1. Create an account at [pinecone.io](https://www.pinecone.io).
2. Create a new index with the following settings:
   - **Dimensions:** `1536` (matches OpenAI's default embedding model)
   - **Metric:** `cosine`
3. Copy your API key, environment/region, and index name into `.env`:
   - `PINECONE_API_KEY`
   - `PINECONE_ENV_NAME` (e.g. `us-east-1`)
   - `PINECONE_INDEX_NAME` (e.g. `docs`)

Uploaded PDFs are chunked and stored in this index for retrieval during chat.

### Redis

Redis is required for Celery task queuing and chat session state.

Install and run Redis locally:

```
# macOS (Homebrew)
brew install redis
redis-server

# Or use Docker
docker run -d -p 6379:6379 redis
```

Set `REDIS_URI=redis://localhost:6379` in your `.env` file.

### File Upload Service

PDF files are stored by an external upload service. The app expects a base URL that exposes:

- `POST /upload` — accepts a file and returns a file ID
- `GET /download/{file_id}` — returns the stored file

Set `UPLOAD_URL` to the base URL of that service (without a trailing slash).

### Langfuse (optional)

Langfuse is used to trace and observe LLM conversations. To enable it:

1. Create an account at [langfuse.com](https://langfuse.com).
2. Create a project and copy the public and secret keys.
3. Set `LANGFUSE_PUBLIC_KEY` and `LANGFUSE_SECRET_KEY` in your `.env` file.

If these keys are left empty, tracing is disabled.

## 2. Environment Configuration

Copy the example environment file and fill in your values:

```
cp .env.example .env
```

Edit `.env` with the credentials from the steps above:

| Variable | Description |
| --- | --- |
| `SECRET_KEY` | Random string used to sign Flask sessions |
| `SQLALCHEMY_DATABASE_URI` | Database connection string (default `sqlite:///sqlite.db` works for local dev) |
| `UPLOAD_URL` | Base URL of the file upload service |
| `OPENAI_API_KEY` | Your OpenAI API key |
| `REDIS_URI` | Redis connection string (default `redis://localhost:6379`) |
| `PINECONE_API_KEY` | Your Pinecone API key |
| `PINECONE_ENV_NAME` | Pinecone environment/region |
| `PINECONE_INDEX_NAME` | Name of your Pinecone index |
| `LANGFUSE_PUBLIC_KEY` | Langfuse public key (optional) |
| `LANGFUSE_SECRET_KEY` | Langfuse secret key (optional) |

## 3. Install Dependencies

### Backend (Pipenv)

```
# Install Python dependencies
pipenv install

# Activate the virtual environment
pipenv shell
```

### Frontend

The Flask server serves the built Svelte client from `client/build`.

```
cd client
npm install
npm run build
cd ..
```

## 4. Initialize the Database

With the virtual environment active:

```
flask --app app.web init-db
```

# Running the app

There are three separate processes that need to be running for the app to work: the server, the worker, and Redis.

If you stop any of these processes, you will need to start them back up!

Commands to start each are listed below. If you need to stop them, select the terminal window the process is running in and press Control-C

### To run the Python server

Open a new terminal window and create a new virtual environment:

```
pipenv shell
```

Then:

```
inv dev
```

### To run the worker

Open a new terminal window and create a new virtual environment:

```
pipenv shell
```

Then:

```
inv devworker
```

### To run Redis

```
redis-server
```

### To reset the database

Open a new terminal window and create a new virtual environment:

```
pipenv shell
```

Then:

```
flask --app app.web init-db
```
