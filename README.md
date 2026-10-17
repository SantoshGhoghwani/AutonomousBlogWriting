**Guide**

An automated blog-writing pipeline built with CrewAI, Python, and Ollama. Give it a topic and it researches the web, drafts a post, edits it, formats it, and exports it as Markdown, HTML, PDF, DOCX, or TXT. It runs fully local and free with Ollama, or with a paid LLM API of your choice.

Full tutorial: [How to Build an Autonomous Blog Writer with CrewAI and Python on Medium.](https://medium.com/@santoshghoghwani2524/how-to-build-an-autonomous-blog-writer-with-crewai-and-python-346a3377177e)

Note: AI is meant to be an assistant, not a replacement for your effort. Please don't use this to spam low-quality blogs for monetary gain.

Features
- Four-agent crew: Researcher, Writer, Editor, and Formatter, each with its own role, goal, and backstory
- Web research tools: DuckDuckGo search plus a page reader, so drafts are based on current sources
- Sequential CrewAI Flow: each step feeds the next, with no loops or branching
- Multiple export formats: Markdown, HTML, PDF, DOCX, TXT
- Runs locally: works with Ollama (default model llama3.1:8b), so no API costs
- Configurable from the CLI: topic, audience, tone, word count, format, and output folder
- Intermediate outputs saved: inspect the research notes, draft, and edited post separately

**How it works**

Topic ──► Research ──► Drafting ──► Editing ──► Formatting ──► Export

**Prerequisites**

- Python (check CrewAI's docs for the currently supported versions)
- uv package manager
- Either Ollama installed locally (free) or API keys for a paid LLM provider
- A code editor (VS Code, Cursor, or similar)
- Basic knowledge of Python, CrewAI, and prompt engineering

**Roadmap ideas**
- Add a review loop so the editor can send the draft back to the writer
- Support more output formats and publishing targets
- Add SEO keyword and tag suggestions
- Generate images or cover art for each post
  
**Contributing**
- Issues and pull requests are welcome. If you find a bug or want a feature, open an issue first to discuss it.
  
**License**
This project is licensed under the MIT License.

Author
Santosh

Medium: https://medium.com/@santoshghoghwani2524
GitHub: https://github.com/SantoshGhoghwani

If this helped you, please consider giving the repo a star and reading the full tutorial on Medium.
