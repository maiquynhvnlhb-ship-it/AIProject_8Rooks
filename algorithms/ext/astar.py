from __future__ import annotations

import heapq
from typing import List, Tuple, Dict, Iterable

from utils.cost import heuristic as h_cost, _goal_to_cols

Coord = Tuple[int, int]          # (row, col)
State = List[Coord]              # danh sách các quân đã đặt theo thứ tự hàng
AStarResult = Dict[str, object]  # {"steps": ..., "generated": int, "expanded": int}


def cost_place_rook2(state: Iterable[Coord], goal: Iterable[int | Coord]) -> int:
    cols_goal = _goal_to_cols(goal)
    cost = 0
    for r, c in state:
        if cols_goal[r] != c:
            cost += 1
    return cost


def astar(goal: Iterable[int | Coord]) -> AStarResult:
    """
    A*
    """
    cols_goal = _goal_to_cols(goal)
    # Hàng đợi ưu tiên: (f, tie, state)
    pq: List[Tuple[float, int, State]] = []
    steps: List[Tuple[State, float]] = []  # lưu (state, f) cho GUI
    generated = 0
    expanded = 0
    tie = 0

    # Trạng thái khởi đầu: chưa đặt quân nào
    start: State = []
    heapq.heappush(pq, (0.0, tie, start))
    tie += 1

    while pq:
        f, _, current = heapq.heappop(pq)

        # Lưu bước (bỏ qua trạng thái rỗng để GUI đỡ nhiễu, giống code gốc)
        if current:
            steps.append((current[:], f))

        # Kiểm tra mục tiêu: đã đủ 8 hàng và đúng cột mục tiêu
        if len(current) == 8 and [c for _, c in current] == cols_goal:
            return {"steps": steps, "generated": generated, "expanded": expanded}

        expanded += 1
        row = len(current)

        # Sinh các trạng thái con: đặt quân ở hàng 'row' vào mọi cột [0..7]
        if row < 8:
            for col in range(8):
                child: State = current + [(row, col)]

                g = cost_place_rook2(child, goal)
                h = h_cost(child, cols_goal)
                f_child = g + h

                heapq.heappush(pq, (f_child, tie, child))
                tie += 1
                generated += 1

    # Nếu không tìm thấy (trường hợp bất thường)
    return {"steps": steps, "generated": generated, "expanded": expanded}
