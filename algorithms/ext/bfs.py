# algorithms/ext/bfs.py
from __future__ import annotations

from collections import deque
from typing import Deque, Dict, List, Tuple

Coord = Tuple[int, int]   # (row, col)
State = List[Coord]       # danh sách quân đã đặt theo thứ tự hàng
BFSResult = Dict[str, object]  # {"steps": List[State], "generated": int, "expanded": int}

N = 8  # kích thước bàn cờ 8x8

def _is_column_free(partial: State, col: int) -> bool:
    """Trả về True nếu cột `col` chưa có quân trong trạng thái `partial`."""
    for _, c in partial:
        if c == col:
            return False
    return True


def bfs(goal_columns: List[int]) -> BFSResult:
    """
    BFS cho bài toán 8 Rooks .
    """
    queue: Deque[State] = deque([[]])
    steps: List[State] = []
    generated = 0
    expanded = 0

    while queue:
        state = queue.popleft()

        # Lưu lại bước cho GUI (bỏ qua trạng thái rỗng để đỡ nhiễu)
        if state:
            steps.append(state[:])

        # Kiểm tra đích: đủ 8 hàng và cột đúng mục tiêu
        if len(state) == N and [c for _, c in state] == goal_columns:
            return {"steps": steps, "generated": generated, "expanded": expanded}

        expanded += 1
        row = len(state)

        # Sinh các trạng thái con ở hàng hiện tại
        if row < N:
            for col in range(N):
                if _is_column_free(state, col):
                    queue.append(state + [(row, col)])
                    generated += 1

    # Không tìm thấy (trường hợp không khớp goal yêu cầu)
    return {"steps": steps, "generated": generated, "expanded": expanded}
