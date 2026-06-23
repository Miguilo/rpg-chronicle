# Architecture Decisions

Notes on structural choices: where files live, how modules connect, separation of concerns, and why.

---

### Why not use an interface/abstract class for LLM providers?
**Date:** 2026-06-09
**Context:** Discussing openai_client.py and embedder.py design
**Answer/Decision:** An abstract `EmbeddingProvider` interface would make swapping providers (OpenAI → Anthropic) clean, but it's premature when you only have one implementation. This is the YAGNI principle: don't abstract before you have a second real consumer. The cost of refactoring later is low because `embedder.py` is already the single point of change. Add the interface when: (1) you have two providers, (2) you need runtime fallback, or (3) you need a mock for testing.

---

### Steering doc should be lean — context + tech only
**Date:** 2026-06-09
**Context:** Reviewing the rpg-chronicle.md steering file after Phase 0 pipeline completion
**Answer/Decision:** Steering files should contain only what influences Kiro's behavior: project context, stack, structure, phases/checklists, schema, anti-patterns, commands, and agent rules. Educational content (concepts explained, learning questions, cost estimates) belongs in `docs/learning/` or the `helping-dev` skill — not in steering, which is read on every interaction and should stay focused.

---

