# RPG Chronicle — Steering Document

## Project Philosophy

**MVP first, robustness later.** Each phase delivers something functional and demonstrable.

**Everything in English.** Code, comments, docs, commit messages, variable names — all English.

The frontend can be built with help from **Google Stitch** to speed up visual prototyping.

---

## What is RPG Chronicle

A system that records tabletop RPG sessions (via Discord/Craig Bot), transcribes them, extracts entities and relationships (characters, locations, factions), indexes everything into a knowledge graph, and allows natural language queries about what happened in the campaign.

---

## Definitive Stack

| Layer | Choice | Reason |
|-------|--------|--------|
| Frontend | Next.js 15 (App Router) | RSC, streaming, industry standard |
| Backend/Pipeline | Python + UV (Astral) | Python for ML/NLP; UV is fast and modern |
| Auth | Supabase Auth (native Discord OAuth) | Zero auth code — dashboard configuration |
| DB + Vector | Supabase (PostgreSQL + pgvector) | Less infra, generous free tier, pgvector for embeddings |
| Queue | ARQ (Phase 1+) | asyncio-native, simple. Not needed in MVP |
| Graph | LightRAG + NetworkX (Phase 3) | LightRAG manages the graph; Neo4j only if it scales too much |
| Monorepo | Turborepo (JS only) | Manages Next.js + Discord bot. Python managed by UV separately |
| Observability | Langfuse (Phase 5) | LLM pipeline traces, open source |
| Analytics | PostHog (Phase 5) | Product analytics |
| UI Prototyping | Google Stitch | Speed up frontend component creation |

---

## Monorepo Structure

```
rpg-chronicle/
├── apps/
│   ├── web/                    # Next.js 15 app (frontend)
│   └── backend/                # Python pipeline service (UV)
├── discord-bot/                # Node.js/TypeScript bot (Phase 4)
├── supabase/
│   ├── migrations/             # Versioned SQL migrations (one per phase)
│   └── seed.sql                # Example data for development
├── docs/
│   └── learning/               # Developer learning notes (auto-populated)
├── turbo.json
├── .env.example
└── README.md
```

---

## MVP → Production Phases

### PHASE 0 — Working MVP (week 1)
**Goal: end-to-end pipeline running.**

1. Monorepo setup (pnpm + turbo.json + folder structure)
2. Supabase: cloud project + MVP migration (campaigns, sessions, session_chunks)
3. `.env.example` → `.env` local with credentials
4. `apps/backend`: FastAPI + uvicorn + openai + supabase
5. Pipeline: POST /ingest → chunk → embed → save to Supabase
6. `apps/web`: Next.js with Discord OAuth login + session list
7. Seed data script for testing

**Success criteria**: log in, see a session, chunks in database.

### PHASE 1 — Solid Foundation (weeks 2-3)
**Goal: organized, testable code with clear patterns.**

8. Pydantic Settings for typed config
9. Async Supabase client singleton
10. Repository pattern for DB queries
11. Chunker + unit tests
12. Transcriber (Whisper API)
13. Entity extractor (Claude Haiku) + tests
14. Audio service (download + merge with ffmpeg)
15. ARQ worker + trigger endpoint
16. Full migration: entities, entity_relations, chat_queries
17. Basic RAG chat endpoint
18. GitHub Actions CI (lint + type check + tests)
19. **Evolve git workflow**: Update `phase-0-git-reminder` hook to require PRs + CI green. Branch protection on `main`.

**Success criteria**: real audio processed, entities extracted, chat answers questions.

### PHASE 2 — Real Frontend (weeks 4-5)
**Goal: usable interface.**

20. Supabase SSR setup (client.ts + server.ts)
21. Polished Discord OAuth login
22. Dashboard: campaign list (Server Component)
23. Campaign page: sessions + pipeline status
24. Chat with vector RAG (streaming)
25. UI components via Google Stitch
26. RLS enabled

**Success criteria**: another person can log in, see their campaign, chat with the bot.

### PHASE 3 — Graph RAG (month 2)
**Goal: the project's differentiator.**

27. LightRAG integration
28. Hybrid query (vector + graph)
29. Entity graph visualization
30. Entity detail page

**Success criteria**: "who knows Theron?" returns graph-based answers.

### PHASE 4 — Discord Bot + Automation (month 2-3)
**Goal: complete flow without leaving Discord.**

31. Bot with `/start-session` and `/end-session`
32. Automatic pipeline trigger via webhook
33. Completion notification in channel
34. `/ask` command for queries

**Success criteria**: record → auto-process → query from Discord.

### PHASE 5 — Quality and Portfolio (month 3)
**Goal: presentable and documented project.**

35. Langfuse on all spans
36. Integration tests
37. README with architecture + demo
38. Metrics: cost/session, p50/p95 latency
39. Deploy: Vercel (frontend) + Railway/Fly.io (pipeline)

**Success criteria**: clone → understand → see running demo.

---

## Database Schema

### Migration 001 — MVP (Phase 0)

