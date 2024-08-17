import dataclasses


@dataclasses.dataclass
class Paper:
    authors: list[str] | None = None
    year: int | None = None
    month: int | None = None
    title: str | None = None
    journal: str | None = None
    abstract: str | None = None
    doi: str | None = None
    citations: int | None = None
