from collections import deque
import copy
import random

def ac3(goal):
    """
    AC-3 kết hợp Backtracking cho bài toán N quân xe (N Rooks)
    Trả về dict {"steps": steps, "generated": gen, "expanded": exp}
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

    # -----------------------------------------------------
    #  Các hàm phụ
    # -----------------------------------------------------
    def consistent(x, y):
        return x != y  # ràng buộc Xi != Xj (không cùng cột)

    def revise(domains, Xi, Xj):
        """Loại khỏi domain[Xi] các giá trị không hợp lệ với domain[Xj]."""
        revised = False
        to_remove = set()
        for x in domains[Xi]:
            if not any(consistent(x, y) for y in domains[Xj]):
                to_remove.add(x)
        if to_remove:
            domains[Xi] -= to_remove
            revised = True
        return revised

    def ac3(domains):
        """Chạy AC3 trên miền hiện tại."""
        queue = deque([(i, j) for i in range(N) for j in range(N) if i != j])
        while queue:
            Xi, Xj = queue.popleft()
            if revise(domains, Xi, Xj):
                if not domains[Xi]:
                    return False
                for Xk in range(N):
                    if Xk != Xi and Xk != Xj:
                        queue.append((Xk, Xi))
        return True

    def record_step():
        placement = [(r, assignment[r]) for r in sorted(assignment)]
        steps.append((placement, 0))

    # -----------------------------------------------------
    #  Backtracking + AC3
    # -----------------------------------------------------
    def backtrack(row, domains):
        nonlocal gen, exp, found, solution

        if found:
            return True

        if row == N:  # đã gán hết biến
            placement = [(r, assignment[r]) for r in range(N)]
            if placement == goal:
                found = True
                solution = placement
                record_step()
                return True
            return False

        exp += 1
        for val in list(domains[row]):
            gen += 1
            assignment[row] = val
            record_step()

            # Copy miền để sửa độc lập
            new_domains = {r: set(domains[r]) for r in range(N)}

            # Cập nhật domain: loại giá trị trùng cột ở các hàng khác
            for r in range(N):
                if r != row and val in new_domains[r]:
                    new_domains[r].remove(val)

            # Duy trì arc-consistency
            if ac3(new_domains):
                if backtrack(row + 1, new_domains):
                    return True

            # backtrack
            del assignment[row]
            record_step()

        return False

    # Bắt đầu từ hàng 0
    backtrack(0, domains)

    return {
        "steps": steps,
        "generated": gen,
        "expanded": exp
    }
