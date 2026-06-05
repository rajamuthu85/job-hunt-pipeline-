# job-hunt-pipeline

A Claude Code plugin that runs an end-to-end job-hunt workflow from a single resume.

## What it does
Bundles 6 specialist subagents, orchestrated in sequence:

```
/run-pipeline <resume>
   └─ resume-analyser            → ATS-optimized resume .docx (dated)
        └─ india-germany-job-finder   → jobs table (apply URL, recruiter email, company summary)
             └─ job-search-jd-analyser    → JD breakdown + fit %
                  └─ job-application-assistant → tailored cover letters .docx (top 3–5)
                       └─ job-email-drafter   → Gmail draft (optional, never sends)
```

`job-pipeline-orchestrator` is the coordinating agent; `/run-pipeline` is the entry command.

## Usage
```
/run-pipeline "D:\path\to\resume.docx"
/run-pipeline "D:\path\to\resume.docx" India and Germany, DevOps lead
```

## Install
Copy this folder into a Claude Code plugin location, or add its parent as a marketplace:
```
/plugin marketplace add D:\Claude_Projects\plugins
/plugin install job-hunt-pipeline
```
Then invoke `/run-pipeline <resume-path>`.

## Outputs (saved next to the resume)
- `<Name>_ATS_Optimized_<YYYY-MM-DD>.docx`
- `Cover_Letters_<Name>_<YYYY-MM-DD>.docx`

## Guardrails
- Never fabricates job listings or recruiter emails.
- Never submits applications or sends email — drafts/files only.
- Never overwrites the original resume.

## Requirements
- Python with `python-docx` (for .docx generation), or Microsoft Word (COM fallback).

---

## Projects

| Folder | Description |
|--------|-------------|
| [`german-school-system/`](german-school-system/) | Plain-language guide to the German school system, universities & top Gymnasiums near Heinickestraße, Essen |
