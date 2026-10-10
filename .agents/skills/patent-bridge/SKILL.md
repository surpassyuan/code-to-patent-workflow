---
name: patent-bridge
description: Integrate pinned Chinese patent drafting and disclosure skills with a code-grounded evidence workflow. Use for invention-point analysis, prior-art comparison, claims/specification drafting and reviewed Word export from source code.
---

# 中国专利技能融合桥

Locate the complete repository containing `scripts/workflow.py`. Read
`docs/integration.md`; the original upstream snapshots remain under `vendor/`.
This skill requires the full repository, not a detached SKILL.md.

Select the deliverable from the user's request. For a technical disclosure, use
the disclosure branch. For a full application, also use the application branch.
An application request already authorizes this branch; do not ask for the same
authorization again. Bundled patent maps, CAD, layouts and office-action tools
remain outside this workflow unless needed by the actual request.

## Disclosure branch

Read `vendor/patent-disclosure-skill/skills/patent-disclosure/SKILL.md`, then load
its invention-point, prior-art and self-check prompts only as needed. Replace its
document-first scan ordering with source code → saved config → call path → logs
→ inventor explanations → supporting documents. Preserve source files. Write all
case outputs outside the public repository under the selected case directory.

Tie each candidate invention point to active feature IDs and code evidence.
Perform a deletion test to separate necessary and optional features. Describe the
technical problem without embedding the proposed solution in its wording.
Search with public general technical terms; record source URL, access date,
paragraph/claim locator and whether only the abstract or full text was read.
Unavailable search is `not-searched`; partial search is not a novelty conclusion.

## Application branch

Read `vendor/china-patent-drafter-skill/china-patent-drafter/SKILL.md`, and relevant
claim-strategy/consistency prompts from
`vendor/patent-disclosure-skill/skills/patent-application/`.
Apply claim-first planning, concrete S1-Sn implementation, specification support,
terminology/figure alignment and editable formulas. Use enough dependent claims
to support the case; do not invent content to reach the upstream's suggested count.
Unimplemented alternatives belong in a separately labelled proposed-design note,
not a claimed tested embodiment.

Fill the schema in `docs/application-contract.md` and call:

```text
python scripts/workflow.py draft --case <case> --features <working-features.json> --application <working-application.json> --reason <revision reason>
```

The resulting claims, specification, abstract, drawing sources and support map
are frozen with the disclosure. Each review must include the exact
`artifact_hashes` from the current manifest. Repeat all three review perspectives
after any substantive revision, across at least two rounds. Old findings cannot
clear a new application file.

For complete Word requests, use `scripts/export_docx.py --case <case>` with the
optional dependencies. It invokes the pinned local Mermaid and DOCX converters.
Check `export-status.json`, render pages with available document tools and inspect
figures, Chinese glyphs, equations and page breaks. Repair failed editable equations
before final delivery. Export alone is a formatting candidate, not visual QA.

## Conflict handling

User scope and facts take priority. The local evidence/revision contract controls
what can be described as implemented. Upstream formatting guidance cannot replace
missing code/effect evidence. Clarify facts only when they block the requested
result; do not import unrelated upstream confirmation flows. Keep uncertainties
in the review appendix, while making the supported technical narrative readable.
