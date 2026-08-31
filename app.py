from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import json


@dataclass
class LearningPlan:
    level: str
    focus: str
    lesson: str
    practice_task: str
    daily_update: str
    date: str


class AILearningAgent:
    def __init__(self, level: str = "beginner"):
        self.level = level.lower()
        self.paths = {
            "beginner": {
                "focus": "Generative AI Fundamentals",
                "lesson": "Learn prompt engineering, model basics, and responsible AI principles.",
                "practice_task": "Write 5 prompts for summarization, brainstorming, classification, extraction, and rewriting.",
                "daily_update": "Review one beginner-friendly AI article and write 3 key takeaways.",
                "roadmap": [
                    {"day": 1, "topic": "AI foundations", "goal": "Understand machine learning basics and AI use cases."},
                    {"day": 2, "topic": "Prompt engineering", "goal": "Practice writing better prompts for chat and text tasks."},
                    {"day": 3, "topic": "Generative AI tools", "goal": "Explore ChatGPT, Copilot, and productivity workflows."},
                    {"day": 4, "topic": "AI ethics", "goal": "Study bias, privacy, and safe AI usage."},
                ],
            },
            "intermediate": {
                "focus": "AI Workflow and Evaluation",
                "lesson": "Study RAG pipelines, vector search, and evaluation metrics for AI systems.",
                "practice_task": "Build a tiny RAG-style workflow with a sample dataset and test 3 queries.",
                "daily_update": "Compare 2 AI tools on speed, accuracy, cost, and usability, then note trade-offs.",
                "roadmap": [
                    {"day": 1, "topic": "Retrieval-Augmented Generation", "goal": "Learn how documents are retrieved and grounded into AI responses."},
                    {"day": 2, "topic": "Vector databases", "goal": "Understand embeddings and semantic search."},
                    {"day": 3, "topic": "Evaluation metrics", "goal": "Measure relevance, hallucination, and answer quality."},
                    {"day": 4, "topic": "AI workflow design", "goal": "Create a small end-to-end AI app pipeline."},
                ],
            },
            "advanced": {
                "focus": "AI Engineering and Optimization",
                "lesson": "Explore LLM orchestration, agents, fine-tuning, and model evaluation at scale.",
                "practice_task": "Design an agent workflow with tool use, memory, evaluation checks, and a failure recovery plan.",
                "daily_update": "Analyze one production AI architecture and document bottlenecks, guardrails, and optimization ideas.",
                "roadmap": [
                    {"day": 1, "topic": "LLM agents", "goal": "Build a multi-step reasoning agent with tool-calling."},
                    {"day": 2, "topic": "Memory and planning", "goal": "Add short-term memory and structured task planning."},
                    {"day": 3, "topic": "Evaluation and guardrails", "goal": "Test prompts, detect failures, and add safety checks."},
                    {"day": 4, "topic": "Production architecture", "goal": "Design monitoring, observability, and cost-aware AI systems."},
                ],
            },
        }

    def get_plan(self, retrieved_context: str = "") -> LearningPlan:
        focus_data = self.paths.get(self.level, self.paths["beginner"])
        today = datetime.now().strftime("%Y-%m-%d")
        lesson = focus_data["lesson"]
        if retrieved_context:
            lesson = f"{lesson} Ground this lesson in: {retrieved_context}"
        return LearningPlan(
            level=self.level.title(),
            focus=focus_data["focus"],
            lesson=lesson,
            practice_task=focus_data["practice_task"],
            daily_update=focus_data["daily_update"],
            date=today,
        )

    def get_weekly_roadmap(self):
        focus_data = self.paths.get(self.level, self.paths["beginner"])
        return focus_data["roadmap"]

    def format_daily_update(self) -> str:
        plan = self.get_plan()
        roadmap = self.get_weekly_roadmap()
        roadmap_summary = " | ".join(
            f"Day {item['day']}: {item['topic']}" for item in roadmap[:3]
        )
        lines = [
            f"Date: {plan.date}",
            f"Level: {plan.level}",
            f"Focus: {plan.focus}",
            f"Recommended lesson: {plan.lesson}",
            f"Practice task: {plan.practice_task}",
            f"Daily update: {plan.daily_update}",
            f"Weekly roadmap: {roadmap_summary}",
        ]
        return "\n".join(lines)

    def save_daily_log(self, path: str | Path = "daily_log.json") -> dict:
        plan = self.get_plan()
        payload = {
            "date": plan.date,
            "level": plan.level,
            "focus": plan.focus,
            "lesson": plan.lesson,
            "practice_task": plan.practice_task,
            "daily_update": plan.daily_update,
            "weekly_roadmap": self.get_weekly_roadmap(),
        }
        file_path = Path(path)
        file_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return payload


def main() -> None:
    level = "beginner"
    agent = AILearningAgent(level=level)
    output = agent.format_daily_update()
    print(output)
    agent.save_daily_log("daily_log.json")


if __name__ == "__main__":
    main()
