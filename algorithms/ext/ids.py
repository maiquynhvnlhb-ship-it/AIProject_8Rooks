# algorithms/ext/ids.py
from typing import List, Tuple, Dict, Any
from utils.cost import _goal_to_cols

State = List[Tuple[int, int]]  # [(row, col), ...]


def ids(goal: List[int] | State, max_limit: int | None = None) -> Dict[str, Any]:
    """
    IDS (Iterative Deepening Search)
    """
    cols_goal = _goal_to_cols(goal)
    N = len(cols_goal)
    if max_limit is None:
        max_limit = N

    steps: List[Tuple[State, int]] = []
    gen = 0  # số nút sinh ra
    exp = 0  # số nút mở rộng

    def check(vt: State, col: int) -> bool:
        """Hợp lệ nếu chưa có quân nào cùng cột."""
        for _, c in vt:
            if c == col:
                return False
        return True

    def dls_once(limit: int) -> bool:
        """Chạy DLS 1 lần với giới hạn 'limit'. Trả về True nếu tìm thấy goal."""
        nonlocal gen, exp, steps
        found = False

        def rec(vt: State, depth: int) -> bool:
            nonlocal gen, exp, found, steps
            if vt:
                steps.append((vt[:], depth))  # lưu bước (state, depth)

            # kiểm tra đích
            if len(vt) == N and [c for _, c in vt] == cols_goal:
                found = True
                return True

            if depth == limit:
                return False

            exp += 1  # mở rộng node hiện tại
            row = len(vt)
            if row < N:
                for c in range(N):
                    if check(vt, c):
                        gen += 1
                        if rec(vt + [(row, c)], depth + 1):
                            return True
            return False

        rec([], 0)
        return found

    # Lặp tăng giới hạn độ sâu từ 0..max_limit
    for L in range(0, max_limit + 1):
        if dls_once(L):
            break

    return {"steps": steps, "generated": gen, "expanded": exp}
