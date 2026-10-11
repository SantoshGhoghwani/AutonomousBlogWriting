from pathlib import Path

import yaml
from crewai import Agent, Crew, Process, Task

from config import get_llm

CONFIG_DIR = Path(__file__).parent / "config"
AGENTS = yaml.safe_load((CONFIG_DIR / "agents.yaml").read_text(encoding="utf-8"))
TASKS = yaml.safe_load((CONFIG_DIR / "tasks.yaml").read_text(encoding="utf-8"))


def run_step(task_key: str, inputs: dict, tools=None, temperature=0.4, max_iter=None) -> str:
    task_cfg = dict(TASKS[task_key])
    agent_key = task_cfg.pop("agent")          # "agent: researcher" -> look up in agents.yaml

    extra = {"max_iter": max_iter} if max_iter else {}
    agent = Agent(
        config=AGENTS[agent_key],
        tools=tools or [],
        llm=get_llm(temperature),
        allow_delegation=False,
        verbose=True,
        **extra,
    )
    task = Task(config=task_cfg, agent=agent)
    crew = Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=True)
    return str(crew.kickoff(inputs=inputs).raw).strip()   # fills {topic}, {draft}, etc.