from datetime import date

from app.models import EvidenceItem, NexusCase
from app.services import evaluate_case


def test_direct_case_ready_to_draft():
    case = NexusCase(
        case_id="CASE-TEST",
        opinion_date=date(2026, 3, 22),
        provider_name="Tester",
        theory_type="Direct Service Connection",
        condition_family="Tinnitus/Hearing",
        diagnosis="Tinnitus",
        event_type="Acoustic Trauma",
        evidence=[
            EvidenceItem(id="E01", include=True, document_name="STR"),
            EvidenceItem(id="E02", include=True, document_name="Lay Statement"),
            EvidenceItem(id="E03", include=True, document_name="Audiology"),
        ],
    )
    case.reasoning.diagnosis_support_strength = "Strong"
    case.reasoning.diagnosis_evidence_summary = "Diagnosis supported"
    case.reasoning.diagnosis_citation_ids = ["E03"]
    case.reasoning.onset_timing = "During service"
    case.reasoning.continuity_strength = "Strong"
    case.reasoning.timeline_explanation = "Started in service"
    case.reasoning.timeline_citation_ids = ["E01", "E02"]
    case.reasoning.biologic_plausibility_strength = "Clear"
    case.reasoning.medical_mechanism_explanation = "Mechanism explained"
    case.reasoning.mechanism_citation_ids = ["E01"]
    case.reasoning.str_documentation_strength = "Yes"
    case.rebuttal.stronger_alternative_cause_present = "None"
    case.rebuttal.alternative_cause_summary = "No stronger cause"
    case.rebuttal.unfavorable_evidence_summary = "Some delay in treatment"
    case.theory_specific.direct_event_documented = "Yes"
    case.theory_specific.direct_service_reasoning = "Direct link explained"
    case.theory_specific.direct_citation_ids = ["E01", "E02", "E03"]

    result = evaluate_case(case)
    assert result.ready_to_draft is True
    assert result.total_score >= 0
    assert "conclusion" in result.draft
