# 🤖 SmartAgent

> A tool-using AI agent built with LangChain, Groq, and Streamlit — capable of searching the web, doing math, reading/writing files, and summarizing text.

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-0.3.25-1C3C3C?style=flat&logo=chainlink&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-llama--3.3--70b-F55036?style=flat&logo=groq&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.45.0-FF4B4B?style=flat&logo=streamlit&logoColor=white)

---

## 📌 What is SmartAgent?

SmartAgent is a **ReAct-based AI agent** — it doesn't just chat, it **thinks and acts**. When you ask it a question, it reasons through which tool to use, uses it, reads the result, and reasons again until it has a complete answer.

```
You ask a question
      ↓
Agent thinks: "What tool do I need?"
      ↓
Agent uses a tool (search / calculator / file / summarizer)
      ↓
Agent reads the result and thinks again
      ↓
Agent gives you a final answer
```

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔍 **Web Search** | Searches DuckDuckGo and returns top 3 results with titles, summaries, and URLs |
| 🧮 **Calculator** | Safely evaluates any math expression |
| 📝 **Write File** | Saves content to a `.txt` file on your computer |
| 📂 **Read File** | Reads and returns the contents of any saved file |
| 📄 **Summarize Text** | Detects long text and signals the agent to condense it |
| 💬 **Memory** | Remembers the last 10 messages in the conversation |
| 🌐 **Chat UI** | Clean browser-based chat interface powered by Streamlit |

---

## 🗂️ Project Structure

```
SmartAgent/
├── app.py                  # Streamlit web UI
├── agent.py                # Assembles the LangChain ReAct agent
├── memory.py               # Conversation memory (last 10 messages)
├── main.py                 # Optional terminal/CLI interface
├── requirements.txt        # All dependencies
├── .env.example            # Template for environment variables
├── .gitignore              # Files excluded from Git
└── tools/
    ├── __init__.py         # Bundles all tools together
    ├── search_tool.py      # DuckDuckGo web search
    ├── file_tool.py        # Read and write files
    ├── calculator.py       # Safe math expression evaluator
    └── summarizer.py       # Long text preview and summarizer
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/vaishyampayan-alt/SmartAgent.git
cd SmartAgent
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# Mac / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your environment variables

```bash
cp .env.example .env
```

Open `.env` and add your Groq API key:

```
GROQ_API_KEY=gsk_your_key_here
```

> Get a free API key at [console.groq.com](https://console.groq.com)

### 5. Run the app

```bash
streamlit run app.py
```

Open your browser and go to **http://localhost:8501**

---

## 💬 Example Prompts

Try these once the app is running:

```
What is 15% of 847?
```
```
Search the web for the latest AI news
```
```
Write a file called notes.txt with the content: Hello World
```
```
Read the file notes.txt
```
```
Summarize this text: [paste any long article]
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| [LangChain](https://langchain.com) | Agent framework and tool orchestration |
| [Groq](https://groq.com) | Ultra-fast LLM inference (`llama-3.3-70b-versatile`) |
| [Streamlit](https://streamlit.io) | Web-based chat UI |
| [DuckDuckGo Search](https://pypi.org/project/duckduckgo-search/) | Privacy-friendly web search |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | Secure API key management |

---

## 🧠 How the Agent Works

SmartAgent uses the **ReAct** (Reason + Act) pattern:

1. **Receives** your message
2. **Reasons** about which tool to use based on tool descriptions
3. **Acts** by calling the appropriate tool
4. **Observes** the tool's output
5. **Repeats** until it has enough information
6. **Responds** with a final answer

The prompt template (`hwchase17/react-chat`) from LangChain Hub guides this thinking loop. Memory is handled by `ConversationBufferWindowMemory` keeping the last 10 exchanges.

---

## ⚙️ Configuration

| Setting | Value | Description |
|---|---|---|
| Model | `llama-3.3-70b-versatile` | Groq LLM used for reasoning |
| Temperature | `0` | Focused, consistent responses |
| Memory window | `10` | Number of past messages remembered |
| Max iterations | `10` | Max reasoning loops per response |

---

## 📋 Requirements

- Python 3.9 or higher
- A free [Groq API key](https://console.groq.com)
- Internet connection (for web search and model inference)

---

## 🔒 Security Notes

- Your `GROQ_API_KEY` is stored in `.env` which is listed in `.gitignore` — it is **never uploaded to GitHub**
- The calculator uses a whitelist of allowed characters and runs with no Python builtins — safe against code injection
- File tools use `os.path.basename()` to prevent directory traversal attacks

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the repository
2. Create a new branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 👤 Author

**vaishyampayan-alt**

- GitHub: [@vaishyampayan-alt](https://github.com/vaishyampayan-alt)

---

> Built with ❤️ using LangChain, Groq, and Streamlit
