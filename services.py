from __future__ import annotations

from typing import Iterable

from .config import BVA_LIBRARY, SCORE_MAP, THRESHOLD_MODERATE, THRESHOLD_STRONG
from .models import BVAResult, EvaluationResult, NexusCase, QARuleResult


def _included_evidence_ids(case: NexusCase) -> set[str]:
    return {e.id for e in case.evidence if e.include}


def _validate_citations(case: NexusCase) -> list[str]:
    included = _included_evidence_ids(case)
    all_groups = {
        "diagnosis": case.reasoning.diagnosis_citation_ids,
        "timeline": case.reasoning.timeline_citation_ids,
        "event": case.reasoning.event_citation_ids,
        "mechanism": case.reasoning.mechanism_citation_ids,
        "general_support": case.reasoning.general_support_citation_ids,
        "direct": case.theory_specific.direct_citation_ids,
        "secondary": case.theory_specific.secondary_citation_ids,
        "aggravation": case.theory_specific.aggravation_citation_ids,
        "rebuttal": case.rebuttal.rebuttal_citation_ids,
    }
    errors: list[str] = []
    for label, citation_ids in all_groups.items():
        for cid in citation_ids:
            normalized = cid.strip().upper()
            if normalized and normalized not in included:
                errors.append(f"{label}: citation ID {normalized} is missing from included evidence.")
    return errors


def _score(case: NexusCase) -> tuple[int, str]:
    score = 0
    r = case.reasoning
    ts = case.theory_specific
    rebut = case.rebuttal

    def add(key: str, value: str | None) -> None:
        nonlocal score
        if value:
            score += SCORE_MAP.get(f"{key}|{value}", 0)

    add("STR", r.str_documentation_strength)
    add("Continuity", r.continuity_strength)
    add("Imaging", r.imaging_objective_support)
    add("Diagnosis", r.diagnosis_support_strength)
    add("Biologic", r.biologic_plausibility_strength)
    add("Alt", rebut.stronger_alternative_cause_present)
    add("Gap", r.treatment_gap)
    add("Functional", r.functional_impact)
    add("Lay", r.lay_evidence_strength)

    if case.theory_type == "Direct Service Connection":
        add("DirectEvent", ts.direct_event_documented)
    elif case.theory_type == "Secondary Causation":
        add("SecondaryPrimary", ts.secondary_primary_confirmed)
    elif case.theory_type == "Aggravation":
        if ts.aggravation_baseline_severity and ts.aggravation_worsening_evidence and ts.aggravation_beyond_natural_progression:
            score += SCORE_MAP["AggravationParts|Complete"]
        elif any([
            ts.aggravation_baseline_severity,
            ts.aggravation_worsening_evidence,
            ts.aggravation_beyond_natural_progression,
        ]):
            score += SCORE_MAP["AggravationParts|Partial"]
        else:
            score += SCORE_MAP["AggravationParts|Missing"]

    if score >= THRESHOLD_STRONG:
        category = "Strong"
    elif score >= THRESHOLD_MODERATE:
        category = "Moderate"
    else:
        category = "Weak"
    return score, category


def _bva_match(case: NexusCase) -> BVAResult | None:
    for row in BVA_LIBRARY:
        if (
            row["condition_family"] == case.condition_family
            and row["event_type"] == case.event_type
            and row["theory_type"] == case.theory_type
        ):
            return BVAResult(
                key_reasoning_pattern=row["key_reasoning_pattern"],
                what_to_emphasize=row["what_to_emphasize"],
                what_to_address=row["what_to_address"],
                common_failure_points=row["common_failure_points"],
                best_framing=row["best_framing"],
            )
    return None


def _records_reviewed(case: NexusCase) -> str:
    included = [e for e in case.evidence if e.include and e.document_name]
    if not included:
        return ""
    parts = []
    for item in included:
        if item.document_date:
            parts.append(f"{item.document_name} ({item.document_date:%-m/%-d/%Y})")
        else:
            parts.append(item.document_name)
    return "Records reviewed include: " + "; ".join(parts) + "."


