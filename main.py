from __future__ import annotations

from fastapi import FastAPI

from . import config
from .models import NexusCase
from .services import evaluate_case

app = FastAPI(title="Medical Nexus Workflow API", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/options")
def options() -> dict[str, list[str]]:
    return {
        "theory_types": config.THEORY_TYPES,
        "condition_families": config.CONDITION_FAMILIES,
        "event_types": config.EVENT_TYPES,
        "yes_no_partial": config.YES_NO_PARTIAL,
        "support_level": config.SUPPORT_LEVEL,
        "biologic_level": config.BIOLOGIC_LEVEL,
        "imaging_level": config.IMAGING_LEVEL,
        "alt_cause_level": config.ALT_CAUSE_LEVEL,
        "treatment_gap": config.TREATMENT_GAP,
        "onset_timing": config.ONSET_TIMING,
        "evidence_type": config.EVIDENCE_TYPE,
        "evidence_stance": config.EVIDENCE_STANCE,
    }


@app.post("/evaluate")
def evaluate(payload: NexusCase):
    return evaluate_case(payload)
