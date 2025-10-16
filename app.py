import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Tuple, Any
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from algorithms import get_names, get


# ---------- Helpers ----------
def to_placements(step: Any) -> List[Tuple[int, int]]:
    if isinstance(step, tuple) and step and isinstance(step[0], list):
        return step[0]
    return step if isinstance(step, list) else []


def meta_get(meta_obj, key, default="-"):
    if meta_obj is None:
        return default
    if isinstance(meta_obj, dict):
        return meta_obj.get(key, default)
    return getattr(meta_obj, key, default)


# ---------- Chessboard Canvas ----------
class ChessBoardCanvas(tk.Canvas):
    def __init__(self, master, cell_size=56, *args, **kwargs):
        self.cell_size = cell_size
        w, h = cell_size * 8, cell_size * 8
        super().__init__(master, width=w, height=h, highlightthickness=0, *args, **kwargs)
        self.dark = "#1B4965"
        self.light = "#CAE9FF"
        self.piece_color = "#1B263B"
        self.font = ("Segoe UI Black", int(cell_size * 0.5))
        self.draw_board()
        self.current_pieces = []

    def draw_board(self):
        self.delete("square")
        for r in range(8):
            for c in range(8):
                x0, y0 = c * self.cell_size, r * self.cell_size
                x1, y1 = x0 + self.cell_size, y0 + self.cell_size
                color = self.light if (r + c) % 2 == 0 else self.dark
                self.create_rectangle(x0, y0, x1, y1, fill=color, width=0, tags="square")

    def draw_rooks(self, placements: List[Tuple[int, int]]):
        placements = to_placements(placements)
        for pid in getattr(self, "current_pieces", []):
            self.delete(pid)
        self.current_pieces = []
        for (r, c) in placements:
            x = c * self.cell_size + self.cell_size // 2
            y = r * self.cell_size + self.cell_size // 2
            pid = self.create_text(x, y, text="♜", fill="#E63946", font=self.font)
            self.current_pieces.append(pid)


