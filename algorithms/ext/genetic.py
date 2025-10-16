import random
from typing import List, Tuple, Dict, Any
from utils.cost import heuristic

State = List[Tuple[int, int]]  # [(row, col), ...]


def genetic_algorithm(
    goal: State,
    pop_size: int = 100,
    generations: int = 500,
    mutation_rate: float = 0.2
) -> Dict[str, Any]:
    """
    Genetic Algorithm
    """
    N = len(goal)
    steps: List[Tuple[State, float]] = []
    gen = 0  # số cá thể sinh ra
    exp = 0  # số thế hệ đã duyệt

    # -----------------------------
    # Các hàm hỗ trợ
    # -----------------------------
    def random_individual() -> State:
        """Tạo ngẫu nhiên 1 cá thể: mỗi hàng 1 cột."""
        return [(r, random.randint(0, N - 1)) for r in range(N)]

    def fitness(ind: State) -> float:
        """Đánh giá độ thích nghi (fitness) - giá trị càng nhỏ càng tốt."""
        return heuristic(ind, goal)

    def crossover(p1: State, p2: State) -> State:
        """Lai ghép hai cá thể (cắt ngẫu nhiên một điểm)."""
        cut = random.randint(1, N - 1)
        return p1[:cut] + p2[cut:]

    def mutate(ind: State) -> State:
        """Đột biến ngẫu nhiên: đổi cột 1 quân."""
        r = random.randint(0, N - 1)
        c_new = random.randint(0, N - 1)
        ind[r] = (r, c_new)
        return ind

    # -----------------------------
    # Khởi tạo quần thể ban đầu
    # -----------------------------
    population: List[State] = [random_individual() for _ in range(pop_size)]
    gen += pop_size

    # -----------------------------
    # Vòng lặp tiến hóa
    # -----------------------------
    for generation in range(generations):
        exp += 1  # mở rộng 1 thế hệ

        # Đánh giá fitness cho từng cá thể
        scored = [(ind, fitness(ind)) for ind in population]
        scored.sort(key=lambda x: x[1])  # sắp xếp tăng dần theo fitness
        best, best_fit = scored[0]

        # Ghi lại trạng thái tốt nhất trong thế hệ
        steps.append((best[:], best_fit))

        # Kiểm tra nghiệm đạt mục tiêu
        if best == goal:
            break

        # Chọn cha mẹ tốt nhất (elitism)
        parents = [ind for ind, _ in scored[: pop_size // 2]]

        # Lai ghép & đột biến tạo thế hệ mới
        children: List[State] = []
        while len(children) < pop_size:
            p1, p2 = random.sample(parents, 2)
            child = crossover(p1[:], p2[:])
            if random.random() < mutation_rate:
                child = mutate(child)
            children.append(child)
            gen += 1

        population = children

    # -----------------------------
    # Kết quả cuối cùng
    # -----------------------------
    return {
        "steps": steps,
        "generated": gen,
        "expanded": exp
    }
