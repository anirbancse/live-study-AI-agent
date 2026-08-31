# AI Learning Daily Agent

This project creates a small AI learning recommendation agent that suggests daily learning tasks and provides a daily summary update.

## Features

- Personalized daily AI learning suggestions
- Beginner to advanced level tracking
- Daily update summary
- Simple Python implementation with no external dependencies
- Easy scheduling via Windows Task Scheduler or cron
- Local RAG retrieval seam and web dashboard

## Run locally

```bash
python app.py
```

## Web dashboard

```powershell
python dashboard.py
```

Open `http://127.0.0.1:8000`. The architecture and migration path to an
embedding-powered vector database are documented in
[implementation-plan.md](implementation-plan.md).

The dashboard navigation switches between beginner, intermediate, and advanced
plans. It refreshes public AI article data from arXiv once per calendar day
and caches the result in `live_updates.json`.

## Free hosting with Render

1. Push this project to a GitHub repository.
2. In Render, choose **New > Web Service** and connect the repository.
3. Use these settings:
   - **Runtime:** Python
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `python dashboard.py`
   - **Instance type:** Free
4. Deploy and open the generated `onrender.com` URL.

The server reads Render's `PORT` value and binds to `0.0.0.0`. The free
instance may sleep when idle, and local files such as `learning_vectors.db`
and `live_updates.json` are not durable across redeploys. Use a hosted
database/object store later if uploaded content or history must persist.

## Example output

```text
Date: 2026-08-31
Focus: Generative AI Fundamentals
Recommended lesson: Learn prompt engineering patterns and chain-of-thought reasoning.
Practice task: Build 3 sample prompts for summarization, classification, and brainstorming.
Daily update: Review 1 research paper or article and note 3 takeaways.
```

## Optional scheduling

On Windows, create a task to run:

```powershell
python C:\path\to\ai-learning-agent\app.py
```

at a preferred daily time.