# ---------- App ----------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("♜ 8 Rooks — Runtime & Steps Visualization")
        self.state("zoomed")

        self.configure(bg="#F6F9FC")

        # state
        self.goal = [0, 1, 2, 3, 5, 4, 7, 6]
        self.steps = []
        self.stats = {}
        self.solution = None
        self.anim_idx = 0
        self.anim_running = False
        self.anim_after = None
        self.chart_canvas_time = None
        self.chart_canvas_steps = None
        self.runtime_data = {}
        self.steps_data = {}

        self._build_ui()
        self._render_all()

    # ---------- UI ----------
    def _build_ui(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#F6F9FC")
        style.configure("TLabel", background="#F6F9FC", font=("Segoe UI", 10))
        style.configure("Header.TLabel", font=("Segoe UI Semibold", 12, "bold"), foreground="#1D3557")
        style.configure("Accent.TButton",
                        background="#457B9D", foreground="white",
                        font=("Segoe UI", 10, "bold"), padding=6)
        style.map("Accent.TButton",
                  background=[("active", "#2A9D8F"), ("!active", "#457B9D")])

        # Left panel
        left = ttk.Frame(self, width=340)
        left.grid(row=0, column=0, sticky="nsw", padx=10, pady=10)
        left.grid_propagate(False)
        left.grid_columnconfigure(1, weight=1)

        ttk.Label(left, text="Thuật toán", style="Header.TLabel").grid(row=0, column=0, padx=8, pady=8, sticky="w")

        self.combo_algo = ttk.Combobox(left, state="readonly", font=("Segoe UI", 10))
        self.combo_algo.grid(row=0, column=1, padx=8, pady=8, sticky="ew")
        self._refresh_algos()
        self.combo_algo.configure(postcommand=self._refresh_algos)


        # Control Buttons (colorful)
        # --- Các nút điều khiển ---
        btn_frame = ttk.Frame(left)
        btn_frame.grid(row=2, column=0, columnspan=2, padx=8, pady=8, sticky="ew")

        # Định nghĩa tiện ích tạo nút
        def make_btn(parent, text, command, color, row, col):
            btn = tk.Button(
                parent, text=text, command=command,
                font=("Segoe UI", 10, "bold"), bg=color, fg="white",
                activebackground="#264653", activeforeground="white",
                relief="flat", bd=0, padx=10, pady=8, cursor="hand2"
            )
            btn.grid(row=row, column=col, padx=4, pady=4, sticky="nsew")

        for r in range(2):
            btn_frame.grid_rowconfigure(r, weight=1)
        for c in range(2):
            btn_frame.grid_columnconfigure(c, weight=1)

        # Hàng 1
        make_btn(btn_frame, "▶ Chạy", self.on_run, "#2ECC71", 0, 0)
        make_btn(btn_frame, "⏸ Tạm dừng", self.on_pause, "#F4A261", 0, 1)
        # Hàng 2
        make_btn(btn_frame, "🔁 Bắt đầu lại", self.on_restart, "#A8A8A8", 1, 0)
        make_btn(btn_frame, "💡 Hiện lời giải", self.on_show_solution, "#9B5DE5", 1, 1)

        # Info
        ttk.Label(left, text="Thông tin thuật toán", style="Header.TLabel").grid(
            row=4, column=0, columnspan=2, padx=8, pady=(16, 4), sticky="w"
        )
        self.lbl_group = ttk.Label(left, text="Nhóm: -")
        self.lbl_attr = ttk.Label(left, text="Thuộc tính: -")
        self.lbl_group.grid(row=5, column=0, columnspan=2, padx=8, pady=2, sticky="w")
        self.lbl_attr.grid(row=6, column=0, columnspan=2, padx=8, pady=2, sticky="w")

        ttk.Label(left, text="Thống kê", style="Header.TLabel").grid(
            row=7, column=0, columnspan=2, padx=8, pady=(16, 4), sticky="w"
        )
        self.lbl_generated = ttk.Label(left, text="Số nút sinh ra: 0")
        self.lbl_expanded = ttk.Label(left, text="Số nút mở rộng: 0")

        self.lbl_steps = ttk.Label(left, text="Số bước đi: 0")
        self.lbl_runtime = ttk.Label(left, text="Thời gian thực thi: 0 ms")

        for i, w in enumerate([self.lbl_generated, self.lbl_expanded,
                               self.lbl_steps, self.lbl_runtime], start=8):
            w.grid(row=i, column=0, columnspan=2, padx=8, pady=2, sticky="w")

        # Main area
        main = ttk.Frame(self)
        main.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        for c in range(3):
            main.grid_columnconfigure(c, weight=1)
        main.grid_rowconfigure(1, weight=1)

        ttk.Label(main, text="📊 Biểu đồ thời gian / số nút sinh ra", style="Header.TLabel").grid(row=0, column=0)
        ttk.Label(main, text="♜ Thuật toán", style="Header.TLabel").grid(row=0, column=1)
        ttk.Label(main, text="🏁 Trạng thái đích", style="Header.TLabel").grid(row=0, column=2)

        # Chart frame
        self.chart_frame = ttk.Frame(main, borderwidth=2, relief="ridge")
        self.chart_frame.config(width=580, height=730)
        self.chart_frame.grid(row=1, column=0, sticky="nsew", padx=8, pady=8)
        self.chart_frame.grid_propagate(True)

        # Boards
        self.board_exec = ChessBoardCanvas(main)
        self.board_goal = ChessBoardCanvas(main)
        self.board_exec.grid(row=1, column=1, padx=8, pady=8)
        self.board_goal.grid(row=1, column=2, padx=8, pady=8)

        # Steps text
        bottom = ttk.Frame(self)
        bottom.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=(0, 8))
        bottom.grid_columnconfigure(0, weight=1)
        bottom.grid_rowconfigure(1, weight=1)

        ttk.Label(bottom, text="📜 Steps (danh sách trạng thái)", style="Header.TLabel").grid(
            row=0, column=0, sticky="w", pady=(0, 5)
        )

        # Frame chứa Text + Scrollbar để dễ co giãn
        text_frame = ttk.Frame(bottom)
        text_frame.grid(row=1, column=0, sticky="nsew")
        text_frame.grid_columnconfigure(0, weight=1)
        text_frame.grid_rowconfigure(0, weight=1)

        # Text widget mở rộng chiều ngang
        self.steps_list = tk.Text(
            text_frame,
            height=13,  # tăng chiều cao một chút
            width=200,  # tăng chiều rộng hiển thị
            wrap="none",
            bg="#FFFFFF",
            font=("Consolas", 10),
            relief="solid",
            borderwidth=1,
        )
        self.steps_list.grid(row=0, column=0, sticky="nsew", padx=(0, 5))

        # Thanh cuộn dọc
        scroll_y = ttk.Scrollbar(text_frame, orient="vertical", command=self.steps_list.yview)
        scroll_y.grid(row=0, column=1, sticky="ns")
        self.steps_list.config(yscrollcommand=scroll_y.set)

    # ---------- Data ----------
    def _refresh_algos(self):
        try:
            names = sorted(get_names())
            cur = self.combo_algo.get()
            self.combo_algo["values"] = names
            if cur in names:
                self.combo_algo.set(cur)
            elif names:
                self.combo_algo.current(0)
        except Exception:
            pass

    def _on_algo_changed(self, *_):
        try:
            mod = get(self.combo_algo.get())
            m = getattr(mod, "META", None)
            self.lbl_group.config(text=f"Nhóm thuật toán: {meta_get(m, 'group')}")
            self.lbl_attr.config(text=f"Thuộc tính: {meta_get(m, 'attributes')}")
        except Exception:
            self.lbl_group.config(text="Nhóm thuật toán: -")
            self.lbl_attr.config(text="Thuộc tính: -")

    def _render_all(self):
        self._on_algo_changed()
        self.board_goal.draw_rooks([(r, c) for r, c in enumerate(self.goal)])
        self.board_exec.draw_rooks([])
        self._update_metrics_display()

    def _update_metrics_display(self):
        g = self.stats.get("generated", 0)
        e = self.stats.get("expanded", 0)
        d = self.stats.get("depth", 0) or "-"
        s = self.stats.get("steps_count", 0)
        t = self.stats.get("runtime_ms", 0)
        self.lbl_generated.config(text=f"Số nút sinh ra: {g}")
        self.lbl_expanded.config(text=f"Số nút mở rộng: {e}")

        self.lbl_steps.config(text=f"Số bước đi: {s}")
        self.lbl_runtime.config(text=f"Thời gian thực thi: {t} ms")

    def _populate_steps_text(self):
        self.steps_list.config(state="normal")
        self.steps_list.delete("1.0", "end")
        for i, st in enumerate(self.steps, 1):
            pl = to_placements(st)
            msg = ", ".join([f"({r},{c})" for r, c in pl])
            self.steps_list.insert("end", f"Bước {i}: {msg}\n")
        self.steps_list.config(state="disabled")

    # ---------- Controls ----------
    def on_confirm(self):
        """Chạy 1 thuật toán, cập nhật lời giải và 2 biểu đồ."""
        algo_name = self.combo_algo.get()
        if not algo_name:
            messagebox.showwarning("Thiếu thuật toán", "Hãy chọn thuật toán trước.")
            return

        # Cập nhật thông tin META mỗi lần xác nhận
        self._on_algo_changed()

        mod = get(algo_name)
        self.steps, self.stats, self.solution = mod.solve(self.goal)
        self.anim_idx = 0
        self.board_exec.draw_rooks([])

        # Lưu dữ liệu cho biểu đồ
        runtime = self.stats.get("runtime_ms", 0)
        generated = self.stats.get("generated", 0)
        self.runtime_data[algo_name] = runtime
        self.steps_data[algo_name] = generated

        # Cập nhật hiển thị
        self._update_metrics_display()
        self._populate_steps_text()
        self._update_charts()

    # ---------- Hai biểu đồ ----------
    def _update_charts(self):
        """Cập nhật biểu đồ thời gian và số nút sinh ra."""
        for child in self.chart_frame.winfo_children():
            child.destroy()

        if not self.runtime_data:
            return

        # ---- Biểu đồ thời gian ----
        fig1, ax1 = plt.subplots(figsize=(6, 3.5), dpi=100)
        sorted_runtime = dict(sorted(self.runtime_data.items(), key=lambda x: x[1]))
        names_rt = list(sorted_runtime.keys())
        times = [sorted_runtime[k] for k in names_rt]

        bars1 = ax1.barh(names_rt, times, color="#4B9CD3")
        ax1.set_xlabel("Thời gian (ms)")
        ax1.set_title("Thời gian thực thi")
        ax1.grid(axis="x", linestyle="--", alpha=0.6)
        ax1.set_xlim(0, max(times) * 1.2)

        # Thêm số hiển thị ở cuối thanh
        for bar in bars1:
            width = bar.get_width()
            ax1.text(width + max(times) * 0.02,
                     bar.get_y() + bar.get_height() / 2,
                     f"{width:.3f}",
                     va="center", ha="left", fontsize=9, color="#1B1B1B")

        fig1.tight_layout()
        chart1 = FigureCanvasTkAgg(fig1, master=self.chart_frame)
        chart1.draw()
        chart1.get_tk_widget().pack(fill="x", expand=True, pady=(5, 10))

        # ---- Biểu đồ số nút sinh ra ----
        fig2, ax2 = plt.subplots(figsize=(6, 3.5), dpi=100)
        sorted_gen = dict(sorted(self.steps_data.items(), key=lambda x: x[1]))
        names_st = list(sorted_gen.keys())
        generated = [sorted_gen[k] for k in names_st]

        bars2 = ax2.barh(names_st, generated, color="#FFB347")
        ax2.set_xlabel("Số nút sinh ra")
        ax2.set_title("Tổng số nút được sinh ra (Generated Nodes)")
        ax2.grid(axis="x", linestyle="--", alpha=0.6)
        ax2.set_xlim(0, max(generated) * 1.2)

        # Thêm số hiển thị ở cuối thanh
        for bar in bars2:
            width = bar.get_width()
            ax2.text(width + max(generated) * 0.02,
                     bar.get_y() + bar.get_height() / 2,
                     f"{int(width)}",
                     va="center", ha="left", fontsize=9, color="#1B1B1B")

        fig2.tight_layout()
        chart2 = FigureCanvasTkAgg(fig2, master=self.chart_frame)
        chart2.draw()
        chart2.get_tk_widget().pack(fill="x", expand=True, pady=(5, 5))

    # ---------- Animation ----------
    def on_run(self):
        """Nhấn 'Chạy' → tự động xác nhận và chạy thuật toán."""
        algo_name = self.combo_algo.get()
        if not algo_name:
            messagebox.showwarning("Thiếu thuật toán", "Hãy chọn thuật toán trước.")
            return

        # chạy thuật toán và cập nhật biểu đồ
        self.on_confirm()

        # Sau đó bắt đầu animation
        if self.anim_running:
            return
        self.anim_running = True
        self.anim_idx = 0
        self._tick()

    def on_pause(self):
        self.anim_running = False
        if self.anim_after:
            self.after_cancel(self.anim_after)
            self.anim_after = None

    def on_restart(self):
        self.on_pause()
        self.anim_idx = 0
        self.board_exec.draw_rooks([])

    def on_show_solution(self):
        if not self.solution:
            if not self.steps:
                messagebox.showwarning("Chưa có dữ liệu", "Hãy chạy 'Xác nhận' trước.")
                return
            self.solution = self.steps[-1]
        self.on_pause()
        self.board_exec.draw_rooks(to_placements(self.solution))

    def _tick(self):
        if not self.anim_running:
            return
        if self.anim_idx >= len(self.steps):
            self.anim_running = False
            return
        current = self.steps[self.anim_idx]
        self.board_exec.draw_rooks(to_placements(current))
        self.anim_idx += 1
        self.anim_after = self.after(500, self._tick)


if __name__ == "__main__":
    App().mainloop()
