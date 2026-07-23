from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum


class AIProvider(str, Enum):
    OPENAI = "openai"
    GEMINI = "gemini"
    OPENROUTER = "openrouter"


class AnalyzeRequest(BaseModel):
    provider: AIProvider
    apiKey: str = Field(..., min_length=1, description="AI provider API key")
    linkedinUrl: str = Field(..., min_length=1, description="LinkedIn profile URL")


class CompareRequest(BaseModel):
    provider: AIProvider
    apiKey: str = Field(..., min_length=1, description="AI provider API key")
    profileUrlOne: str = Field(..., min_length=1, description="First LinkedIn profile URL")
    profileUrlTwo: str = Field(..., min_length=1, description="Second LinkedIn profile URL")


class HeadlineAnalysis(BaseModel):
    score: int = Field(..., ge=0, le=100)
    strengths: List[str]
    weaknesses: List[str]
    suggestions: List[str]


class AboutAnalysis(BaseModel):
    score: int = Field(..., ge=0, le=100)
    missingInformation: List[str]
    writingSuggestions: List[str]


class ExperienceAnalysis(BaseModel):
    score: int = Field(..., ge=0, le=100)
    missingAchievements: List[str]
    missingTechnologies: List[str]
    missingMeasurableResults: List[str]


class SkillItem(BaseModel):
    name: str
    reason: Optional[str] = None


class SkillsAnalysis(BaseModel):
    score: int = Field(..., ge=0, le=100)
    currentSkills: List[str]
    suggestedSkills: List[SkillItem]


class ProjectsAnalysis(BaseModel):
    score: int = Field(..., ge=0, le=100)
    hasPortfolio: bool
    hasGitHub: bool
    hasLiveProjects: bool
    hasCaseStudies: bool
    suggestions: List[str]


class EducationAnalysis(BaseModel):
    score: int = Field(..., ge=0, le=100)
    isComplete: bool
    suggestedCertifications: List[str]


class ActivityAnalysis(BaseModel):
    score: int = Field(..., ge=0, le=100)
    postingFrequency: str
    professionalEngagement: str
    suggestions: List[str]


class RecruiterScore(BaseModel):
    visibility: int = Field(..., ge=0, le=100)
    professionalism: int = Field(..., ge=0, le=100)
    atsReadiness: int = Field(..., ge=0, le=100)
    networking: int = Field(..., ge=0, le=100)


class LearningRecommendation(BaseModel):
    technology: str
    reason: str


class AnalysisScores(BaseModel):
    headline: HeadlineAnalysis
    about: AboutAnalysis
    experience: ExperienceAnalysis
    skills: SkillsAnalysis
    projects: ProjectsAnalysis
    education: EducationAnalysis
    activity: ActivityAnalysis
    recruiterScore: RecruiterScore


class AnalyzeResponse(BaseModel):
    overallScore: int = Field(..., ge=0, le=100)
    extractedProfile: dict
    scores: AnalysisScores
    learningRecommendations: List[LearningRecommendation]
    summary: str


class ComparisonHighlight(BaseModel):
    betterProfile: str
    missingSections: List[str]
    strongerKeywords: List[str]
    betterWriting: str
    betterAtsOptimization: str


class ComparisonResult(BaseModel):
    profileOneAnalysis: AnalyzeResponse
    profileTwoAnalysis: AnalyzeResponse
    comparison: ComparisonHighlight
    recommendations: List[str]


class HealthResponse(BaseModel):
    status: str = "healthy"
