from __future__ import annotations

from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


class EvidenceItem(BaseModel):
    id: str = Field(..., description="Evidence ID, e.g. E01")
    include: bool = True
    source_type: Optional[str] = None
    document_date: Optional[date] = None
    document_name: Optional[str] = None
    key_finding: Optional[str] = None
    relevance: Optional[str] = None
    page_reference: Optional[str] = None
    stance: Optional[str] = None

    @field_validator("id")
    @classmethod
    def validate_id(cls, value: str) -> str:
        value = value.strip().upper()
        if not value.startswith("E"):
            raise ValueError("Evidence IDs must start with 'E'.")
        return value


class GuidedReasoning(BaseModel):
    diagnosis_support_strength: Optional[str] = None
    diagnosis_evidence_summary: Optional[str] = None
    diagnosis_citation_ids: List[str] = Field(default_factory=list)
    onset_timing: Optional[str] = None
    continuity_strength: Optional[str] = None
    timeline_explanation: Optional[str] = None
    timeline_citation_ids: List[str] = Field(default_factory=list)
    str_documentation_strength: Optional[str] = None
    event_exposure_summary: Optional[str] = None
    event_citation_ids: List[str] = Field(default_factory=list)
    biologic_plausibility_strength: Optional[str] = None
    medical_mechanism_explanation: Optional[str] = None
    mechanism_citation_ids: List[str] = Field(default_factory=list)
    imaging_objective_support: Optional[str] = None
    functional_impact: Optional[str] = None
    lay_evidence_strength: Optional[str] = None
    treatment_gap: Optional[str] = None
    treatment_gap_explanation: Optional[str] = None
    general_support_citation_ids: List[str] = Field(default_factory=list)


class TheorySpecific(BaseModel):
    direct_event_documented: Optional[str] = None
    direct_service_reasoning: Optional[str] = None
    direct_citation_ids: List[str] = Field(default_factory=list)
    secondary_primary_confirmed: Optional[str] = None
    secondary_mechanism: Optional[str] = None
    secondary_citation_ids: List[str] = Field(default_factory=list)
    aggravation_baseline_severity: Optional[str] = None
    aggravation_worsening_evidence: Optional[str] = None
    aggravation_beyond_natural_progression: Optional[str] = None
    aggravation_citation_ids: List[str] = Field(default_factory=list)


class RebuttalSection(BaseModel):
    stronger_alternative_cause_present: Optional[str] = None
    alternative_cause_summary: Optional[str] = None
    unfavorable_evidence_summary: Optional[str] = None
    rebuttal: Optional[str] = None
    rebuttal_citation_ids: List[str] = Field(default_factory=list)


class NexusCase(BaseModel):
    case_id: Optional[str] = None
    opinion_date: Optional[date] = None
    provider_name: Optional[str] = None
    provider_credentials: Optional[str] = None
    veteran_claimant: Optional[str] = None
    theory_type: Optional[str] = None
    condition_family: Optional[str] = None
    diagnosis: Optional[str] = None
    event_type: Optional[str] = None
    primary_sc_condition: Optional[str] = None
    str_records_date_range: Optional[str] = None
    evidence: List[EvidenceItem] = Field(default_factory=list)
    reasoning: GuidedReasoning = Field(default_factory=GuidedReasoning)
    theory_specific: TheorySpecific = Field(default_factory=TheorySpecific)
    rebuttal: RebuttalSection = Field(default_factory=RebuttalSection)


class QARuleResult(BaseModel):
    rule: str
    status: str
    how_to_fix: Optional[str] = None


class BVAResult(BaseModel):
    key_reasoning_pattern: Optional[str] = None
    what_to_emphasize: Optional[str] = None
    what_to_address: Optional[str] = None
    common_failure_points: Optional[str] = None
    best_framing: Optional[str] = None


class EvaluationResult(BaseModel):
    total_score: int
    score_category: str
    qa_results: List[QARuleResult]
    ready_to_draft: bool
    cited_evidence_errors: List[str] = Field(default_factory=list)
    bva_match: Optional[BVAResult] = None
    draft: dict[str, str] = Field(default_factory=dict)
