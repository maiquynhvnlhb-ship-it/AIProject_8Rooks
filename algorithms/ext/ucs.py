import heapq
from utils.cost import cost_place_rook, _goal_to_cols

def ucs(goal):
    """
    Uniform Cost Search (UCS)
    """
    cols_goal = _goal_to_cols(goal)

    pq = []           # (cost, tie, state)
    steps = []        # (state, cost)
    gen = 0
    exp = 0
    tie = 0

    start = []
    heapq.heappush(pq, (0, tie, start)); tie += 1

    while pq:
        cost, _, vt = heapq.heappop(pq)

        if vt:
            steps.append((vt[:], cost))

        # Đạt mục tiêu: đủ 8 hàng và cột khớp với goal
        if len(vt) == 8 and [c for r, c in vt] == cols_goal:
            return {"steps": steps, "generated": gen, "expanded": exp}

        exp += 1
        row = len(vt)
        if row < 8:
            for c in range(8):
                new_state = vt + [(row, c)]
                g = cost_place_rook(vt, c, cols_goal)  # chi phí từng bước (0 hoặc 1 nếu sai)
                new_cost = cost + g
                heapq.heappush(pq, (new_cost, tie, new_state))
                tie += 1
                gen += 1

    return {"steps": steps, "generated": gen, "expanded": exp}
