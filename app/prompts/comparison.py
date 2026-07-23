import json

from app.prompts.analysis import _format_profile


def get_comparison_prompt(profile_one: dict, profile_two: dict) -> str:
    text_one = _format_profile(profile_one)
    text_two = _format_profile(profile_two)

    return f"""You are an expert LinkedIn profile analyzer. Compare the following two LinkedIn profiles and provide a detailed comparison.

Profile A:
{text_one}

Profile B:
{text_two}

Respond with a SINGLE valid JSON object (no markdown, no code fences) containing EXACTLY this structure:
{{
  "profileOneAnalysis": {{
    "overallScore": 75,
    "scores": {{
      "headline": {{"score": 70, "strengths": [], "weaknesses": [], "suggestions": []}},
      "about": {{"score": 70, "missingInformation": [], "writingSuggestions": []}},
      "experience": {{"score": 70, "missingAchievements": [], "missingTechnologies": [], "missingMeasurableResults": []}},
      "skills": {{"score": 70, "currentSkills": [], "suggestedSkills": [{{"name": "", "reason": ""}}]}},
      "projects": {{"score": 70, "hasPortfolio": false, "hasGitHub": false, "hasLiveProjects": false, "hasCaseStudies": false, "suggestions": []}},
      "education": {{"score": 70, "isComplete": true, "suggestedCertifications": []}},
      "activity": {{"score": 70, "postingFrequency": "", "professionalEngagement": "", "suggestions": []}},
      "recruiterScore": {{"visibility": 70, "professionalism": 70, "atsReadiness": 70, "networking": 70}}
    }},
    "learningRecommendations": [{{"technology": "", "reason": ""}}],
    "summary": ""
  }},
  "profileTwoAnalysis": {{
    "overallScore": 75,
    "scores": {{
      "headline": {{"score": 70, "strengths": [], "weaknesses": [], "suggestions": []}},
      "about": {{"score": 70, "missingInformation": [], "writingSuggestions": []}},
      "experience": {{"score": 70, "missingAchievements": [], "missingTechnologies": [], "missingMeasurableResults": []}},
      "skills": {{"score": 70, "currentSkills": [], "suggestedSkills": [{{"name": "", "reason": ""}}]}},
      "projects": {{"score": 70, "hasPortfolio": false, "hasGitHub": false, "hasLiveProjects": false, "hasCaseStudies": false, "suggestions": []}},
      "education": {{"score": 70, "isComplete": true, "suggestedCertifications": []}},
      "activity": {{"score": 70, "postingFrequency": "", "professionalEngagement": "", "suggestions": []}},
      "recruiterScore": {{"visibility": 70, "professionalism": 70, "atsReadiness": 70, "networking": 70}}
    }},
    "learningRecommendations": [{{"technology": "", "reason": ""}}],
    "summary": ""
  }},
  "comparison": {{
    "betterProfile": "Profile A or Profile B with brief reason",
    "missingSections": [],
    "strongerKeywords": [],
    "betterWriting": "Which profile and why",
    "betterAtsOptimization": "Which profile and why"
  }},
  "recommendations": []
}}

IMPORTANT: Return ONLY the raw JSON object. No markdown, no code fences, no explanation text. Fill in all arrays with real analysis data based on the profiles provided."""
