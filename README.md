
# Autonomous Code Review with AI

This project implements an autonomous, AI-driven agent to analyze GitHub pull requests. Using Large Language Models (LLMs) via LangChain, the agent provides comprehensive code reviews, identifying issues such as code style, potential bugs, performance improvements, and best practices. It returns a structured JSON report with identified issues and suggestions, enhancing code quality and reducing the burden on human reviewers.

## Features

- **Automated Code Review**: Identifies potential code issues, style problems, and performance improvements.
- **Pull Request Summarization**: Summarizes the scope and purpose of each pull request.
- **Comprehensive Reporting**: Generates a JSON report summarizing identified issues.
- **Asynchronous Processing**: Uses Celery for efficient asynchronous task handling.
- **Modular Architecture**: Designed with extensibility and maintainability in mind.

---

## Project Setup Instructions

### Prerequisites

- **Python 3.8+**
- **Redis** (for Celery task management and result backend)
- **GitHub Token**: Required if accessing private repositories

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/autonomous_code_review.git
   cd autonomous_code_review
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   - Copy `.env.example` to `.env` and add your environment variables:
     ```plaintext
     OPENAI_API_KEY=your_openai_api_key
     GITHUB_TOKEN=your_github_token
     REDIS_BROKER_URL=redis://localhost:6379/0
     REDIS_RESULT_BACKEND=redis://localhost:6379/0
     ```

---

## Running the Application

1. **Start Redis** (for Celery)
   - Make sure you have Redis running locally or update the `REDIS_BROKER_URL` and `REDIS_RESULT_BACKEND` in `.env` to point to your Redis instance.

2. **Start the Celery Worker**
   ```bash
   celery -A app.celery_app worker --loglevel=info
   ```

3. **Run the API** (if using FastAPI)
   ```bash
   uvicorn app.main:app --reload
   ```

---

## API Documentation

### POST `/analyze-pr`

Accepts GitHub PR details and returns a structured JSON report analyzing the pull request.

**Request Body:**
```json
{
  "repo_url": "https://github.com/user/repo",
  "pr_number": 123,
  "github_token": "your_github_token"
}
```

**Response:**
```json
{
    "task_id": "abc123",
    "status": "completed",
    "results": {
        "files": [
            {
                "name": "main.py",
                "issues": [
                    {
                        "type": "style",
                        "line": 15,
                        "description": "Line too long",
                        "suggestion": "Break line into multiple lines"
                    },
                    {
                        "type": "bug",
                        "line": 23,
                        "description": "Potential null pointer",
                        "suggestion": "Add null check"
                    }
                ]
            }
        ],
        "summary": {
            "total_files": 1,
            "total_issues": 2,
            "critical_issues": 1
        }
    }
}
```

---

## Project Structure

```
|-- autonomous_code_review/
|   |-- app/
|       |-- __init__.py
|       |-- review_agent.py           # Main function for analyzing PRs
|       |-- review_classes.py         # Contains PullRequestRetriever, PRSummaryChain, CodeReviewChain, PullRequestReporter
|       |-- templates.py              # Contains the prompt templates
|   |-- .env.example                  # Example environment file
|   |-- requirements.txt              # List of project dependencies
|   |-- README.md                     # Project documentation
|   |-- tests/
|       |-- __init__.py
|       |-- test_review_agent.py      # Test cases for the `analyze_pr` function and classes
```

---

## Design Decisions

- **Modular Structure**: Each part of the process is encapsulated in a separate class (`PullRequestRetriever`, `PRSummaryChain`, `CodeReviewChain`, `PullRequestReporter`) to enhance maintainability and scalability.
- **AI-Powered Analysis**: LangChain is used to leverage LLMs for natural language understanding, allowing the AI to perform code analysis and summarization tasks effectively.
- **Asynchronous Processing with Celery**: Celery enables asynchronous task processing, ensuring the code review requests are handled efficiently.

---

## Future Improvements

1. **Enhanced Error Detection**: Integrate additional error-checking techniques, such as popular linting tools, to complement the AI's code review.
2. **Support for Multiple Programming Languages**: Extend support to analyze code written in languages other than Python.
3. **GitHub Webhook Integration**: Enable automatic code review by setting up GitHub webhook support, allowing the code review process to trigger automatically on pull request events.
4. **Detailed Reporting with Links**: Enhance reporting by providing links to specific lines in GitHub for easy navigation.

---

## Example Environment File (.env.example)

```plaintext
# .env.example

# OpenAI API key
OPENAI_API_KEY=your_openai_api_key

# GitHub token (optional if working with public repos)
GITHUB_TOKEN=your_github_token

# Celery broker URL (e.g., for Redis)
REDIS_BROKER_URL=redis://localhost:6379/0

# Celery result backend (optional if using Redis or a similar service)
REDIS_RESULT_BACKEND=redis://localhost:6379/0
```

---

## Testing

Unit tests are provided in `tests/test_review_agent.py` to ensure the main functions perform as expected.

#### Running Tests

1. Run tests using `unittest`:
   ```bash
   python -m unittest discover tests
   ```

2. **Example Test Structure**:
   The tests verify the structure of the JSON output, the functionality of the modular components, and correct handling of API requests.

---

## Dependencies

Dependencies are listed in `requirements.txt`. To install them, use:
```bash
pip install -r requirements.txt
```

---

## License

This project is licensed under the MIT License.

---