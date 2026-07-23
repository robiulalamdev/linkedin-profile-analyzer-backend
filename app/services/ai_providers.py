import json
import httpx

from app.models.schemas import (
    AIProvider, AnalyzeResponse, ComparisonResult,
)
from app.prompts.analysis import get_analysis_prompt
from app.prompts.comparison import get_comparison_prompt
from app.exceptions import AppError


async def run_analysis(provider: AIProvider, api_key: str, profile_data: dict) -> AnalyzeResponse:
    prompt = get_analysis_prompt(profile_data)
    response_text = await _call_ai(provider, api_key, prompt)
    return _parse_analyze_response(response_text, profile_data)


async def run_comparison(
    provider: AIProvider,
    api_key: str,
    profile_one: dict,
    profile_two: dict,
) -> ComparisonResult:
    prompt = get_comparison_prompt(profile_one, profile_two)
    response_text = await _call_ai(provider, api_key, prompt)
    return _parse_comparison_response(response_text, profile_one, profile_two)


async def _call_ai(provider: AIProvider, api_key: str, prompt: str) -> str:
    try:
        if provider == AIProvider.OPENAI:
            return await _call_openai(api_key, prompt)
        elif provider == AIProvider.GEMINI:
            return await _call_gemini(api_key, prompt)
        elif provider == AIProvider.OPENROUTER:
            return await _call_openrouter(api_key, prompt)
        raise AppError("Unsupported AI provider.")
    except AppError:
        raise
    except httpx.HTTPStatusError as e:
        _handle_http_error(e, provider)
    except httpx.ConnectError:
        raise AppError("Unable to connect to the AI provider. Please check your internet connection.")
    except httpx.TimeoutException:
        raise AppError("The AI provider took too long to respond. Please try again.")
    except Exception:
        raise AppError("Something went wrong while contacting the AI provider. Please try again.")


def _handle_http_error(e: httpx.HTTPStatusError, provider: AIProvider) -> None:
    status = e.response.status_code
    provider_name = provider.value.title()

    if status == 429:
        raise AppError(
            f"You've reached the {provider_name} rate limit. "
            "Please wait a moment and try again, or upgrade your plan.",
            status_code=429,
        )
    elif status == 401:
        raise AppError(
            f"Invalid {provider_name} API key. "
            "Please double-check your key and try again.",
            status_code=401,
        )
    elif status == 402:
        raise AppError(
            f"Your {provider_name} account needs funds. "
            "Even free models require a small balance. "
            "Add at least $1 at the provider's dashboard, then try again.",
            status_code=402,
        )
    elif status == 403:
        raise AppError(
            f"Your {provider_name} API key doesn't have permission for this request. "
            "Please check your API key permissions.",
            status_code=403,
        )
    elif status == 404:
        raise AppError(
            f"The {provider_name} model or endpoint was not found. "
            "Please try a different provider.",
            status_code=404,
        )
    elif status >= 500:
        raise AppError(
            f"{provider_name} is experiencing server issues. Please try again later.",
            status_code=502,
        )
    else:
        raise AppError(
            f"Unexpected error from {provider_name} (HTTP {status}). Please try again.",
            status_code=status,
        )


async def _call_openai(api_key: str, prompt: str) -> str:
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={
                "model": "gpt-4o",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
                "response_format": {"type": "json_object"},
            },
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]


async def _call_gemini(api_key: str, prompt: str) -> str:
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}",
            headers={"Content-Type": "application/json"},
            json={
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": 0.7, "responseMimeType": "application/json"},
            },
        )
        response.raise_for_status()
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]


async def _call_openrouter(api_key: str, prompt: str) -> str:
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://profilelens.ai",
                "X-OpenRouter-Title": "ProfileLens AI",
            },
            json={
                "model": "meta-llama/llama-3.1-8b-instruct",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
            },
        )
        if not response.is_success:
            raise AppError(
                "Could not complete the analysis. Please check your API key and try again.",
                status_code=response.status_code,
            )
        return response.json()["choices"][0]["message"]["content"]


def _parse_analyze_response(text: str, profile_data: dict) -> AnalyzeResponse:
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        import re
        match = re.search(r"```json\s*(.*?)\s*```", text, re.DOTALL)
        if match:
            data = json.loads(match.group(1))
        else:
            raise AppError(
                "The AI response couldn't be parsed. Please try again.",
                status_code=502,
            )

    scores = data.get("scores", data)

    return AnalyzeResponse(
        overallScore=data.get("overallScore", scores.get("overallScore", 75)),
        extractedProfile=profile_data,
        scores={
            "headline": scores.get("headline", {"score": 70, "strengths": [], "weaknesses": [], "suggestions": []}),
            "about": scores.get("about", {"score": 70, "missingInformation": [], "writingSuggestions": []}),
            "experience": scores.get("experience", {"score": 70, "missingAchievements": [], "missingTechnologies": [], "missingMeasurableResults": []}),
            "skills": scores.get("skills", {"score": 70, "currentSkills": [], "suggestedSkills": []}),
            "projects": scores.get("projects", {"score": 70, "hasPortfolio": False, "hasGitHub": False, "hasLiveProjects": False, "hasCaseStudies": False, "suggestions": []}),
            "education": scores.get("education", {"score": 70, "isComplete": True, "suggestedCertifications": []}),
            "activity": scores.get("activity", {"score": 70, "postingFrequency": "Unknown", "professionalEngagement": "Unknown", "suggestions": []}),
            "recruiterScore": scores.get("recruiterScore", {"visibility": 70, "professionalism": 70, "atsReadiness": 70, "networking": 70}),
        },
        learningRecommendations=data.get("learningRecommendations", []),
        summary=data.get("summary", "Analysis complete."),
    )


def _parse_comparison_response(text: str, profile_one: dict, profile_two: dict) -> ComparisonResult:
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        import re
        match = re.search(r"```json\s*(.*?)\s*```", text, re.DOTALL)
        if match:
            data = json.loads(match.group(1))
        else:
            raise AppError(
                "The AI comparison response couldn't be parsed. Please try again.",
                status_code=502,
            )

    profile_one_analysis = _parse_analyze_response(
        json.dumps(data.get("profileOneAnalysis", data.get("profileOne", {}))),
        profile_one,
    )
    profile_two_analysis = _parse_analyze_response(
        json.dumps(data.get("profileTwoAnalysis", data.get("profileTwo", {}))),
        profile_two,
    )

    comparison = data.get("comparison", {})
    return ComparisonResult(
        profileOneAnalysis=profile_one_analysis,
        profileTwoAnalysis=profile_two_analysis,
        comparison={
            "betterProfile": comparison.get("betterProfile", "Tie"),
            "missingSections": comparison.get("missingSections", []),
            "strongerKeywords": comparison.get("strongerKeywords", []),
            "betterWriting": comparison.get("betterWriting", ""),
            "betterAtsOptimization": comparison.get("betterAtsOptimization", ""),
        },
        recommendations=data.get("recommendations", []),
    )
