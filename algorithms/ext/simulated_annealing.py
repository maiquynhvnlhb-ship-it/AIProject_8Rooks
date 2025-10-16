import math
import random
from typing import List, Tuple, Dict
# =====================================

#  HÀM HEURISTIC
def heuristic(state: List[Tuple[int, int]], goal: List[Tuple[int, int]]) -> int:
    """
    Heuristic = tổng số quân đặt sai vị trí so với goal.
    """
    cost = 0
    for (r, c_goal) in goal:
        # nếu hàng này chưa có quân hoặc cột sai
        found = [c for (rr, c) in state if rr == r]
        if not found or found[0] != c_goal:
            cost += 1
    return cost

#  KHỞI TẠO NGẪU NHIÊN
def random_start() -> List[Tuple[int, int]]:
    """Sinh trạng thái ban đầu ngẫu nhiên: mỗi hàng 1 quân ở cột ngẫu nhiên."""
    return [(r, random.randint(0, 7)) for r in range(8)]


#  SIMULATED ANNEALING (TÔI LUYỆN MÔ PHỎNG)
def simulated_annealing(goal: List[Tuple[int, int]],
                        T0: float = 10000,
                        alpha: float = 0.95,
                        Tmin: float = 1e-3,
                        max_steps: int = 10000) -> Dict:

    # --- Khởi tạo ---
    current = random_start()
    h_curr = heuristic(current, goal)
    steps = [(current[:], h_curr)]
    gen = 0
    exp = 0

    T = T0
    k = 0

    # --- Vòng lặp chính ---
    while T > Tmin and k < max_steps:
        exp += 1

        # Chọn hàng ngẫu nhiên và tạo neighbor
        r = random.randint(0, 7)
        c_now = current[r][1]
        c_new = random.choice([c for c in range(8) if c != c_now])

        new_state = current[:]
        new_state[r] = (r, c_new)
        gen += 1

        # Tính heuristic mới
        h_new = heuristic(new_state, goal)
        delta = h_new - h_curr

        # Quy tắc chấp nhận: chấp nhận nếu tốt hơn
        #  hoặc xấu hơn nhưng vẫn chấp nhận theo xác suất e^(-Δ/T)
        if delta < 0 or random.random() < math.exp(-delta / T):
            current, h_curr = new_state, h_new
            steps.append((current[:], h_curr))

        # Kiểm tra mục tiêu
        if [c for _, c in current] == [c for _, c in goal]:
            break

        # Giảm nhiệt độ
        T *= alpha
        k += 1

    return {"steps": steps, "generated": gen, "expanded": exp}
