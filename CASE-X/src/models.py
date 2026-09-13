from dataclasses import dataclass


@dataclass
class Suspect:
    """A person connected to an investigation."""

    id: int
    name: str
    age: int
    occupation: str
    relationship_to_victim: str
    alibi: str
    score: float = 0.0


@dataclass
class Evidence:
    """Evidence linked to a case and optionally to a suspect."""

    id: int
    case_id: int
    evidence_type: str
    description: str
    reliability: int
    suspect_id: int | None = None
