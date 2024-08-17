def authors(response: dict) -> list[str] | None:
    try:
        return [author.name for author in response["authors"]]
    except Exception:
        return None


def year(response: dict) -> int | None:
    try:
        return response["updated"].year
    except Exception:
        return None


def month(response: dict) -> int | None:
    try:
        return response["updated"].month
    except Exception:
        return None


def title(response: dict) -> str | None:
    try:
        return response["title"]
    except Exception:
        return None


def journal(response: dict) -> str | None:
    try:
        return "ArXiv"
    except Exception:
        return None


def abstract(response: dict) -> str | None:
    try:
        abstract = response["summary"]
    except Exception:
        return None

    # Remove \n
    abstract = abstract.replace("\n", " ")

    # Check Length due to API Limitations
    abstract = abstract if len(abstract) <= 2000 else ""

    return abstract


def doi(response: dict) -> str | None:
    try:
        return response.get("doi").lower()
    except Exception:
        return None


def citations(response: dict) -> int | None:
    return None
