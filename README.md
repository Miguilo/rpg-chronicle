# RPG Chronicle

AI-powered knowledge graph for tabletop RPG campaigns. Records sessions, transcribes audio, extracts entities/relationships, and enables natural language queries about your campaign history.

## Stack

- **Frontend**: Next.js 15 (App Router)
- **Pipeline**: Python + FastAPI (managed by UV)
- **Database**: Supabase (PostgreSQL + pgvector)
- **Auth**: Supabase Auth (Discord OAuth)
- **Monorepo**: Turborepo + pnpm

## Project Structure

```
rpg-chronicle/
├── apps/
│   ├── web/          # Next.js frontend
│   └── backend/      # Python backend (UV)
├── supabase/
│   └── migrations/   # Versioned SQL migrations
├── turbo.json        # Turborepo config
└── package.json      # Root workspace
```

## Getting Started

### Prerequisites

- Node.js 20+
- pnpm (`npm install -g pnpm`)
- UV (`curl -LsSf https://astral.sh/uv/install.sh | sh`)

### Setup

```bash
# Install JS dependencies (Next.js + Turborepo)
pnpm install

# Install Python dependencies
cd apps/backend
uv sync

# Copy environment variables
cp .env.example .env
# Fill in your Supabase and OpenAI credentials
```

### Running

```bash
# Frontend (from root)
pnpm --filter web dev

# Backend API (from apps/backend)
uv run uvicorn chronicle.api:app --reload --port 8001
```

## Development Phase

Currently in **Phase 0 — Working MVP**. See `.kiro/steering/rpg-chronicle.md` for the full roadmap.
