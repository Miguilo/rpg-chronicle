# Architecture Decisions

Notes on structural choices: where files live, how modules connect, separation of concerns, and why.

---

### Why not use an interface/abstract class for LLM providers?
**Date:** 2026-06-09
**Context:** Discussing openai_client.py and embedder.py design
**Answer/Decision:** An abstract `EmbeddingProvider` interface would make swapping providers (OpenAI → Anthropic) clean, but it's premature when you only have one implementation. This is the YAGNI principle: don't abstract before you have a second real consumer. The cost of refactoring later is low because `embedder.py` is already the single point of change. Add the interface when: (1) you have two providers, (2) you need runtime fallback, or (3) you need a mock for testing.

---

