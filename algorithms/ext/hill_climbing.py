from typing import List, Tuple, Dict, Any
from utils.cost import heuristic, _goal_to_cols

State = List[Tuple[int, int]]  # [(row, col), ...]


def hill_climbing(goal: List[int] | State) -> Dict[str, Any]:
    """
    Hill Climbing
    """
    cols_goal = _goal_to_cols(goal)
    N = len(cols_goal)

    # Trạng thái khởi đầu: mỗi hàng đặt ở cột 0
    current: State = [(0,0),(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7)]
    h_curr: float = heuristic(current, cols_goal)

    steps: List[Tuple[State, float]] = [(current[:], h_curr)]
    gen = 0   # số trạng tháisinh ra
    exp = 0   # số lần mở rộng

    # Hàm kiểm tra đạt mục tiêu nhanh (khớp cột theo từng hàng)
    def is_goal(state: State) -> bool:
        return [c for _, c in state] == cols_goal

    improved = True
    while improved:
        # Nếu đã đạt goal hoặc h = 0 thì dừng
        if h_curr == 0 or is_goal(current):
            # đảm bảo ghi nhận bước cuối (h=0) nếu chưa có
            if steps[-1][1] != 0:
                steps.append((current[:], 0.0))
            break

        improved = False
        exp += 1
        neighbors: List[Tuple[float, State]] = []

        # Sinh tất cả láng giềng bằng cách di chuyển từng quân sang cột khác
        for r in range(N):
            c_now = current[r][1]
            for c in range(N):
                if c == c_now:
                    continue
                child = current[:]
                child[r] = (r, c)
                h_child = heuristic(child, cols_goal)
                neighbors.append((h_child, child))

        if not neighbors:
            break

        gen += len(neighbors)

        # Chọn láng giềng tốt nhất theo heuristic (nhỏ nhất)
        best_h, best_state = min(neighbors, key=lambda x: x[0])

        # Chỉ cập nhật nếu có cải thiện
        if best_h < h_curr:
            current, h_curr = best_state, best_h
            steps.append((current[:], h_curr))
            improved = True
        else:
            # không cải thiện -> kẹt tại cực trị cục bộ/điểm bằng phẳng
            break

    return {
        "steps": steps,
        "generated": gen,
        "expanded": exp
    }
