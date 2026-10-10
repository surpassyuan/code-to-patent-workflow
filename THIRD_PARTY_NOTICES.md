# Third-party notices

The workflow's original orchestration, evidence engine, adapters and tests are
licensed under the root MIT license. The following unmodified upstream snapshots
are redistributed under their original licenses. Their authorship is not claimed
as original work by this workflow's author.

| Upstream | Pinned commit | License and copyright |
|---|---|---|
| [Oscima2026/china-patent-drafter-skill](https://github.com/Oscima2026/china-patent-drafter-skill) | `71e61bb073c20d3a974f3fc041d9f17c61228e5b` | MIT, Copyright (c) 2026; retained verbatim in `vendor/china-patent-drafter-skill/LICENSE` |
| [handsomestWei/patent-disclosure-skill](https://github.com/handsomestWei/patent-disclosure-skill) | `6935a14d342ed9c7a07440c999d1b7bf1852a701` | MIT, Copyright (c) 2026 handsomestWei; retained verbatim in `vendor/patent-disclosure-skill/LICENSE` |

Downloaded on 2026-10-10. `vendor/manifest.json` records every redistributed
upstream file and SHA-256. Bundled third-party assets retain their adjacent license
notices, including the upstream map's Three.js notice. Git metadata is excluded.

## What was integrated

- China patent drafter: claim-first drafting, operational S1-Sn embodiments,
  specification/claim/figure alignment, editable Word equations and visual QA.
- China patent disclosure: invention-point extraction, source-aware prior-art
  comparisons, disclosure self-check and bounded iterative revision; its local
  Mermaid renderer and application Markdown-to-DOCX converter are used by the
  optional export adapter.
- Local additions: code-first ordering, activation/origin/effect distinctions,
  claim-to-feature-to-code links, immutable multi-artifact revisions and three
  recorded review perspectives across at least two rounds.

The bundled repositories contain broader capabilities (CAD, maps, office-action
responses, etc.). Bundling does not enable them, establish their correctness or
authorize extra actions. Only the adapters described in `docs/integration.md`
participate in the default workflow. No upstream setup script is run automatically.
