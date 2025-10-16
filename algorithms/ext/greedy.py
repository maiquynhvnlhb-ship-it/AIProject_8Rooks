# algorithms/ext/greedy.py
import heapq
from typing import List, Tuple, Dict, Any

from utils.cost import heuristic, _goal_to_cols

State = List[Tuple[int, int]]  # [(row, col), ...]


def greedy(goal: List[int] | State) -> Dict[str, Any]:
    """
    Greedy Best-First Search
    """
    cols_goal = _goal_to_cols(goal)
    N = len(cols_goal)

    # Hàng đợi ưu tiên theo h(n) (Greedy)
    pq: List[Tuple[float, int, State]] = []
    steps: List[Tuple[State, float]] = []
    gen = 0
    exp = 0
    tie = 0  # tiebreaker tránh so sánh list khi h bằng nhau

    # Trạng thái khởi đầu (chưa đặt quân nào)
    start: State = []
    heapq.heappush(pq, (heuristic(start, cols_goal), tie, start))
    tie += 1

    while pq:
        h_cur, _, vt = heapq.heappop(pq)

        # Lưu bước cho GUI (bỏ trạng thái rỗng)
        if vt:
            steps.append((vt[:], h_cur))

        # Kiểm tra đích
        if len(vt) == N and [c for _, c in vt] == cols_goal:
            return {"steps": steps, "generated": gen, "expanded": exp}

        exp += 1
        row = len(vt)
        if row >= N:
            continue

        # Sinh các láng giềng: đặt 1 quân tại hàng 'row' ở mọi cột
        for c in range(N):
            child: State = vt + [(row, c)]
            h_new = heuristic(child, cols_goal)  # Greedy: chỉ xếp theo h
            heapq.heappush(pq, (h_new, tie, child))
            tie += 1
            gen += 1

    # Không tìm thấy nghiệm khớp tuyệt đối
    return {"steps": steps, "generated": gen, "expanded": exp}
