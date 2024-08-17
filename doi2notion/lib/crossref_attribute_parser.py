import re


def authors(response: dict) -> list[str] | None:
    try:
        return [
            author["given"] + " " + author["family"] for author in response["author"]
        ]
    except Exception:
        return None


def year(response: dict) -> int | None:
    try:
        return response["issued"]["date-parts"][0][0]
    except Exception:
        return None


def month(response: dict) -> int | None:
    try:
        return response["issued"]["date-parts"][0][1]
    except Exception:
        return None


def title(response: dict) -> str | None:
    try:
        return response["title"][0]
    except Exception:
        return None


def journal(response: dict) -> str | None:
    try:
        return response["container-title"][0]
    except Exception:
        return None


def abstract(response: dict) -> str | None:
    try:
        abstract = response["abstract"]
    except Exception:
        return None

    # Remove JATS-elements
    abstract = re.sub("<(|/)jats:p>|", "", abstract)

    # Check Length due to API Limitations
    abstract = abstract if len(abstract) <= 2000 else ""

    return abstract


def doi(response: dict) -> str | None:
    try:
        return response.get("DOI").lower()
    except Exception:
        return None


def citations(response: dict) -> int | None:
    return response.get("is-referenced-by-count")
