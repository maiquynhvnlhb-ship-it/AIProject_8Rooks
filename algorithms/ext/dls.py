def dls(goal, limit):
    """
    Depth-Limited Search (DLS)
    """
    def check(vt, col):
        # Kiểm tra xem có thể đặt quân ở cột col mà không trùng với cột trước
        for _, c in vt:
            if c == col:
                return False
        return True

    steps = []
    gen = 0
    exp = 0

    def rec(vt):
        nonlocal gen, exp, steps

        # Lưu lại bước (để hiển thị mô phỏng)
        steps.append(vt[:])

        # Nếu đã đặt đủ 8 quân và đúng goal → thành công
        if len(vt) == 8 and [c for _, c in vt] == goal:
            return True

        # Nếu đã đặt đủ limit quân → dừng mở rộng (depth limit)
        if len(vt) == limit:
            return False

        exp += 1
        row = len(vt)  # hàng hiện tại

        for c in range(8):
            if check(vt, c):
                gen += 1
                new_state = vt + [(row, c)]
                if rec(new_state):
                    return True
        return False

    # Gọi đệ quy từ trạng thái rỗng (bắt đầu từ hàng 0)
    rec([])
    return {"steps": steps, "generated": gen, "expanded": exp}
