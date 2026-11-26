"""Typed access to `upstreams.json`, the record of each upstream's Pin and Sync log.

See ADR-0006. The JSON is validated and shaped once here, so callers never touch
`Any` and a malformed record fails with a message instead of a KeyError.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Literal, NotRequired, TypedDict, cast, get_args

RECORD_PATH = "upstreams.json"

FULL_SHA = re.compile(r"[0-9a-f]{40}")
DATE = re.compile(r"\d{4}-\d{2}-\d{2}")

OutcomeState = Literal["ported", "no-change", "diverged", "owed", "unrecorded"]
Decision = Literal["adopted", "declined", "owed"]

OUTCOME_STATES: frozenset[str] = frozenset(get_args(OutcomeState))
DECISIONS: frozenset[str] = frozenset(get_args(Decision))


class ForkPoint(TypedDict):
    sha: str
    version: str


class Pin(TypedDict):
    sha: str
    version: str
    committed: str
    reviewed: str


class Owed(TypedDict):
    state: Literal["owed"]
    ticket: str


class Candidate(TypedDict):
    name: str
    decision: Decision
    ticket: NotRequired[str]


# `from` is a keyword, so this one needs the functional form.
LogEntry = TypedDict(
    "LogEntry",
    {
        "date": str,
        "from": str | None,
        "to": str,
        "pr": str,
        "backfilled": NotRequired[bool],
        "note": NotRequired[str],
        "outcomes": dict[str, OutcomeState | Owed],
        "candidates": list[Candidate],
    },
)


class Upstream(TypedDict):
    name: str
    repository: str
    fork_point: ForkPoint
    pin: Pin
    log: list[LogEntry]


class Record(TypedDict):
    upstreams: list[Upstream]


class RecordError(ValueError):
    """The record does not have the shape ADR-0006 defines."""


def outcome_state(value: OutcomeState | Owed) -> OutcomeState:
    return value if isinstance(value, str) else value["state"]


def load_record(root: Path) -> Record:
    path = root / RECORD_PATH
    try:
        raw: Any = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise RecordError(f"{RECORD_PATH} is missing") from exc
    except json.JSONDecodeError as exc:
        raise RecordError(f"{RECORD_PATH} is not valid JSON: {exc}") from exc
    problems = shape_problems(raw)
    if problems:
        raise RecordError("\n".join(problems))
    return cast(Record, raw)


def shape_problems(raw: Any) -> list[str]:
    """Every way `raw` departs from the record shape, as readable messages."""
    out: list[str] = []
    if not isinstance(raw, dict) or not isinstance(raw.get("upstreams"), list):
        return ['top level must be an object with an "upstreams" list']
    names: set[str] = set()
    for i, upstream in enumerate(cast(list[Any], raw["upstreams"])):
        where = f"upstreams[{i}]"
        if not isinstance(upstream, dict):
            out.append(f"{where} must be an object")
            continue
        up = cast(dict[str, Any], upstream)
        name = up.get("name")
        if not isinstance(name, str) or not name:
            out.append(f"{where}.name must be a non-empty string")
        else:
            where = name
            if name in names:
                out.append(f"{where}: duplicate upstream name")
            names.add(name)
        if not isinstance(up.get("repository"), str):
            out.append(f"{where}.repository must be a string URL")
        out += _object_problems(f"{where}.fork_point", up.get("fork_point"), ("sha", "version"))
        out += _object_problems(
            f"{where}.pin", up.get("pin"), ("sha", "version", "committed", "reviewed")
        )
        log = up.get("log")
        if not isinstance(log, list) or not log:
            out.append(f"{where}.log must be a non-empty list")
            continue
        for j, entry in enumerate(cast(list[Any], log)):
            out += _entry_problems(f"{where}.log[{j}]", entry)
    return out


def _object_problems(where: str, value: Any, keys: tuple[str, ...]) -> list[str]:
    if not isinstance(value, dict):
        return [f"{where} must be an object"]
    obj = cast(dict[str, Any], value)
    out = [f"{where}.{k} must be a string" for k in keys if not isinstance(obj.get(k), str)]
    if isinstance(obj.get("sha"), str) and not FULL_SHA.fullmatch(obj["sha"]):
        out.append(f"{where}.sha must be a full 40-character SHA")
    out += [
        f"{where}.{k} must be a YYYY-MM-DD date"
        for k in ("committed", "reviewed")
        if k in keys and isinstance(obj.get(k), str) and not DATE.fullmatch(obj[k])
    ]
    return out


def _entry_problems(where: str, value: Any) -> list[str]:
    if not isinstance(value, dict):
        return [f"{where} must be an object"]
    entry = cast(dict[str, Any], value)
    out: list[str] = []
    if not isinstance(entry.get("date"), str) or not DATE.fullmatch(entry["date"]):
        out.append(f"{where}.date must be a YYYY-MM-DD date")
    start = entry.get("from")
    if start is not None and not (isinstance(start, str) and FULL_SHA.fullmatch(start)):
        out.append(f"{where}.from must be a full SHA or null")
    if not (isinstance(entry.get("to"), str) and FULL_SHA.fullmatch(entry["to"])):
        out.append(f"{where}.to must be a full SHA")
    if not isinstance(entry.get("pr"), str):
        out.append(f"{where}.pr must be a string URL")
    backfilled = entry.get("backfilled", False)
    if not isinstance(backfilled, bool):
        out.append(f"{where}.backfilled must be a boolean")
    if "note" in entry and not isinstance(entry["note"], str):
        out.append(f"{where}.note must be a string")

    outcomes = entry.get("outcomes")
    if not isinstance(outcomes, dict):
        out.append(f"{where}.outcomes must be an object keyed by repo path")
    else:
        for path, outcome in cast(dict[str, Any], outcomes).items():
            out += _outcome_problems(f"{where}.outcomes[{path!r}]", outcome, backfilled is True)

    candidates = entry.get("candidates")
    if not isinstance(candidates, list):
        out.append(f"{where}.candidates must be a list")
    else:
        for k, candidate in enumerate(cast(list[Any], candidates)):
            out += _candidate_problems(f"{where}.candidates[{k}]", candidate)
    return out


def _outcome_problems(where: str, value: Any, backfilled: bool) -> list[str]:
    if isinstance(value, dict):
        owed = cast(dict[str, Any], value)
        if owed.get("state") != "owed" or not isinstance(owed.get("ticket"), str):
            return [f'{where} as an object must be {{"state": "owed", "ticket": "<ref>"}}']
        return []
    if value not in OUTCOME_STATES:
        return [f"{where} must be one of {', '.join(sorted(OUTCOME_STATES))}"]
    if value == "owed":
        return [f'{where}: owed needs a ticket, as {{"state": "owed", "ticket": "<ref>"}}']
    if value == "unrecorded" and not backfilled:
        return [f"{where}: unrecorded is allowed only in a backfilled entry"]
    return []


def _candidate_problems(where: str, value: Any) -> list[str]:
    if not isinstance(value, dict):
        return [f"{where} must be an object"]
    candidate = cast(dict[str, Any], value)
    out: list[str] = []
    if not isinstance(candidate.get("name"), str):
        out.append(f"{where}.name must be a string")
    decision = candidate.get("decision")
    if decision not in DECISIONS:
        out.append(f"{where}.decision must be one of {', '.join(sorted(DECISIONS))}")
    if decision == "owed" and not isinstance(candidate.get("ticket"), str):
        out.append(f"{where}: an owed candidate needs a ticket")
    return out
