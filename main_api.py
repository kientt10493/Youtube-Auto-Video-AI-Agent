import uvicorn
from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
from agents.minh_orchestrator import MinhOrchestrator

app = FastAPI(
    title="YouTube AI Agent Studio API",
    description="Hệ thống Multi-Agent tự động hóa sản xuất Video YouTube từ A-Z",
    version="2.0.0"
)

orchestrator = MinhOrchestrator(max_qa_retries=3)

class ProduceRequest(BaseModel):
    topic: str

@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "YouTube AI Agent Studio",
        "agents": [
            "Hoàng (Executive Manager & QA Lead)",
            "Minh (Lead Producer & Orchestrator)",
            "Linh (Trend & Market Researcher)",
            "Khoa (Retention Scriptwriter)",
            "Đạt (Audio & Voice Engineer)",
            "Vân (Visual & Art Director)",
            "Tùng (Technical Video Editor)",
            "Hà (Growth, Thumbnail & SEO Specialist)"
        ]
    }

@app.post("/produce")
def trigger_production(req: ProduceRequest):
    try:
        result = orchestrator.run_full_pipeline(req.topic)
        return {
            "status": "success",
            "project_id": result["project_id"],
            "video_path": result["final_video_path"],
            "publish_package": result["publish_package"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main_api:app", host="0.0.0.0", port=8090, reload=True)
