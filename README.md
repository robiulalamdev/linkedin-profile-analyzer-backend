# ProfileLens AI

> AI-powered LinkedIn profile analysis tool. Get detailed scores, strengths, weaknesses, and personalized improvement suggestions for any public LinkedIn profile.

![Next.js](https://img.shields.io/badge/Next.js-16-black?logo=next.js)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green?logo=fastapi)
![TypeScript](https://img.shields.io/badge/TypeScript-5-blue?logo=typescript)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-4-38bdf8?logo=tailwindcss)

**Live Demo:** [ai-linkedin-profile-analyzer.vercel.app](https://ai-linkedin-profile-analyzer.vercel.app)

**Developer:** [Robiul Alam](https://robiulalamdev.vercel.app)

---

## Features

- **Multi-Provider AI Analysis** — OpenAI (GPT-4o), Google Gemini, OpenRouter
- **Profile Comparison** — Side-by-side comparison of two LinkedIn profiles
- **Encrypted Sessions** — API key encrypted with AES-256-GCM, stored in HTTP-only cookies (1-day expiry)
- **PDF Export** — Professional reports generated client-side with jsPDF
- **Detailed Scoring** — Overall score + 8 section scores with actionable suggestions
- **Recruiter Score** — ATS readiness, visibility, professionalism, networking metrics
- **Learning Recommendations** — Personalized technology and skill suggestions
- **Responsive Design** — Works on desktop, tablet, and mobile

---

## Quick Start

### Prerequisites

- **Node.js** 18+ and **npm**
- **Python** 3.11+
- An API key from one of: [OpenAI](https://platform.openai.com), [Google AI Studio](https://aistudio.google.com), or [OpenRouter](https://openrouter.ai)

### 1. Clone the Repository

```bash
git clone https://github.com/robiulalamdev/ai-linkedin-profile-analyzer.git
cd ai-linkedin-profile-analyzer
```

```bash
git clone https://github.com/robiulalamdev/ai-linkedin-profile-analyzer-frontend.git
cd ai-linkedin-profile-analyzer-frontend
git clone https://github.com/robiulalamdev/ai-linkedin-profile-analyzer-backend.git
cd ai-linkedin-profile-analyzer-backend
```

### 2. Set Up Backend

```bash
cd backend

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
ENCRYPTION_SECRET=profilelens-enc-key-2025-change-in-production
EOF

# Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend runs at `http://localhost:8000`

### 3. Set Up Frontend

```bash
cd frontend

# Install dependencies
npm install

# Create .env.local file
cat > .env.local << EOF
API_URL=http://localhost:8000
ENCRYPTION_SECRET=profilelens-enc-key-2025-change-in-production
EOF

# Start the dev server
npm run dev
```

Frontend runs at `http://localhost:3000`

### 4. Open and Use

1. Go to `http://localhost:3000`
2. Click **Start Analyzing**
3. Select your AI provider and enter your API key
4. Paste any public LinkedIn profile URL
5. Get instant AI-powered analysis!

---

## API Endpoints

| Method | Endpoint   | Description                       |
| ------ | ---------- | --------------------------------- |
| `POST` | `/analyze` | Analyze a single LinkedIn profile |
| `POST` | `/compare` | Compare two LinkedIn profiles     |
| `GET`  | `/health`  | Health check                      |

### Example Request

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "provider": "openai",
    "apiKey": "your-encrypted-api-key",
    "linkedinUrl": "https://linkedin.com/in/username"
  }'
```

---

## Tech Stack

| Layer            | Technology                                                  |
| ---------------- | ----------------------------------------------------------- |
| **Frontend**     | Next.js 16, React 19, TypeScript, Tailwind CSS 4, shadcn/ui |
| **Animations**   | Framer Motion                                               |
| **State**        | TanStack Query                                              |
| **PDF**          | jsPDF (client-side)                                         |
| **Encryption**   | AES-256-GCM (Node.js crypto + Python cryptography)          |
| **Backend**      | FastAPI, Python, Pydantic                                   |
| **AI Providers** | OpenAI, Google Gemini, OpenRouter                           |

---

## Project Structure

```
linkedin-analyzer/
├── frontend/          # Next.js app (App Router)
│   ├── src/app/       # Pages & server actions
│   ├── src/components # UI components
│   ├── src/hooks      # React hooks
│   └── src/lib        # Utilities & crypto
├── backend/           # FastAPI app
│   ├── app/routers    # API endpoints
│   ├── app/services   # AI providers & scraper
│   ├── app/models     # Pydantic schemas
│   └── app/prompts    # AI prompt templates
└── docs/              # Documentation
```

---

## How It Works

```
User → Select Provider + API Key → Encrypted Cookie
         ↓
User → Enter LinkedIn URL → Backend scrapes profile
         ↓
Backend → Sends to AI Provider → Gets structured analysis
         ↓
Frontend → Renders scores, suggestions, recommendations
         ↓
User → Exports PDF report (client-side)
```

---

## Environment Variables

| Variable            | Location                     | Description                                    |
| ------------------- | ---------------------------- | ---------------------------------------------- |
| `ENCRYPTION_SECRET` | Both `.env` and `.env.local` | Must match for encryption/decryption           |
| `API_URL`           | Frontend `.env.local`        | Backend URL (default: `http://localhost:8000`) |

---

## License

Open source — feel free to use and modify.

---

**Built by [Robiul Alam](https://robiulalamdev.vercel.app)**
