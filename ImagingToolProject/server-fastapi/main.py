from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from diagnosis_cardiac import video_cardiac_analyze
from fastapi.staticfiles import StaticFiles
import os
from pathlib import Path


app = FastAPI()
router = APIRouter()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8081",
        # VIC
        "http://192.168.1.19:8081",
        # ABI
        "http://172.23.127.183:8081"
        ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Get current directory and setup storage paths
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

frames_storage = os.path.join(current_dir, "server-fastapi-frames-storage")
results_storage = os.path.join(current_dir, "server-fastapi-results-storage")
input_folder_path = os.path.join(parent_dir, "frontend-storage")

print(f"(∆π∆) Frames storage path: {frames_storage}")
print(f"(∆π∆) Results storage path: {results_storage}")
print(f"(∆π∆) Frames storage exists: {os.path.exists(frames_storage)}")
print(f"(∆π∆) Results storage exists: {os.path.exists(results_storage)}")
print(f"(∆π∆) Input folder exists: {os.path.exists(input_folder_path)}")

# Mount the storage directories for static file serving
app.mount("/server-fastapi-frames-storage", StaticFiles(directory=frames_storage), name="frames")
app.mount("/server-fastapi-results-storage", StaticFiles(directory=results_storage), name="results")


@app.get("/")
async def root():
    return {"message": "Python FastAPI server is running!"}


@router.get("/diagnosis/cardiac")
async def diagnose_cardiac():
    try:
        print(f"(∆π∆) Checking input folder: {input_folder_path}")
        if not os.path.exists(input_folder_path):
            print(f"(∆π∆) Input folder does not exist: {input_folder_path}")
            return {"success": False, "message": "Input folder not found"}
   
        video_files = [f for f in os.listdir(input_folder) if f.lower().endswith(('.mp4', '.avi', '.mov'))]
        if not video_files:
            return {"success": False, "message": "No video files found"}
            
        video_name = Path(video_files[0]).stem
        success = await video_cardiac_analyze()
        
        if success:
            # Check if output files were generated
            displacement_plot = os.path.join(results_storage, "total_displacement_plot.png")
            registration_csv = os.path.join(results_storage, "registration_results.csv")
            
            if not (os.path.exists(displacement_plot) and os.path.exists(registration_csv)):
                return {
                    "success": False,
                    "message": "Analysis completed but output files not generated"
                }

            return {
                "success": True,
                "videoName": video_name,
                "results": {
                    "displacement_plot": "/server-fastapi-storage2/total_displacement_plot.png",
                    "registration_data": "/server-fastapi-storage2/registration_results.csv"
                }
            }
        else:
            return {"success": False, "message": "Analysis failed"}
    
    except Exception as e:
        print(f"Error in diagnosis endpoint: {e}")
        return {"success": False, "message": {e}}


# For REST API Testing
@router.get("/api")
async def api_endpoint():
    return {"message": "Connected"}

app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
