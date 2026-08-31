from app import AILearningAgent


def test_beginner_plan_has_expected_fields():
    agent = AILearningAgent(level="beginner")
    plan = agent.get_plan()

    assert plan.level == "Beginner"
    assert "Generative AI" in plan.focus
    assert plan.lesson
    assert plan.practice_task
    assert plan.daily_update


def test_format_daily_update_contains_details():
    agent = AILearningAgent(level="intermediate")
    text = agent.format_daily_update()

    assert "Date:" in text
    assert "Level: Intermediate" in text
    assert "Focus: AI Workflow and Evaluation" in text
    assert "Recommended lesson:" in text


def test_weekly_plan_matches_skill_level():
    agent = AILearningAgent(level="advanced")
    roadmap = agent.get_weekly_roadmap()

    assert isinstance(roadmap, list)
    assert len(roadmap) >= 3
    assert "Agents" in roadmap[0]["topic"] or "LLM" in roadmap[0]["topic"]
