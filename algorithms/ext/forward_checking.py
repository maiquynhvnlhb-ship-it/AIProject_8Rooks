import random

def forward_checking(goal):
    """
    Forward Checking
    """
    N = len(goal)
    steps = []
    gen = 0
    exp = 0
    found = False
    solution = None

    # Miền ban đầu: mỗi hàng có thể chọn bất kỳ cột nào
    domains = {r: set(range(N)) for r in range(N)}
    assignment = {}

    def record_step():
        placement = [(r, assignment[r]) for r in sorted(assignment)]
        steps.append((placement[:], 0))

    def solve(row, domains):
        nonlocal found, solution, gen, exp

        if found:
            return True

        exp += 1  # mở rộng 1 node

        if row == N:  # tất cả biến đã gán
            placement = [(r, assignment[r]) for r in range(N)]
            # So sánh với goal (dạng list cột)
            if [c for _, c in placement] == goal:
                found = True
                solution = placement
                record_step()
                return True
            return False

        available_cols = list(domains[row])
        random.shuffle(available_cols)

        for col in available_cols:
            gen += 1  # sinh 1 nút con

            assignment[row] = col
            record_step()  # chỉ ghi khi đặt

            # Sao chép miền cho các hàng sau
            new_domains = {r: set(domains[r]) for r in range(N)}
            for r in range(row + 1, N):
                new_domains[r].discard(col)

            # Kiểm tra tất cả hàng sau còn miền khả dụng
            if all(new_domains[r] for r in range(row + 1, N)):
                if solve(row + 1, new_domains):
                    return True

            # Backtrack
            del assignment[row]

        return False

    solve(0, domains)

    return {
        "steps": steps,
        "generated": gen,
        "expanded": exp
    }
