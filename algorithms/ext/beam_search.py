import random
from utils.cost import  heuristic

def beam_search(goal, beam_width=5, max_steps=500):
    """
    Beam Search cho bài toán N quân xe (hoặc N-queens).
    Trả về dict {"steps": steps, "generated": gen, "expanded": exp}
    """

    N = len(goal)
    steps = []
    gen = 0   # số trạng thái sinh ra
    exp = 0   # số trạng thái mở rộng

    # ------------------------------
    # Hàm sinh trạng thái ban đầu ngẫu nhiên
    # ------------------------------
    def random_start():
        return [(r, random.randint(0, N - 1)) for r in range(N)]

    # ------------------------------
    # Hàm sinh lân cận
    # ------------------------------
    def neighbors(state):
        for r in range(N):
            c_now = state[r][1]
            for c in range(N):
                if c != c_now:
                    new_state = state[:]
                    new_state[r] = (r, c)
                    yield new_state

    # ------------------------------
    # Khởi tạo
    # ------------------------------
    frontier = [random_start()]
    gen += len(frontier)

    # ------------------------------
    # Vòng lặp chính
    # ------------------------------
    for step in range(max_steps):
        # Đánh giá các trạng thái hiện có
        scored = [(s, heuristic(s, goal)) for s in frontier]
        scored.sort(key=lambda x: x[1])
        best, best_h = scored[0]
        steps.append((best[:], best_h))
        exp += len(frontier)

        # Nếu đã đạt mục tiêu
        if best == goal:
            break

        # Sinh tất cả lân cận
        all_candidates = []
        for s in frontier:
            for n in neighbors(s):
                all_candidates.append(n)
        gen += len(all_candidates)

        # Tính heuristic cho tất cả
        scored = [(s, heuristic(s, goal)) for s in all_candidates]
        scored.sort(key=lambda x: x[1])

        # Giữ lại beam_width tốt nhất
        frontier = [s for s, _ in scored[:beam_width]]

        # Nếu hết ứng viên thì dừng
        if not frontier:
            break

    # ------------------------------
    # Kết quả
    # ------------------------------
    return {
        "steps": steps,
        "generated": gen,
        "expanded": exp
    }
