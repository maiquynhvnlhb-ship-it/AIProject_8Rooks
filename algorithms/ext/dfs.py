# algorithms/ext/dfs.py
from __future__ import annotations

from typing import List, Tuple, Dict

Coord = Tuple[int, int]          # (row, col)
State = List[Coord]
DFSResult = Dict[str, object]
N = 8  # bàn cờ 8x8


def _is_column_free(partial: State, col: int) -> bool:
    """True nếu cột `col` chưa bị chiếm trong trạng thái `partial`."""
    for _, c in partial:
        if c == col:
            return False
    return True


def dfs(goal_columns: List[int]) -> DFSResult:
    """
    DFS cho bài toán 8 Rooks
    """
    stack: List[State] = [[]]
    steps: List[State] = []
    generated = 0
    expanded = 0

    while stack:
        state = stack.pop()

        if state:
            steps.append(state[:])

        # đích: đủ 8 quân và khớp cột mục tiêu
        if len(state) == N and [c for _, c in state] == goal_columns:
            return {"steps": steps, "generated": generated, "expanded": expanded}

        expanded += 1
        row = len(state)

        if row < N:
            # duyệt ngược 7..0 để hành vi DFS giống bản gốc
            for col in range(N - 1, -1, -1):
                if _is_column_free(state, col):
                    stack.append(state + [(row, col)])
                    generated += 1

    return {"steps": steps, "generated": generated, "expanded": expanded}
