import json


def get_analysis_prompt(profile_data: dict) -> str:
    profile_text = _format_profile(profile_data)

    return f"""You are an expert LinkedIn profile analyzer. Analyze the following LinkedIn profile and provide a comprehensive analysis.

LinkedIn Profile Data:
{profile_text}

Respond with a JSON object containing the following structure:
{{
  "overallScore": <number 0-100>,
  "scores": {{
    "headline": {{
      "score": <0-100>,
      "strengths": ["<strength1>", ...],
      "weaknesses": ["<weakness1>", ...],
      "suggestions": ["<suggestion1>", ...]
    }},
    "about": {{
      "score": <0-100>,
      "missingInformation": ["<item1>", ...],
      "writingSuggestions": ["<suggestion1>", ...]
    }},
    "experience": {{
      "score": <0-100>,
      "missingAchievements": ["<item1>", ...],
      "missingTechnologies": ["<item1>", ...],
      "missingMeasurableResults": ["<item1>", ...]
    }},
    "skills": {{
      "score": <0-100>,
      "currentSkills": ["<skill1>", ...],
      "suggestedSkills": [{{"name": "<skill>", "reason": "<why valuable>"}}]
    }},
    "projects": {{
      "score": <0-100>,
      "hasPortfolio": <boolean>,
      "hasGitHub": <boolean>,
      "hasLiveProjects": <boolean>,
      "hasCaseStudies": <boolean>,
      "suggestions": ["<suggestion1>", ...]
    }},
    "education": {{
      "score": <0-100>,
      "isComplete": <boolean>,
      "suggestedCertifications": ["<cert1>", ...]
    }},
    "activity": {{
      "score": <0-100>,
      "postingFrequency": "<description>",
      "professionalEngagement": "<description>",
      "suggestions": ["<suggestion1>", ...]
    }},
    "recruiterScore": {{
      "visibility": <0-100>,
      "professionalism": <0-100>,
      "atsReadiness": <0-100>,
      "networking": <0-100>
    }}
  }},
  "learningRecommendations": [
    {{"technology": "<name>", "reason": "<why learn this>"}}
  ],
  "summary": "<2-3 paragraph overall summary of the profile quality, biggest strengths, and biggest weaknesses>"
}}

Return ONLY valid JSON. Be specific and actionable in your suggestions."""


def _format_profile(data: dict) -> str:
    parts = []
    for key, value in data.items():
        if key == "rawHtml":
            continue
        if isinstance(value, str) and value:
            parts.append(f"{key}: {value}")
        elif isinstance(value, dict):
            parts.append(f"{key}: {json.dumps(value, indent=2)}")
    return "\n".join(parts) if parts else json.dumps(data, indent=2)
