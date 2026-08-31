from __future__ import annotations

import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from app import AILearningAgent
from live_data import get_daily_updates
from rag import VectorStore


ROOT = Path(__file__).parent


def _payload(level: str = "beginner") -> dict:
    agent = AILearningAgent(level=level)
    store = VectorStore(ROOT / "learning_vectors.db")
    context = store.context_for(agent.get_plan().focus)
    plan = agent.get_plan(retrieved_context=context)
    return {
        "plan": plan.__dict__,
        "roadmap": agent.get_weekly_roadmap(),
        "sources": store.search(plan.focus),
        "live_updates": get_daily_updates(ROOT / "live_updates.json"),
    }


HTML = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width">
<title>AI Learning Agent</title><style>
body{font:16px system-ui;background:#f4f7fb;color:#172033;margin:0}nav{background:#172033;padding:14px calc((100% - 960px)/2);display:flex;gap:8px}nav button{background:transparent;color:white;border:1px solid #71809b;border-radius:20px;padding:8px 16px;cursor:pointer}nav button.active{background:#5b7cfa;border-color:#5b7cfa}main{max-width:960px;margin:40px auto;padding:0 20px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px}.card{background:white;border-radius:14px;padding:20px;box-shadow:0 4px 18px #17203312}
 h1{margin-bottom:4px}h2{font-size:18px;color:#40506b}.muted{color:#66748a}li{margin:10px 0}a{color:#315bdc}
</style></head><body><nav><button data-level="beginner">Beginner</button><button data-level="intermediate">Intermediate</button><button data-level="advanced">Advanced</button></nav><main><p class="muted">AI LEARNING AGENT</p><h1 id="focus">Loading...</h1><p id="meta"></p>
<div class="grid"><section class="card"><h2>Today's lesson</h2><p id="lesson"></p><h2>Practice</h2><p id="practice"></p></section>
<section class="card"><h2>Daily update</h2><p id="update"></p><h2>Retrieved context</h2><p id="sources"></p></section>
<section class="card"><h2>Live AI updates</h2><p id="live-status"></p><ul id="live-items"></ul></section>
<section class="card"><h2>Weekly roadmap</h2><ol id="roadmap"></ol></section></div>
<script>
const buttons=document.querySelectorAll('nav button'),focus=document.getElementById('focus'),
meta=document.getElementById('meta'),lesson=document.getElementById('lesson'),practice=document.getElementById('practice'),
update=document.getElementById('update'),sources=document.getElementById('sources'),roadmap=document.getElementById('roadmap'),
liveStatus=document.getElementById('live-status'),liveItems=document.getElementById('live-items');
function load(level){buttons.forEach(b=>b.classList.toggle('active',b.dataset.level===level));
fetch('/api/plan?level='+level).then(r=>r.json()).then(d=>{let p=d.plan;
focus.textContent=p.focus;meta.textContent=`${p.date} · ${p.level}`;lesson.textContent=p.lesson;
practice.textContent=p.practice_task;update.textContent=p.daily_update;
sources.textContent=d.sources.length?d.sources.map(s=>s.text).join(' '):'No indexed sources yet.';
roadmap.innerHTML=d.roadmap.map(x=>`<li><b>${x.topic}</b><br>${x.goal}</li>`).join('');
liveStatus.textContent=d.live_updates.status==='live'?`Updated daily from ${d.live_updates.source} (${d.live_updates.date})`:d.live_updates.message;
liveItems.innerHTML=d.live_updates.items.map(x=>`<li><a href="${x.url}" target="_blank" rel="noopener">${x.title}</a></li>`).join('')||'<li>No live articles available.</li>'})}
buttons.forEach(b=>b.addEventListener('click',()=>load(b.dataset.level)));load('beginner');
</script>
</main></body></html>"""


class DashboardHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        route = urlparse(self.path).path
        if route == "/":
            body, content_type = HTML, "text/html; charset=utf-8"
        elif route == "/api/plan":
            requested = parse_qs(urlparse(self.path).query).get("level", ["beginner"])[0].lower()
            level = requested if requested in {"beginner", "intermediate", "advanced"} else "beginner"
            body, content_type = json.dumps(_payload(level)), "application/json"
        else:
            self.send_error(404)
            return
        encoded = body.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def log_message(self, format: str, *args: object) -> None:
        return


if __name__ == "__main__":
    host = "0.0.0.0"
    port = int(os.environ.get("PORT", "8000"))
    print(f"Dashboard available at http://{host}:{port}")
    HTTPServer((host, port), DashboardHandler).serve_forever()