def _qa(case: NexusCase, citation_errors: list[str]) -> list[QARuleResult]:
    r = case.reasoning
    ts = case.theory_specific
    rebut = case.rebuttal
    rules: list[QARuleResult] = []

    def status(ok: bool) -> str:
        return "PASS" if ok else "FAIL"

    rules.append(QARuleResult(rule="Theory selected", status=status(bool(case.theory_type)), how_to_fix="Choose one theory at the top."))
    rules.append(QARuleResult(rule="Diagnosis entered", status=status(bool(case.diagnosis)), how_to_fix="Enter a specific current diagnosis."))
    rules.append(QARuleResult(rule="Diagnosis support + citations", status=status(bool(r.diagnosis_evidence_summary and r.diagnosis_citation_ids)), how_to_fix="Explain why the diagnosis is supported and add evidence IDs."))
    rules.append(QARuleResult(rule="Evidence log has at least 3 included sources", status=status(sum(1 for e in case.evidence if e.include) >= 3), how_to_fix="Log enough records to support your reasoning."))
    rules.append(QARuleResult(rule="Timeline/continuity explained", status=status(bool(r.onset_timing and r.continuity_strength and r.timeline_explanation and r.timeline_citation_ids)), how_to_fix="Explain timing and add evidence IDs."))
    rules.append(QARuleResult(rule="Mechanism explained + cited", status=status(bool(r.biologic_plausibility_strength and r.medical_mechanism_explanation and r.mechanism_citation_ids)), how_to_fix="State the medical mechanism and cite support."))
    rules.append(QARuleResult(rule="Unfavorable evidence acknowledged", status=status(bool(rebut.stronger_alternative_cause_present and rebut.alternative_cause_summary and rebut.unfavorable_evidence_summary)), how_to_fix="You must address negative facts."))
    rebut_ok = (rebut.stronger_alternative_cause_present == "None") or bool(rebut.rebuttal and rebut.rebuttal_citation_ids)
    rules.append(QARuleResult(rule="Rebuttal completed if needed", status=status(rebut_ok), how_to_fix="If alternatives exist, explain why they are less persuasive."))

    direct_ok = True
    secondary_ok = True
    aggravation_ok = True
    if case.theory_type == "Direct Service Connection":
        direct_ok = bool(ts.direct_event_documented and ts.direct_service_reasoning and ts.direct_citation_ids)
    if case.theory_type == "Secondary Causation":
        secondary_ok = bool(case.primary_sc_condition and ts.secondary_primary_confirmed and ts.secondary_mechanism and ts.secondary_citation_ids)
    if case.theory_type == "Aggravation":
        aggravation_ok = bool(case.primary_sc_condition and ts.aggravation_baseline_severity and ts.aggravation_worsening_evidence and ts.aggravation_beyond_natural_progression and ts.aggravation_citation_ids)

    rules.append(QARuleResult(rule="Direct path complete", status=status(direct_ok), how_to_fix="Direct theory requires event + mechanism + citations."))
    rules.append(QARuleResult(rule="Secondary path complete", status=status(secondary_ok), how_to_fix="Secondary theory requires primary SC condition + link mechanism."))
    rules.append(QARuleResult(rule="Aggravation path complete", status=status(aggravation_ok), how_to_fix="Aggravation requires baseline + worsening + beyond natural progression + citations."))
    rules.append(QARuleResult(rule="Citations resolve to included evidence", status=status(not citation_errors), how_to_fix="Fix any missing citation IDs or mark the underlying evidence as included."))

    return rules


