def belief_state(goal):
    """
    Belief-State Search
    """
    N = len(goal)
    steps, gen, exp = [], 0, 0
    found = False

    # ------------------------------
    # Belief ban đầu: 1 tập gồm 2 trạng thái
    # ------------------------------
    belief = [[((0, 0),), ((0, 1),)]]
    visited, depth_dict = set(), {}

    # Lưu các trạng thái ban đầu vào steps (depth = 0)
    for b in belief:
        for s in b:
            steps.append((list(s), 0))
            depth_dict[s] = 1
            visited.add(tuple(sorted(s)))

    # ------------------------------
    # Các hàm hỗ trợ
    # ------------------------------
    def can_place(state, row, col):
        """Kiểm tra có thể đặt quân (row, col) vào state không."""
        for r, c in state:
            if r == row or c == col:
                return False
        return True

    def move_all(states):
        """Di chuyển 1 quân (cột kế tiếp) trong tất cả state của belief hiện tại."""
        next_states = []
        for state in states:
            if not state:
                continue
            r, c = state[-1]
            for new_c in range(c + 1, N):
                if can_place(state[:-1], r, new_c):
                    new_state = list(state)
                    new_state[-1] = (r, new_c)
                    next_states.append(tuple(new_state))
                    break  # chỉ di chuyển 1 lần cho mỗi state
        return next_states

    def place_all(states):
        """Đặt thêm 1 quân (1 lần duy nhất) vào tất cả state."""
        next_states = []
        for state in states:
            row = len(state)
            if row >= N:
                continue
            used_cols = {c for _, c in state}
            for col in range(N):
                if col not in used_cols and can_place(state, row, col):
                    next_states.append(state + ((row, col),))
                    break  # chỉ đặt 1 quân duy nhất
        return next_states

    # ------------------------------
    # Vòng lặp chính
    # ------------------------------
    while belief and not found:
        current_belief = belief.pop()  # lấy ra 1 tập state
        exp += 1
        depth = max(depth_dict.get(s, 1) for s in current_belief)

        # Kiểm tra goal trong bất kỳ state nào
        for s in current_belief:
            if len(s) == N and set(s) == set(goal):
                steps.append((list(s), depth))
                found = True
                break
        if found:
            break

        # --- Move tất cả state ---
        move_belief = move_all(current_belief)
        if move_belief:
            belief.append(move_belief)
            for s in move_belief:
                key = tuple(sorted(s))
                if key not in visited:
                    visited.add(key)
                    depth_dict[s] = depth + 1
                    steps.append((list(s), depth + 1))
                    gen += 1

        # --- Place tất cả state ---
        place_belief = place_all(current_belief)
        if place_belief:
            belief.append(place_belief)
            for s in place_belief:
                key = tuple(sorted(s))
                if key not in visited:
                    visited.add(key)
                    depth_dict[s] = depth + 1
                    steps.append((list(s), depth + 1))
                    gen += 1

    # ------------------------------
    # Kết quả
    # ------------------------------
    return {
        "steps": steps,
        "generated": gen,
        "expanded": exp
    }