```sql
create extension if not exists vector;

create table campaigns (
  id                  uuid primary key default gen_random_uuid(),
  discord_server_id   text not null unique,
  name                text not null,
  created_at          timestamptz default now(),
  settings            jsonb default '{}'
);

create table campaign_members (
  campaign_id         uuid references campaigns(id) on delete cascade,
  discord_user_id     text not null,
  role                text check (role in ('gm', 'player')) default 'player',
  joined_at           timestamptz default now(),
  primary key (campaign_id, discord_user_id)
);

create table sessions (
  id                  uuid primary key default gen_random_uuid(),
  campaign_id         uuid references campaigns(id) on delete cascade,
  session_number      integer not null,
  title               text,
  recorded_at         timestamptz,
  duration_seconds    integer,
  status              text check (status in (
                        'recording', 'processing', 'indexing', 'ready', 'error'
                      )) default 'recording',
  audio_path          text,
  transcript_path     text,
  summary             jsonb,
  error_message       text,
  created_at          timestamptz default now(),
  unique(campaign_id, session_number)
);

create table session_chunks (
  id                uuid primary key default gen_random_uuid(),
  session_id        uuid references sessions(id) on delete cascade,
  campaign_id       uuid references campaigns(id) on delete cascade,
  content           text not null,
  chunk_index       integer not null,
  speaker           text,
  timestamp_start   integer,
  timestamp_end     integer,
  embedding         vector(1536),
  created_at        timestamptz default now()
);

create index on session_chunks (session_id, chunk_index);
```

### Migration 002 — Entities and Relations (Phase 1)

```sql
create table entities (
  id                      uuid primary key default gen_random_uuid(),
  campaign_id             uuid references campaigns(id) on delete cascade,
  name                    text not null,
  type                    text check (type in (
                            'character', 'location', 'faction',
                            'item', 'event', 'secret', 'concept'
                          )),
  description             text,
  first_seen_session_id   uuid references sessions(id),
  last_seen_session_id    uuid references sessions(id),
  metadata                jsonb default '{}',
  embedding               vector(1536),
  created_at              timestamptz default now(),
  unique(campaign_id, name, type)
);

create table entity_relations (
  id              uuid primary key default gen_random_uuid(),
  campaign_id     uuid references campaigns(id) on delete cascade,
  source_id       uuid references entities(id) on delete cascade,
  target_id       uuid references entities(id) on delete cascade,
  relation_type   text not null,
  description     text,
  confidence      float default 1.0,
  session_id      uuid references sessions(id),
  created_at      timestamptz default now()
);

create table chat_queries (
  id                uuid primary key default gen_random_uuid(),
  campaign_id       uuid references campaigns(id) on delete cascade,
  user_discord_id   text not null,
  query             text not null,
  response          text,
  sources           jsonb,
  latency_ms        integer,
  feedback          smallint,
  created_at        timestamptz default now()
);

create index on entities (campaign_id, type);
create index on entity_relations (campaign_id, source_id, target_id);
```

### Migration 003 — RLS (Phase 2)

```sql
alter table campaigns enable row level security;
alter table sessions enable row level security;
alter table entities enable row level security;
alter table entity_relations enable row level security;
alter table session_chunks enable row level security;
alter table chat_queries enable row level security;

create or replace function is_campaign_member(p_campaign_id uuid)
returns boolean as $$
  select exists (
    select 1 from campaign_members
    where campaign_id = p_campaign_id
    and discord_user_id = (auth.jwt() ->> 'sub')
  );
$$ language sql security definer;

create policy "members_read_campaigns" on campaigns
  for select using (is_campaign_member(id));

create policy "members_read_sessions" on sessions
  for select using (is_campaign_member(campaign_id));

create policy "members_read_entities" on entities
  for select using (is_campaign_member(campaign_id));

create policy "members_read_chunks" on session_chunks
  for select using (is_campaign_member(campaign_id));
```

---

## What NOT to Do

- **Don't implement auth from scratch** — use Supabase Auth.
- **Don't create a design system** — use shadcn/ui or Stitch output.
- **Don't optimize before measuring** — ivfflat, caching only with data + metrics.
- **Don't use Neo4j** — pgvector + LightRAG is enough at this scope.
- **Don't deploy before Phase 5** — run locally until presentable.
- **Don't process real audio in Phase 0** — text input only.
- **Don't over-engineer** — no classes/factories/interfaces for 10-line functions.

---

## Useful Commands

```bash
# UV (Python)
uv sync                              # install deps
uv add <pkg>                         # add dependency
uv run uvicorn chronicle.api:app --reload --port 8001  # run API
uv run pytest                        # tests
uv run ruff check .                  # lint

# Monorepo (JavaScript)
pnpm install                         # install everything
pnpm --filter web dev                # frontend only

# Supabase
supabase start                       # local DB
supabase db push                     # apply migrations to cloud
```

---

## Rules for Kiro

1. **MVP first**: simplest version that works before adding robustness.
2. **Don't skip phases**: follow phase order.
3. **Working code > perfect code**: in Phase 0, shortcuts are acceptable.
4. **Tests come in Phase 1**: Phase 0 = make it work.
5. **Frontend with Stitch**: suggest components for Google Stitch when building UI.
6. **Everything in English**: code, comments, docs, commits.
7. **Incremental**: each commit leaves the project in a working state.

See the `helping-dev` skill for learning process rules (ritual, review format, naming discussions, stuck mode).