def _draft(case: NexusCase, score_category: str, ready: bool) -> dict[str, str]:
    if not ready:
        return {"executive_summary": "FINAL DRAFT LOCKED: complete every FAIL item in the QA dashboard above."}

    r = case.reasoning
    ts = case.theory_specific
    rebut = case.rebuttal
    if case.theory_type == "Direct Service Connection":
        relationship = f"the in-service event/exposure described as {case.event_type}"
        theory_analysis = f"Direct-theory analysis: {ts.direct_service_reasoning} (citations: {', '.join(ts.direct_citation_ids)})."
        conclusion_link = "caused by the in-service event/exposure described above"
    elif case.theory_type == "Secondary Causation":
        relationship = f"the service-connected condition of {case.primary_sc_condition}"
        theory_analysis = f"Secondary-theory analysis: the primary service-connected condition is {case.primary_sc_condition} and the medical link is {ts.secondary_mechanism} (citations: {', '.join(ts.secondary_citation_ids)})."
        conclusion_link = f"proximately due to the service-connected condition of {case.primary_sc_condition}"
    else:
        relationship = "military service through permanent aggravation beyond natural progression"
        theory_analysis = (
            f"Aggravation analysis: baseline severity was {case.primary_sc_condition}. "
            f"Baseline details: {ts.aggravation_baseline_severity}. "
            f"Worsening evidence: {ts.aggravation_worsening_evidence}. "
            f"The worsening exceeds natural progression because {ts.aggravation_beyond_natural_progression} "
            f"(citations: {', '.join(ts.aggravation_citation_ids)})."
        )
        conclusion_link = "permanently aggravated beyond its natural progression by military service"

    return {
        "executive_summary": (
            f"This independent medical opinion addresses whether the claimant's condition of {case.diagnosis} "
            f"is at least as likely as not related to {relationship}. Based on the records reviewed, clinical history, "
            f"and the medical reasoning documented in this application, the threshold of at least as likely as not is "
            f"{'not yet supported' if score_category == 'Weak' else 'met'}."
        ),
        "records_reviewed": _records_reviewed(case),
        "relevant_history": (
            f"The diagnosis of {case.diagnosis} is supported by {r.diagnosis_evidence_summary} "
            f"(citations: {', '.join(r.diagnosis_citation_ids)}). The relevant timeline is {str(r.onset_timing).lower()}, "
            f"with continuity assessed as {str(r.continuity_strength).lower()}. The chronology is explained as follows: "
            f"{r.timeline_explanation} (citations: {', '.join(r.timeline_citation_ids)})."
        ),
        "medical_analysis": (
            f"Medical analysis: the service relationship is supported by {str(r.biologic_plausibility_strength).lower()} biological plausibility. "
            f"Mechanistically, {r.medical_mechanism_explanation} (citations: {', '.join(r.mechanism_citation_ids)}). "
            f"STR documentation is assessed as {str(r.str_documentation_strength).lower()}. "
            f"Imaging/objective support is {str(r.imaging_objective_support).lower()}. "
            f"Functional impact is {str(r.functional_impact).lower()} and lay evidence is {str(r.lay_evidence_strength).lower()}. "
            f"{theory_analysis}"
        ),
        "unfavorable_evidence": (
            f"Unfavorable evidence and alternative causes were considered. Alternative-cause strength is assessed as "
            f"{str(rebut.stronger_alternative_cause_present).lower()}. The main competing explanation(s) are: "
            f"{rebut.alternative_cause_summary}. Additional unfavorable facts include: {rebut.unfavorable_evidence_summary}. "
            f"These do not outweigh the service-related explanation because {rebut.rebuttal} "
            f"(citations: {', '.join(rebut.rebuttal_citation_ids)})."
        ),
        "conclusion": (
            f"It is my professional medical opinion that the claimant's condition of {case.diagnosis} is at least as likely as not "
            f"(50 percent probability or greater) {conclusion_link}. This conclusion rests on the diagnosis support, timeline, medical mechanism, "
            f"consideration of unfavorable evidence, and the absence of a more persuasive alternative explanation."
        ),
        "statement_of_truth": (
            "This draft is generated from a rule-based application designed to support complete reasoning. "
            "Final clinician review, edits, and signature remain required before use."
        ),
        "signature_block": (
            f"{case.provider_name or ''}{(', ' + case.provider_credentials) if case.provider_credentials else ''}\n"
            f"Date: {case.opinion_date.strftime('%-m/%-d/%Y') if case.opinion_date else ''}\n"
            "Signature: __________________________"
        ),
    }


def evaluate_case(case: NexusCase) -> EvaluationResult:
    citation_errors = _validate_citations(case)
    total_score, score_category = _score(case)
    qa_results = _qa(case, citation_errors)
    ready = all(item.status == "PASS" for item in qa_results)
    draft = _draft(case, score_category, ready)
    return EvaluationResult(
        total_score=total_score,
        score_category=score_category,
        qa_results=qa_results,
        ready_to_draft=ready,
        cited_evidence_errors=citation_errors,
        bva_match=_bva_match(case),
        draft=draft,
    )
