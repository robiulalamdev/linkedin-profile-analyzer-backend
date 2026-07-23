from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.models.schemas import CompareRequest, ComparisonResult
from app.services.linkedin_scraper import scrape_linkedin_profile
from app.services.ai_providers import run_comparison
from app.exceptions import AppError
from app.crypto import decrypt

router = APIRouter()


@router.post("/compare", response_model=ComparisonResult)
async def compare_profiles(request: CompareRequest):
    try:
        api_key = decrypt(request.apiKey)
        profile_one = await scrape_linkedin_profile(request.profileUrlOne)
        profile_two = await scrape_linkedin_profile(request.profileUrlTwo)
        result = await run_comparison(
            provider=request.provider,
            api_key=api_key,
            profile_one=profile_one,
            profile_two=profile_two,
        )
        return result
    except AppError as e:
        return JSONResponse(status_code=e.status_code, content={"error": e.message})
    except Exception:
        return JSONResponse(
            status_code=500,
            content={"error": "Something went wrong. Please try again."},
        )
