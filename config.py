from __future__ import annotations

THEORY_TYPES = [
    "Direct Service Connection",
    "Secondary Causation",
    "Aggravation",
]

CONDITION_FAMILIES = [
    "Migraine/Headache",
    "Tinnitus/Hearing",
    "Back/Orthopedic",
    "Respiratory/Asthma",
    "Mental Health",
    "Sleep Disorder",
    "Knee/Foot",
    "Neurologic",
    "Other",
]

EVENT_TYPES = [
    "Acoustic Trauma",
    "Blast/TBI",
    "Fall/Impact Injury",
    "Repetitive Overuse",
    "Toxic Exposure/Smoke",
    "Combat Stressor",
    "Medication Effect",
    "Chronic Pain Sequelae",
    "Other",
]

YES_NO_PARTIAL = ["Yes", "Partial", "No"]
SUPPORT_LEVEL = ["Strong", "Moderate", "Weak", "None"]
BIOLOGIC_LEVEL = ["Clear", "Plausible", "Unclear"]
IMAGING_LEVEL = ["Supportive", "Neutral/Not Needed", "Non-supportive"]
ALT_CAUSE_LEVEL = ["None", "Possible", "Strong"]
TREATMENT_GAP = ["None", "Explained", "Unexplained", "Long/Unexplained"]
ONSET_TIMING = ["During service", "Shortly after service", "Delayed"]
EVIDENCE_INCLUDE = ["Yes", "No"]
EVIDENCE_TYPE = [
    "STR",
    "VA Record",
    "Private Record",
    "Imaging",
    "Lay Statement",
    "C&P Exam",
    "Pharmacy",
    "Employment",
    "Literature",
    "Other",
]
EVIDENCE_STANCE = ["Supports", "Against", "Neutral"]

SCORE_MAP = {
    "STR|Yes": 2,
    "STR|Partial": 1,
    "STR|No": 0,
    "Continuity|Strong": 2,
    "Continuity|Moderate": 1,
    "Continuity|Weak": 0,
    "Continuity|None": 0,
    "Imaging|Supportive": 1,
    "Imaging|Neutral/Not Needed": 0,
    "Imaging|Non-supportive": -1,
    "Diagnosis|Strong": 1,
    "Diagnosis|Moderate": 0,
    "Diagnosis|Weak": -1,
    "Diagnosis|None": -1,
    "Biologic|Clear": 2,
    "Biologic|Plausible": 1,
    "Biologic|Unclear": -1,
    "Alt|None": 3,
    "Alt|Possible": 0,
    "Alt|Strong": -3,
    "Gap|None": 0,
    "Gap|Explained": -1,
    "Gap|Unexplained": -2,
    "Gap|Long/Unexplained": -2,
    "Functional|Strong": 1,
    "Functional|Moderate": 1,
    "Functional|Weak": 0,
    "Functional|None": 0,
    "Lay|Strong": 1,
    "Lay|Moderate": 0,
    "Lay|Weak": 0,
    "Lay|None": 0,
    "DirectEvent|Yes": 2,
    "DirectEvent|Partial": 1,
    "DirectEvent|No": 0,
    "SecondaryPrimary|Yes": 2,
    "SecondaryPrimary|Partial": 1,
    "SecondaryPrimary|No": 0,
    "AggravationParts|Complete": 3,
    "AggravationParts|Partial": 1,
    "AggravationParts|Missing": 0,
}

THRESHOLD_STRONG = 12
THRESHOLD_MODERATE = 7

BVA_LIBRARY = [
    {
        "condition_family": "Tinnitus/Hearing",
        "event_type": "Acoustic Trauma",
        "theory_type": "Direct Service Connection",
        "favorable_factors": "Noise exposure documented; credible lay report; no better post-service cause",
        "negative_factors": "Normal separation audiogram; delayed formal diagnosis",
        "key_reasoning_pattern": "Tinnitus may be present despite normal audiometry; weigh lay continuity and exposure context",
        "what_to_emphasize": "MOS/noise intensity, contemporaneous symptoms, credible continuity",
        "what_to_address": "Normal testing does not rule out tinnitus; explain why post-service noise is less persuasive",
        "common_failure_points": "Ignoring normal exit testing without explanation",
        "best_framing": "At least as likely as not related to military acoustic trauma when exposure and symptom history are coherent.",
    },
    {
        "condition_family": "Migraine/Headache",
        "event_type": "Blast/TBI",
        "theory_type": "Secondary Causation",
        "favorable_factors": "TBI service connected; headaches began or worsened after TBI; neurology confirmation",
        "negative_factors": "Pre-service headaches; stress or sleep deprivation as alternatives",
        "key_reasoning_pattern": "Explain post-traumatic headache mechanisms and why TBI better explains chronic pattern than nonspecific factors",
        "what_to_emphasize": "Temporal sequence, TBI severity, neurologic features, treatment history",
        "what_to_address": "Pre-service headache history and non-service triggers",
        "common_failure_points": "Failing to distinguish causation from aggravation",
        "best_framing": "At least as likely as not proximately due to service-connected TBI based on mechanism, timing, and course.",
    },
    {
        "condition_family": "Respiratory/Asthma",
        "event_type": "Toxic Exposure/Smoke",
        "theory_type": "Aggravation",
        "favorable_factors": "Baseline mild asthma, increased medication needs after exposure, persistent worsening",
        "negative_factors": "Smoking history; seasonal triggers; treatment gaps",
        "key_reasoning_pattern": "Identify baseline, show sustained worsening, and explain why course exceeds expected natural progression",
        "what_to_emphasize": "Baseline before service, documented increased frequency/severity, escalation of treatment",
        "what_to_address": "Smoking and other irritants must be acknowledged and weighed",
        "common_failure_points": "Using aggravation language without baseline discussion",
        "best_framing": "At least as likely as not aggravated beyond natural progression by service exposures when sustained worsening is documented.",
    },
]
