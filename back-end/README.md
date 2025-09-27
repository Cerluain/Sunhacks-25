# Sunhacks-25 Backend

## Prerequisites

Before setting up this project, make sure you have:
- **Python 3.13+** installed
- **uv** package manager installed ([Install uv](https://docs.astral.sh/uv/getting-started/installation/))

## Project Setup

### 1. Clone and Navigate
```powershell
git clone <repository-url>
cd Sunhacks-25/back-end
```

### 2. Install All Dependencies
This project uses `uv` for modern Python dependency management. Run this command to install all packages:

```powershell
uv sync
```

This will automatically:
- Create a virtual environment (`.venv`)
- Install all dependencies from `pyproject.toml`
- Lock exact versions in `uv.lock`

### 3. Environment Variables (Optional)
If your project needs API keys:
1. Create a `.env` file in the project root
2. Add your environment variables:
```
TAVILY_API_KEY=your_tavily_key_here
GOOGLE_API_KEY=your_google_key_here
```

## Installed Packages

### Core FastAPI Dependencies
- `fastapi` - Modern web framework for building APIs
- `uvicorn[standard]` - ASGI server for running FastAPI apps
- `pydantic[email]` - Data validation with email validation support

### Database Dependencies
- `sqlalchemy[asyncio]` - SQL toolkit with async support
- `asyncpg` - PostgreSQL async driver
- `alembic` - Database migrations

### Security Dependencies
- `passlib[bcrypt]` - Password hashing
- `python-jose[cryptography]` - JWT token handling
- `python-multipart` - File upload and form data support

### AI/ML Dependencies
- `google-generativeai` - Google AI integration
- `langchain` - LangChain framework
- `langchain-google-genai` - Google AI for LangChain
- `tavily-python` - Tavily search integration

### Development Dependencies
- `pytest` - Testing framework
- `pytest-asyncio` - Async testing support
- `httpx` - HTTP client for API testing

### Utility Dependencies
- `python-dotenv` - Environment variable management

## Running the Application

### Start the main application:
```powershell
uv run python main.py
```

### Run FastAPI development server (when you build your API):
```powershell
uv run uvicorn main:app --reload
```

## Development Commands

### Add new packages:
```powershell
uv add package-name
```

### Add development-only packages:
```powershell
uv add --dev package-name
```

### Remove packages:
```powershell
uv remove package-name
```

### Run tests:
```powershell
uv run pytest
```

## Quick Code Examples

### Load environment variables:
```python
from dotenv import load_dotenv
load_dotenv()
```

### Basic FastAPI setup:
```python
from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}
```

### LangChain + Gemini:
```python
from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
resp = llm.invoke("Say hello in one sentence")
print(resp.content)
```

### Tavily search:
```python
from dotenv import load_dotenv
load_dotenv()

from tavily import TavilyClient

client = TavilyClient()
result = client.search(query="latest LangChain release", max_results=3)
print(result)
```

## Why uv instead of pip + requirements.txt?

- **Faster installs** - uv is written in Rust and much faster than pip
- **Automatic virtual environment management** - no need to manually create/activate venvs
- **Lock files** - `uv.lock` ensures everyone gets identical dependencies
- **Modern Python packaging** - uses `pyproject.toml` (the new standard)
- **Better dependency resolution** - handles conflicts automatically

## Troubleshooting

### If packages don't install:
```powershell
uv sync --reinstall
```

### If you get import errors:
Make sure you're using uv to run Python:
```powershell
uv run python your-script.py
```

### Check installed packages:
```powershell
uv pip list
```

