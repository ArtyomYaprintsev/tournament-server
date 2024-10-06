from typing import Self, TypeVar
from uuid import UUID, uuid4


T = TypeVar("T")


class Team:
    uuid: UUID
    name: str

    def __init__(self, name: str, uuid: UUID | None = None) -> None:
        self.uuid = uuid or uuid4()
        self.name = name

    def __str__(self) -> str:
        return f"<Team: {self.uuid.hex[:8]}|{self.name}>"

    def __repr__(self) -> str:
        return str(self)


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


def get_each_even(data: list[T]) -> list[T]:
    return [item for index, item in enumerate(data) if index % 2 == 0]


def get_each_odd(data: list[T]) -> list[T]:
    return [item for index, item in enumerate(data) if index % 2 == 1]


def generate_bracket(
    teams: list[Team],
    bracket: list[Match] | None = None,
    next_match: Match | None = None,
):
    teams_count = len(teams)

    if teams_count < 1:
        raise ValueError("Teams count should be greater than 0")

    if teams_count == 1:
        raise ValueError("Can not to generate bracket with only one team")

    if bracket is None:
        bracket = []

    _next_match = Match(next_match=next_match)
    bracket.append(_next_match)

    if teams_count == 2:
        team1, team2 = teams

        _next_match.team1 = team1
        _next_match.team2 = team2

        return bracket

    if teams_count == 3:
        team1, team2, team3 = teams

        _next_match.team1 = team1

        prev_match = Match(next_match=_next_match)
        prev_match.team1 = team2
        prev_match.team2 = team3

        bracket.append(prev_match)
        return bracket

    # left part
    generate_bracket(get_each_even(teams), bracket, _next_match)

    # Right part
    generate_bracket(get_each_odd(teams), bracket, _next_match)

    return bracket


if __name__ == "__main__":
    count = 11

    teams = [Team(f"name-{index}") for index in range(count)]

    bracket = generate_bracket(teams, [])
    print(bracket, len(bracket))
