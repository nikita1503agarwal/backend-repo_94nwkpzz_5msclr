import os
import time
from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class HyperGenerateRequest(BaseModel):
    prompt: str


class HyperGenerateResponse(BaseModel):
    prompt: str
    chat_response: str
    image_url: str
    video_url: str
    audio_url: str
    image_to_video_concept: str


@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI Backend!"}


@app.get("/api/hello")
def hello():
    return {"message": "Hello from the backend API!"}


@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    
    try:
        # Try to import database module
        from database import db
        
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            
            # Try to list collections to verify connectivity
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]  # Show first 10 collections
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
            
    except ImportError:
        response["database"] = "❌ Database module not found (run enable-database first)"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    
    # Check environment variables
    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    
    return response


def build_svg_image_data_url(prompt: str) -> str:
    """Create a high-res cyberpunk-styled SVG image as a data URL."""
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900">
      <defs>
        <linearGradient id="g1" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stop-color="#0f0c29"/>
          <stop offset="50%" stop-color="#302b63"/>
          <stop offset="100%" stop-color="#24243e"/>
        </linearGradient>
        <linearGradient id="neon" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stop-color="#00F5FF"/>
          <stop offset="100%" stop-color="#9B5CFF"/>
        </linearGradient>
        <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
          <feGaussianBlur stdDeviation="6" result="coloredBlur"/>
          <feMerge>
            <feMergeNode in="coloredBlur"/>
            <feMergeNode in="SourceGraphic"/>
          </feMerge>
        </filter>
      </defs>
      <rect width="100%" height="100%" fill="url(#g1)"/>
      <g opacity="0.35">
        <circle cx="200" cy="150" r="120" fill="#7f00ff"/>
        <circle cx="1450" cy="200" r="180" fill="#00d2ff"/>
        <circle cx="1200" cy="780" r="140" fill="#ff00cc"/>
      </g>
      <g fill="none" stroke="url(#neon)" stroke-width="2" opacity="0.6">
        <path d="M0,700 C400,600 600,900 1000,820 1300,770 1500,860 1600,820"/>
        <path d="M0,740 C400,640 600,940 1000,860 1300,810 1500,900 1600,860"/>
      </g>
      <g filter="url(#glow)">
        <rect x="80" y="80" width="520" height="300" rx="12" fill="#0b0f1c" stroke="#9B5CFF"/>
        <text x="110" y="150" font-family="'IBM Plex Sans', Arial" font-size="28" fill="#cbd5e1">AI Power • Hyper-Generate</text>
        <text x="110" y="190" font-family="'IBM Plex Sans', Arial" font-size="22" fill="#94a3b8">Prompt</text>
        <foreignObject x="110" y="210" width="460" height="140">
          <div xmlns="http://www.w3.org/1999/xhtml" style="color:#e2e8f0;font-family:IBM Plex Sans,Arial;font-size:18px;line-height:1.4;">{prompt}</div>
        </foreignObject>
      </g>
      <g opacity="0.9">
        <text x="1200" y="860" text-anchor="end" font-family="'IBM Plex Sans', Arial" font-size="22" fill="#cbd5e1">FREE &amp; UNLIMITED • Powered by AI Power</text>
      </g>
    </svg>'''.strip()
    import base64
    data = base64.b64encode(svg.encode("utf-8")).decode("ascii")
    return f"data:image/svg+xml;base64,{data}"


@app.post("/api/hyper-generate", response_model=HyperGenerateResponse)
def hyper_generate(req: HyperGenerateRequest):
    # Simulate 2-second text generation latency
    time.sleep(2)

    prompt = req.prompt.strip()
    if not prompt:
        prompt = "A serene cyberpunk city at sunset, with flying cars and holographic advertisements."

    chat_response = (
        "Golden hour spills neon over a layered skyline: tiered avenues, glass spires with holo-billboards, "
        "and elevated lanes where sleek aero-cabs drift like koi in a digital river. Below, night markets glow "
        "with ultraviolet signage; above, translucent ad-ribbons ripple in the warm updraft. Distant monorails "
        "trace silver arcs between towers while soft rain atomizes into prismatic mist. The city hums—gentle, "
        "alive, and strangely calm—as if the networks agreed to whisper for a moment so the sunset could be heard."
    )

    image_url = build_svg_image_data_url(prompt)

    # Use known-stable sample assets to simulate video/audio
    video_url = "https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4"
    audio_url = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"

    image_to_video_concept = (
        "Start with the generated keyframe (dusk palette: magenta, cyan, amber). Layer parallax plates:"
        " 1) foreground balcony/silhouette, 2) midground traffic streams (add light streaks),"
        " 3) background towers and sun disk. Apply slow vertical heat-haze and rolling volumetric fog."
        " Introduce looping aero-car splines with easing in/out, billboard shimmer using additive blending,"
        " and a gentle camera dolly from left to right over 10 seconds per loop."
    )

    return HyperGenerateResponse(
        prompt=prompt,
        chat_response=chat_response,
        image_url=image_url,
        video_url=video_url,
        audio_url=audio_url,
        image_to_video_concept=image_to_video_concept,
    )


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
