from typing import Any, Self
from uuid import UUID, uuid4



class Team:
    uuid: UUID
    name: str

    def __init__(self, name: str, uuid: UUID | None = None) -> None:
        self.uuid = uuid or uuid4()
        self.name = name


class Match:
    team1: Team | None = None
    team2: Team | None = None

    uuid: UUID
    next_match: Self | None = None

    def __init__(self, next_match: Self | None = None) -> None:
        self.uuid = uuid4()
        self.next_match = next_match

    def __str__(self) -> str:
        return f"<Match: {self.uuid.hex[:8]}>"

    def __repr__(self) -> str:
        return f"{self} -> {self.next_match or '<NONE>'}"



def generate_bracket(
    teams_count: int,
    bracket: list[Match],
    next_match: Match | None = None,
):
    if teams_count < 1:
        raise ValueError("Teams count should be greater than 0")

    if teams_count == 1:
        raise ValueError("Can not to generate bracket with only one team")

    _next_match = Match(next_match=next_match)
    bracket.append(_next_match)

    if teams_count == 2:
        return bracket

    if teams_count == 3:
        bracket.append(Match(next_match=_next_match))
        return bracket

    # left part
    generate_bracket(teams_count // 2 + teams_count % 2, bracket, _next_match)

    # Right part
    generate_bracket(teams_count // 2, bracket, _next_match)

    return bracket


if __name__ == "__main__":
    count = 9
    bracket = generate_bracket(count, [])
    print(bracket, len(bracket))
