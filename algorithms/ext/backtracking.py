import random

def backtracking(goal):
    """
    Backtracking cho bài toán N quân (8 Rooks).
    Trả về dict {"steps": steps, "generated": gen, "expanded": exp}
    """
    N = len(goal)
    cols = set()
    placement = []
    steps = []
    found = False
    gen = 0
    exp = 0

    def record_step():
        # Lưu bản sao trạng thái hiện tại để GUI
        steps.append((list(placement), 0))

    def solve(row, remaining_cols):
        nonlocal found, gen, exp

        # Mỗi lời gọi solve(~node) xem như 1 nút được MỞ RỘNG
        exp += 1

        if found:
            return True

        if row == N:
            # So sánh theo dạng list cột (phù hợp các hàm trước của bạn)
            if [c for _, c in placement] == goal:
                found = True
                record_step()
                return True
            return False

        # Lấy miền cột và thử ngẫu nhiên
        cols_to_try = remaining_cols[row][:]
        random.shuffle(cols_to_try)

        for col in cols_to_try:
            if col in cols:
                continue

            gen += 1  # sinh 1 nút con

            # Đặt
            cols.add(col)
            placement.append((row, col))
            record_step()  # chỉ ghi khi đặt, KHÔNG ghi khi backtrack

            # (Tuỳ chọn) Forward Checking thật sự: loại col khỏi các hàng sau
            new_remaining = {r: remaining_cols[r][:] for r in range(N)}
            for r2 in range(row, N):
                if col in new_remaining[r2]:
                    new_remaining[r2].remove(col)

            # Đệ quy
            if solve(row + 1, new_remaining):
                return True

            # Backtrack
            placement.pop()
            cols.remove(col)
            # Không record_step() ở đây để steps không “phình” so với generated

        return False

    # Khởi tạo miền ban đầu
    remaining_cols = {r: list(range(N)) for r in range(N)}
    solve(0, remaining_cols)

    return {
        "steps": steps,
        "generated": gen,
        "expanded": exp
    }
