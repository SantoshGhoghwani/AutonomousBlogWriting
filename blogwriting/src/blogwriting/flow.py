import re
from pathlib import Path

from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel

from crews.content_crew.content_crew import run_step
from exporters import export
from tools.web_search_tool import PageReaderTool, WebSearchTool


class BlogState(BaseModel):
    topic: str = ""
    audience: str = "general readers"
    tone: str = "conversational and informative"
    word_count: int = 900
    output_format: str = "markdown"      # markdown | html | pdf | docx | txt
    output_dir: str = "output"
    research_notes: str = ""
    draft: str = ""
    edited_post: str = ""
    final_markdown: str = ""
    output_path: str = ""


def _clean_markdown(text: str) -> str:
    m = re.match(r"^```(?:markdown|md)?\s*\n(.*)\n```\s*$", text.strip(), re.S)
    return (m.group(1) if m else text).strip()


class BlogFlow(Flow[BlogState]):
    def _save_step(self, name: str, text: str) -> None:
        d = Path(self.state.output_dir) / "intermediate"
        d.mkdir(parents=True, exist_ok=True)
        (d / f"{name}.md").write_text(text, encoding="utf-8")

    @start()
    def research(self):
        s = self.state
        s.research_notes = run_step(
            "research_task", s.model_dump(),
            tools=[WebSearchTool(), PageReaderTool()], temperature=0.2, max_iter=10,
        )
        self._save_step("1_research", s.research_notes)

    @listen(research)
    def drafting(self):
        s = self.state
        s.draft = run_step("writing_task", s.model_dump(), temperature=0.7)
        self._save_step("2_draft", s.draft)

    @listen(drafting)
    def editing(self):
        s = self.state
        s.edited_post = run_step("editing_task", s.model_dump(), temperature=0.3)
        self._save_step("3_edited", s.edited_post)

    @listen(editing)
    def formatting(self):
        s = self.state
        raw = run_step("formatting_task", s.model_dump(), temperature=0.1)
        s.final_markdown = _clean_markdown(raw)
        path = export(s.final_markdown, s.output_format, s.output_dir, fallback_title=s.topic)
        s.output_path = str(path)
        print(f"Final output written to: {path}")
        return s.output_path