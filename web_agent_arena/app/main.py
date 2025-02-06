from pathlib import Path
from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from .agents import MockWebAgent
from .tasks import TaskManager

app = FastAPI(
    title="Web Agent Arena", description="Compare and evaluate web browsing agents"
)

# Setup static files and templates
static_dir = Path(__file__).parent.parent / "static"
templates_dir = Path(__file__).parent.parent / "templates"

# Only mount static files if directory exists
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Setup Jinja2 templates
templates = Jinja2Templates(directory=str(templates_dir))

# Initialize task manager with correct path
tasks_file = Path(__file__).parent.parent / "web_use_tasks.jsonl"
task_manager = TaskManager(tasks_file)

# Initialize agents
agent1 = MockWebAgent("Agent A")
agent2 = MockWebAgent("Agent B")

# Store evaluation results (in memory for now)
evaluation_results = {}

# Store deployment timestamp
deployment_time = datetime.now().isoformat()


class VoteData(BaseModel):
    evaluation_id: str
    vote: str  # "A", "B", "neither", or "tie"


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "static_files": static_dir.exists(),
        "templates": templates_dir.exists(),
        "tasks_loaded": len(task_manager.get_all_tasks()),
        "deployment_time": deployment_time,
    }


@app.get("/")
async def home(request: Request):
    """Render the home page."""
    tasks = task_manager.get_all_tasks()
    return templates.TemplateResponse(
        "index.html", {"request": request, "title": "Web Agent Arena", "tasks": tasks}
    )


@app.post("/run_task")
async def run_task(request: Request):
    """Run a task with both agents and return their responses."""
    try:
        form_data = await request.form()
        task_id = form_data.get("task_id")

        # Get the task
        task = task_manager.get_task(task_id)
        if not task:
            return {"error": f"Task {task_id} not found"}

        # Get responses from both agents
        agent1_response = await agent1.run_task(task)
        agent2_response = await agent2.run_task(task)

        # Generate a unique evaluation ID
        evaluation_id = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Store results
        evaluation_results[evaluation_id] = {
            "task_id": task_id,
            "task_prompt": task.task,
            "agent1_result": agent1_response.result,
            "agent2_result": agent2_response.result,
            "agent1_metadata": agent1_response.metadata,
            "agent2_metadata": agent2_response.metadata,
            "vote": None,
        }

        return {
            "evaluation_id": evaluation_id,
            "task_prompt": task.task,
            "agent1_result": agent1_response.result,
            "agent2_result": agent2_response.result,
            "agent1_metadata": agent1_response.metadata,
            "agent2_metadata": agent2_response.metadata,
        }
    except Exception as e:
        return {"error": str(e)}


@app.post("/vote")
async def record_vote(vote_data: VoteData):
    """Record a vote for which agent performed better."""
    try:
        if vote_data.evaluation_id not in evaluation_results:
            return {"error": "Invalid evaluation ID"}

        evaluation_results[vote_data.evaluation_id]["vote"] = vote_data.vote
        return {"success": True, "vote": vote_data.vote}
    except Exception as e:
        return {"error": str(e)}
