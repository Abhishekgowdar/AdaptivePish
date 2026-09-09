"""
AdaptivePhish Backend API
FastAPI server that exposes phishing detection endpoints.
"""

import sys
import os

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, HttpUrl
from typing import Optional
import base64
from io import BytesIO
from PIL import Image
import uvicorn
from pathlib import Path

# Import our detection modules
from modules.url_analyzer import URLAnalyzer
from modules.visual_analyzer import VisualAnalyzer
from modules.text_analyzer import TextAnalyzer

# Initialize FastAPI app
app = FastAPI(
    title="AdaptivePhish API",
    description="Multi-Modal Phishing Detection API using AI and Computer Vision",
    version="1.0.0"
)

# Configure CORS (allow frontend to call backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize detection modules (done once at startup)
print("🔄 Initializing detection modules...")
url_analyzer = URLAnalyzer()
visual_analyzer = VisualAnalyzer()
text_analyzer = TextAnalyzer()
print("✅ All modules loaded successfully!")

# Request/Response models
class URLAnalysisRequest(BaseModel):
    url: str

class TextAnalysisRequest(BaseModel):
    text: str
    url: Optional[str] = None

class FullAnalysisRequest(BaseModel):
    url: str
    text: Optional[str] = None
    screenshot_base64: Optional[str] = None

