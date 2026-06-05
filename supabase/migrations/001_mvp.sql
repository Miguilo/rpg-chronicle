-- Migration 001: MVP schema (Phase 0)
-- Only the minimum tables needed to get the system working end-to-end

create extension if not exists vector;

-- Campaigns: a group of players playing together (maps to a Discord server)
create table campaigns (
  id                  uuid primary key default gen_random_uuid(),
  discord_server_id   text not null unique,
  name                text not null,
  created_at          timestamptz default now(),
  settings            jsonb default '{}'
);

-- Campaign members: who belongs to which campaign
create table campaign_members (
  campaign_id         uuid references campaigns(id) on delete cascade,
  discord_user_id     text not null,
  role                text check (role in ('gm', 'player')) default 'player',
  joined_at           timestamptz default now(),
  primary key (campaign_id, discord_user_id)
);

-- Sessions: a single game session (one evening of play)
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

-- Session chunks: pieces of transcript text with embeddings for vector search
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
