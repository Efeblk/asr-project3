"""Project language rules (docs/project-requirements.md, slides L6/S9).

Only the rules a program can check live here. "Not a group member's mother tongue" cannot be
checked by code and must never be recorded in this repo; runs instead require an explicit
`eligibility_confirmed: true` declaration in the run config.
"""

from __future__ import annotations

ENGLISH_CODES = {"en", "eng"}


class IneligibleLanguageError(ValueError):
    pass


def base_language(code: str) -> str:
    """'pt-BR' -> 'pt', 'cmn_hans_cn' -> 'cmn'."""
    return code.replace("_", "-").split("-")[0].lower()


def check_language(code: str) -> None:
    if not code or not code.strip():
        raise IneligibleLanguageError("Empty language code.")
    if base_language(code) in ENGLISH_CODES:
        raise IneligibleLanguageError(
            f"Language '{code}' is English, which the project forbids (slide L6/S9)."
        )


def check_run_languages(languages: list[str], eligibility_confirmed: bool) -> None:
    for code in languages:
        check_language(code)
    if not eligibility_confirmed:
        raise IneligibleLanguageError(
            "Set `eligibility_confirmed: true` in the run config once the group has confirmed that "
            "none of these languages is a group member's mother tongue (do not record whose)."
        )
