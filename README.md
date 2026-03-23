# Medical Nexus Workflow Python Starter

This is a Python starter rebuild of the Excel-guided medical nexus workflow. It converts the core workbook structure into a small FastAPI service that can be used inside a web application.

## What is included

- Structured data models for a nexus case
- Evidence log support
- Citation validation against included evidence
- Theory-specific QA rules for direct, secondary, and aggravation pathways
- Scoring engine translated from the workbook
- Draft section generation
- BVA pattern matching starter logic
- API endpoints for options and case evaluation

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then open the API docs at:

```text
http://127.0.0.1:8000/docs
```

## Test with the sample payload

```bash
curl -X POST http://127.0.0.1:8000/evaluate \
  -H "Content-Type: application/json" \
  -d @sample_case.json
```

## What should be built next

- Authentication and billing
- Persistent case storage
- Word/PDF letter export
- Frontend workflow UI
- Stronger narrative-quality checks
- More complete BVA library matching
- Role-based admin tools
- Audit logging

## Important note

This is a code-first starter based on the workbook's current logic. It should be treated as a foundation for a production app, not as a finished medical or legal product.