# Root endpoint - will be replaced by frontend if available
@app.get("/api/info")
async def api_info():
    """API information endpoint."""
    return {
        "message": "🛡️ AdaptivePhish API - Multi-Modal Phishing Detection",
        "version": "1.0.0",
        "endpoints": {
            "analyze_url": "/analyze/url",
            "analyze_text": "/analyze/text",
            "analyze_screenshot": "/analyze/screenshot",
            "analyze_full": "/analyze/full"
        },
        "status": "online"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    """Check if API is healthy."""
    return {
        "status": "healthy",
        "modules": {
            "url_analyzer": "loaded",
            "visual_analyzer": "loaded",
            "text_analyzer": "loaded"
        }
    }

# URL Analysis endpoint
@app.post("/analyze/url")
async def analyze_url(request: URLAnalysisRequest):
    """
    Analyze a URL for phishing indicators.

    Returns risk score, verdict, and detailed flags.
    """
    try:
        result = url_analyzer.analyze(request.url)
        return {
            "success": True,
            "module": "url_analyzer",
            "result": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"URL analysis failed: {str(e)}")

# Text Analysis endpoint
@app.post("/analyze/text")
async def analyze_text(request: TextAnalysisRequest):
    """
    Analyze text content for phishing indicators.

    Returns risk score, verdict, and detected patterns.
    """
    try:
        result = text_analyzer.analyze(request.text, request.url)
        return {
            "success": True,
            "module": "text_analyzer",
            "result": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Text analysis failed: {str(e)}")

# Screenshot Analysis endpoint
@app.post("/analyze/screenshot")
async def analyze_screenshot(file: UploadFile = File(...)):
    """
    Analyze a screenshot for phishing indicators.

    Accepts image file upload (PNG, JPG, etc.)
    Returns risk score, verdict, and visual analysis.
    """
    try:
        # Read uploaded image
        image_bytes = await file.read()
        image = Image.open(BytesIO(image_bytes))

        # Analyze with visual analyzer
        result = visual_analyzer.analyze(image)

        return {
            "success": True,
            "module": "visual_analyzer",
            "result": result,
            "image_info": {
                "filename": file.filename,
                "size": image.size,
                "format": image.format
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Screenshot analysis failed: {str(e)}")

# Full Multi-Modal Analysis endpoint
@app.post("/analyze/full")
async def analyze_full(request: FullAnalysisRequest):
    """
    Complete multi-modal analysis combining URL, text, and visual analysis.

    This is the main endpoint that uses all 3 detection modules.
    Returns combined risk score and comprehensive verdict.
    """
    try:
        results = {}

        # 1. URL Analysis (always required)
        print(f"Analyzing URL: {request.url}")
        url_result = url_analyzer.analyze(request.url)
        results['url_analysis'] = url_result

        # 2. Text Analysis (if text provided)
        if request.text and len(request.text) > 10:
            print("Analyzing text content...")
            text_result = text_analyzer.analyze(request.text, request.url)
            results['text_analysis'] = text_result
        else:
            results['text_analysis'] = None

        # 3. Visual Analysis (if screenshot provided)
        if request.screenshot_base64:
            print("Analyzing screenshot...")
            try:
                # Decode base64 screenshot
                image_data = base64.b64decode(request.screenshot_base64.split(',')[-1])
                image = Image.open(BytesIO(image_data))
                visual_result = visual_analyzer.analyze(image)
                results['visual_analysis'] = visual_result
            except Exception as e:
                print(f"Screenshot analysis failed: {e}")
                results['visual_analysis'] = None
        else:
            results['visual_analysis'] = None

        # 4. Fusion: Combine all results
        final_score, final_verdict = _fuse_results(results)

        return {
            "success": True,
            "url": request.url,
            "individual_results": results,
            "final_analysis": {
                "risk_score": final_score,
                "verdict": final_verdict,
                "verdict_color": _get_verdict_color(final_verdict),
                "confidence": _calculate_confidence(results)
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Full analysis failed: {str(e)}")

# Helper function: Fuse results from multiple modules
def _fuse_results(results):
    """
    Combine results from URL, text, and visual analyzers.

    Uses weighted average based on which modules ran successfully.
    """
    scores = []
    weights = []

    # URL analysis (weight: 0.3)
    if results.get('url_analysis'):
        scores.append(results['url_analysis']['risk_score'])
        weights.append(0.3)

    # Text analysis (weight: 0.3)
    if results.get('text_analysis') and results['text_analysis']:
        scores.append(results['text_analysis']['risk_score'])
        weights.append(0.3)

    # Visual analysis (weight: 0.4 - most reliable)
    if results.get('visual_analysis') and results['visual_analysis']:
        scores.append(results['visual_analysis']['risk_score'])
        weights.append(0.4)

    # Normalize weights if not all modules ran
    if len(scores) == 0:
        return 50, "UNKNOWN"

    total_weight = sum(weights)
    normalized_weights = [w / total_weight for w in weights]

    # Calculate weighted average
    final_score = sum(s * w for s, w in zip(scores, normalized_weights))
    final_score = round(final_score, 1)

    # Determine verdict
    if final_score >= 70:
        verdict = "PHISHING"
    elif final_score >= 40:
        verdict = "SUSPICIOUS"
    else:
        verdict = "SAFE"

    return final_score, verdict

def _get_verdict_color(verdict):
    """Get color emoji for verdict."""
    colors = {
        "PHISHING": "🔴",
        "SUSPICIOUS": "🟡",
        "SAFE": "🟢",
        "UNKNOWN": "⚪"
    }
    return colors.get(verdict, "⚪")

def _calculate_confidence(results):
    """
    Calculate confidence based on how many modules successfully analyzed.

    More modules = higher confidence.
    """
    module_count = 0
    if results.get('url_analysis'):
        module_count += 1
    if results.get('text_analysis'):
        module_count += 1
    if results.get('visual_analysis'):
        module_count += 1

    confidence_levels = {
        3: "HIGH",
        2: "MEDIUM",
        1: "LOW",
        0: "NONE"
    }

    return confidence_levels.get(module_count, "NONE")

# Serve frontend static files
frontend_path = Path(__file__).parent.parent / "frontend"

if frontend_path.exists():
    # Mount static directories
    app.mount("/css", StaticFiles(directory=str(frontend_path / "css")), name="css")
    app.mount("/js", StaticFiles(directory=str(frontend_path / "js")), name="js")

    # Serve index.html at root
    @app.get("/", response_class=FileResponse)
    async def serve_frontend_root():
        """Serve the main frontend HTML page"""
        index_file = frontend_path / "index.html"
        return FileResponse(index_file)

    # Serve test.html
    @app.get("/test.html", response_class=FileResponse)
    async def serve_test_page():
        """Serve the test page"""
        test_file = frontend_path / "test.html"
        if test_file.exists():
            return FileResponse(test_file)
        raise HTTPException(status_code=404, detail="Test page not found")

# Run server
if __name__ == "__main__":
    print("=" * 80)
    print("🛡️  AdaptivePhish Backend API")
    print("=" * 80)
    print("\n🚀 Starting server...")
    print("📍 URL: http://localhost:5000")
    print("📖 Docs: http://localhost:5000/docs")
    print("\n⏳ Loading AI models (first time takes 1-2 minutes)...")
    print("=" * 80)

    # Run with uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=5000,
        log_level="info"
    )
