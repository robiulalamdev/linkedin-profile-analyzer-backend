import traceback
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.models.schemas import AnalyzeRequest, AnalyzeResponse
from app.services.linkedin_scraper import scrape_linkedin_profile
from app.services.ai_providers import run_analysis
from app.exceptions import AppError
from app.crypto import decrypt

router = APIRouter()


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_profile(request: AnalyzeRequest):
    try:
        api_key = decrypt(request.apiKey)
        profile_data = await scrape_linkedin_profile(request.linkedinUrl)
        result = await run_analysis(
            provider=request.provider,
            api_key=api_key,
            profile_data=profile_data,
        )
        return result
    except AppError as e:
        return JSONResponse(status_code=e.status_code, content={"error": e.message})
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"error": f"{type(e).__name__}: {str(e)}"},
        )
