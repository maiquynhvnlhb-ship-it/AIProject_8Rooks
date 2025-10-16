# ============================================================
#  AND–OR Search (phiên bản không sử dụng -1)
#  ------------------------------------------------------------
#  - Mỗi state là list các vị trí [(row, col), ...]
#  - Mỗi OR node: chọn hành động (đặt thêm 1 quân)
#  - Mỗi AND node: phải thỏa mãn tất cả trạng thái con
#  - Kết quả trả về {"steps": steps, "generated": gen, "expanded": exp}
# ============================================================

from typing import List, Tuple, Optional, Any


def _goal_to_cols(goal: List[Any]) -> List[int]:
    """Nhận goal là list[int] hoặc list[(row,col)], trả về list[int] theo thứ tự hàng."""
    if not goal:
        return list(range(8))
    g0 = goal[0]
    if isinstance(g0, (list, tuple)):
        N = len(goal)
        cols = [None] * N
        for r, c in goal:
            cols[r] = c
        return cols
    return goal


# ---------- Kiểm tra trạng thái đạt mục tiêu ----------
def goal_test(state: List[Tuple[int, int]], goal_cols: List[int]) -> bool:
    """Đúng nếu tất cả hàng đã được đặt và cột trùng với goal."""
    if len(state) != len(goal_cols):
        return False
    cols_now = [c for _, c in sorted(state, key=lambda x: x[0])]
    return cols_now == goal_cols


# ---------- Sinh các hành động hợp lệ ----------
def actions(state: List[Tuple[int, int]], N: int) -> List[int]:
    """Trả về các cột có thể đặt cho hàng tiếp theo."""
    used_cols = {c for _, c in state}
    return [c for c in range(N) if c not in used_cols]


# ---------- Sinh trạng thái mới ----------
def result(state: List[Tuple[int, int]], row: int, col: int) -> List[Tuple[int, int]]:
    """Thêm quân mới vào danh sách state."""
    return state + [(row, col)]


# ---------- AND–OR SEARCH ----------
def and_or_search(goal: List[Any]) -> dict:
    goal_cols = _goal_to_cols(goal)
    N = len(goal_cols)

    gen = 0
    exp = 0
    steps: List[List[Tuple[int, int]]] = []  # lưu toàn bộ trạng thái trung gian

    # ------------------------------------------------------------
    # Ghi lại mỗi state duy nhất để GUI hiển thị
    # ------------------------------------------------------------
    def record_state(state: List[Tuple[int, int]]):
        if state and state not in steps:
            steps.append(state[:])

    # ------------------------------------------------------------
    # OR node: chọn 1 hành động (một nước đi mới)
    # ------------------------------------------------------------
    def OR_Search(state: List[Tuple[int, int]], path: List[List[Tuple[int, int]]]) -> Optional[list]:
        nonlocal gen, exp
        record_state(state)

        if goal_test(state, goal_cols):
            return []  # đạt mục tiêu

        if state in path:
            return None  # tránh vòng lặp

        row = len(state)  # hàng hiện tại là hàng kế tiếp chưa đặt
        if row >= N:
            return None  # không còn hàng hợp lệ

        exp += 1
        for a in actions(state, N):
            gen += 1
            new_state = result(state, row, a)
            plan = AND_Search([new_state], path + [state])
            if plan is not None:
                return [('move', (row, a), plan)]
        return None

    # ------------------------------------------------------------
    # AND node: phải thỏa mãn tất cả trạng thái con
    # ------------------------------------------------------------
    def AND_Search(states: List[List[Tuple[int, int]]], path: List[List[Tuple[int, int]]]) -> Optional[list]:
        nonlocal gen, exp
        exp += 1
        all_plans = []
        for s in states:
            plan = OR_Search(s, path)
            if plan is None:
                return None
            all_plans.append(plan)
        return all_plans

    # ------------------------------------------------------------
    # Khởi tạo từ state rỗng (chưa có quân nào)
    # ------------------------------------------------------------
    init_state: List[Tuple[int, int]] = []
    plan = OR_Search(init_state, [])

    # ------------------------------------------------------------
    # Trả kết quả
    # ------------------------------------------------------------
    return {"steps": steps, "generated": gen, "expanded": exp}
