
from typing import List, Tuple, Dict, Any, Optional, Protocol

State = List[Tuple[int, int]]  # list of (row, col)

class Solver(Protocol):
    def solve(self, goal: List[int]) -> Tuple[List[State], Dict[str, Any], Optional[State]]:
        ...

# A tiny helper to shape meta info for each algorithm
def meta(name: str,
         group: str = "Uninformed",
         attributes: str = "",
         description: str = "") -> Dict[str, str]:
    return {
        "name": name,
        "group": group,
        "attributes": attributes,
        "description": description,
    }
