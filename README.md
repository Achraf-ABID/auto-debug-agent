# 🤖 Bug Hunter Agent

An AI-powered autonomous agent that automatically detects, reproduces, and fixes bugs in Python code using Google Gemini AI and Docker isolation.

## ✨ Features

- 🔍 **Automatic Bug Detection**: Analyzes Python code to identify logical errors and bugs
- 🧪 **Test Generation**: Creates pytest test cases that reproduce the detected bugs
- 🔧 **Auto-Fix**: Proposes and validates code corrections using AI
- 🐳 **Isolated Testing**: Runs all tests in Docker containers for safety
- 📊 **Detailed Reports**: Generates fixed code, patches, and test files

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Set up your Gemini API key
echo "GEMINI_API_KEY=your_api_key_here" > .env

# Run the agent
python -m src.main examples/buggy_math.py
```

## 📦 Output

The agent generates:
- `*.fixed.py` - Corrected code
- `*.patch` - Unified diff of changes
- `tests/repro_test_*.py` - Reproduction test cases

## 🛠️ Tech Stack

- **AI**: Google Gemini 2.5 Flash
- **Testing**: pytest in Docker containers
- **Language**: Python 3.10+

## 📝 Example

```python
# Input: buggy_math.py
def is_even(n):
    return n % 2 == 1  # Bug: returns True for odd numbers

# Output: buggy_math.py.fixed.py
def is_even(n):
    return n % 2 == 0  # Fixed: correctly checks for even numbers
```

## 🎯 Use Cases

- Automated code review
- Bug detection in legacy code
- Learning tool for debugging
- CI/CD integration for quality checks

---

**Made with ❤️ using Google Gemini AI**
