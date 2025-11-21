from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
import uuid
import services.llm
from services.llm import generate_script_and_storyboard, generate_manim_code
from services.audio import generate_audio
from services.renderer import render_manim_code

app = FastAPI(title="Vidsimplify Manim Agent API")

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerateRequest(BaseModel):
    text: str
    category: str

@app.post("/generate")
async def generate_video(request: GenerateRequest):
    try:
        # 1. Generate Script and Storyboard
        print(f"Generating script for: {request.text[:50]}...")
        storyboard_data = generate_script_and_storyboard(request.text, request.category)
        if "error" in storyboard_data:
            raise HTTPException(status_code=500, detail=f"LLM Error: {storyboard_data['error']}")
        
        # 2. Generate Manim Code
        print("Generating Manim code...")
        manim_code = generate_manim_code(storyboard_data, category=request.category)
        
        # Clean up code (remove markdown backticks if present)
        manim_code = manim_code.replace("```python", "").replace("```", "").strip()
        
        # 3. Render Video with Self-Correction Loop
        print("Rendering video...")
        run_id = str(uuid.uuid4())
        filename = f"scene_{run_id}.py"
        
        # Ensure output directory exists
        os.makedirs("media/videos", exist_ok=True)
        
        success = False
        error_log = ""
        max_retries = 3
        
        for attempt in range(max_retries):
            print(f"Rendering attempt {attempt + 1}/{max_retries}...")
            success, error_log = render_manim_code(manim_code, filename=filename)
            
            if success:
                print("Rendering successful!")
                break
            else:
                print(f"Rendering failed. Error: {error_log}")
                if attempt < max_retries - 1:
                    print("Attempting to fix code with LLM...")
                    manim_code = services.llm.fix_manim_code(manim_code, error_log)
                    # Clean up fixed code
                    manim_code = manim_code.replace("```python", "").replace("```", "").strip()
        
        if not success:
            raise HTTPException(status_code=500, detail=f"Video rendering failed after {max_retries} attempts. Last error: {error_log}")
            
        # Find the generated video file
        # Manim usually outputs to media/videos/{filename_without_ext}/1080p60/VideoScene.mp4
        # We need to find it dynamically or enforce a path
        # For now, let's assume standard Manim output structure and we will serve it.
        # A better approach is to configure Manim to output to a specific file.
        
        # For simplicity in this prototype, we'll search for the mp4 file
        # In a real app, we'd parse the config or set output flags.
        
        # 4. Generate Audio (Optional for now, can be added to the video)
        # audio_data = generate_audio(storyboard_data.get('script', ''))
        
        return {"status": "success", "video_url": f"http://localhost:8000/download/{run_id}"}

    except Exception as e:
        print(f"Error in generate_video: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download/{run_id}")
async def download_video(run_id: str):
    # This is a hacky way to find the file. 
    # In production, we should track the file path in a database or return it from the render step.
    # We'll look for the most recently created mp4 file in the media directory or specific path.
    
    # For this prototype, let's try to find it based on the scene name 'VideoScene'
    # The filename passed to render was scene_{run_id}.py
    # Manim output: media/videos/scene_{run_id}/1080p60/VideoScene.mp4
    
    video_path = f"media/videos/scene_{run_id}/1080p60/VideoScene.mp4"
    
    if os.path.exists(video_path):
        return FileResponse(video_path)
    
    # Fallback search
    for root, dirs, files in os.walk("media"):
        for file in files:
            if file.endswith(".mp4"):
                return FileResponse(os.path.join(root, file))
                
    raise HTTPException(status_code=404, detail="Video not found")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
