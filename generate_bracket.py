"""The tournament bracket generation concept.

The `generate_bracket` function generates a tournament [single-elimination
bracket](https://en.wikipedia.org/wiki/Single-elimination_tournament) and fills
matches with the provided teams.

Note:
To generate the correct bracket, the function must receive an ordered list of
teams (e.g. by team rating or the number of team wins).

Algorithm:

The algorithm for generating the tournament bracket splits the received teams
into two separated lists with each even item and each odd one. These lists are
passes to the corresponding "part" of the bracket (for example, if the total
number of teams is 11, then 6 teams will be provided to the "left part" of the
bracket, and 5 teams to the "right part").
In this case, the algorithm generates bracket in which each team plays with
the closest team (the parameter for ordering the list of teams).

Bracket examples:

1. If the number of teams is 3:

    ```
    team2/team3 -> team1/TBD
    ```

2. If the number of teams is 4:

    ```
    team1/team3 -|
                 |-> TBD/TBD
    team2/team4 -|
    ```

3. If the number of teams is 9:

    ```
    team5/team8 -> team1/TBD ---|
                                |--> TBD/TBD -|
                   team3/team7 -|             | 
                                              |--> TBD/TBD
                   team2/team6 -|             |
                                |--> TBD/TBD -|
                   team4/team8 -|
    ```
"""

from typing import Self, TypeVar
from uuid import UUID, uuid4


T = TypeVar("T")


class Team:
    """Simple class that represents the `Team` model.
    
    Attrs:
        uuid (`UUID`): The UUID of the team.
        name (`str`): The name of the team.
    """

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
    """Simple class that represents the `Match` model.
    
    Attrs:
        uuid (`UUID`): The UUID of the match.
        next_match (`Match | None`): the next optional `Match` instance, None
            by default.
        team1 (`Team | None`): The first team of the match, None by default.
        team2 (`Team | None`): The second team of the match, None by default.
    """

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
    """Get list with an each even item."""
    return [item for index, item in enumerate(data) if index % 2 == 0]


def get_each_odd(data: list[T]) -> list[T]:
    """Get list with an each odd item."""
    return [item for index, item in enumerate(data) if index % 2 == 1]


def generate_bracket(
    teams: list[Team],
    bracket: list[Match] | None = None,
    next_match: Match | None = None,
):
    """Generate tournament bracket by teams list.

    Algorithm uses recursion to generate parts of the bracket.
    For an each iteration the algorithm:
    - creates new "core" `Match` instance;
    - by the number of the current `teams` items:
        - if equals to 2: fills `next_match` instance with current teams;
        - if equals to 3: creates additional `Match` with 2nd and 3rd teams
            and relates it with `next_match`, sets `next_match.team1` as
            the 1st received team.
        - otherwise: call `generate_bracket` with each even team and
            another call with each odd team.
    - returns the resulted bracket.

    Note:
        The algorithm concept described into this module docstring.

    Args:
        teams (`list[Team]`): the ordering by some parameter list of teams.
        bracket (`list[Match] | None`): the resulted set of `Match` instances.
        next_match (`Match | None`): optional next `Match` instance (required
            to generate related matches).

    Returns:
        The list of `Match` instances that represents the tournament bracket.        
    """
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
        # Fill `next_match` teams with current teams
        team1, team2 = teams

        _next_match.team1 = team1
        _next_match.team2 = team2

        return bracket

    if teams_count == 3:
        team1, team2, team3 = teams

        # 1st team of the current `teams` list is the strongest by some
        # parameter. So, provide it to the `next_match.team1` field.
        _next_match.team1 = team1

        # Create additional match between the 2nd and 3rd teams
        prev_match = Match(next_match=_next_match)
        prev_match.team1 = team2
        prev_match.team2 = team3

        bracket.append(prev_match)
        return bracket

    # left part
    generate_bracket(get_each_even(teams), bracket, _next_match)

    # right part
    generate_bracket(get_each_odd(teams), bracket, _next_match)

    return bracket


if __name__ == "__main__":
    count = 11

    teams = [Team(f"name-{index}") for index in range(count)]

    bracket = generate_bracket(teams, [])
    print(bracket, len(bracket))
