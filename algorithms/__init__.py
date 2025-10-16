# algorithms/__init__.py
import time
from typing import List, Callable, Any, Tuple, Dict
from .base import meta

# ---------- Chuẩn hóa bước ----------

def _normalize_steps(steps_raw):
    norm = []
    for item in steps_raw or []:
        if isinstance(item, tuple) and item and isinstance(item[0], list):
            norm.append(item[0])
        else:
            norm.append(item)
    return norm


def _finalize_result(out: Any, started_at: float):
    runtime_ms = round((time.time()+0.00001 - started_at) * 1000, 3)

    if isinstance(out, dict):
        steps = _normalize_steps(out.get("steps"))
        generated = int(out.get("generated", 0))
        expanded = int(out.get("expanded", 0))
    else:
        steps = _normalize_steps(out)
        generated = 0
        expanded = 0

    solution = steps[-1] if steps else None
    depth = len(solution) if solution else 0

    stats = {
        "generated": generated,
        "expanded": expanded,
        "steps_count": len(steps),
        "depth": depth,
        "runtime_ms": runtime_ms,
    }
    return steps, stats, solution


# ---------- Trình bao mục tiêu ----------

def _wrap_cols(func: Callable, name: str, group: str, attributes: str, description: str):
    def solve(goal: List[int]):
        t0 = time.time()
        out = func(goal)
        return _finalize_result(out, t0)
    return {"META": meta(name, group, attributes, description), "solve": solve}


def _wrap_places(func: Callable, name: str, group: str, attributes: str, description: str):
    def solve(goal: List[int]):
        goal_places = [(r, goal[r]) for r in range(len(goal))]
        t0 = time.time()
        out = func(goal_places)
        return _finalize_result(out, t0)
    return {"META": meta(name, group, attributes, description), "solve": solve}


# ---------- Đăng ký thuật toán ----------

REGISTRY: Dict[str, Dict[str, Any]] = {}

def _try_register(key, import_stmt, func_attr, wrap_kind, name, group, attributes, description, call_adapter=None):
    try:
        loc: Dict[str, Any] = {}
        exec(import_stmt, globals(), loc)
        _mod = loc.get("_mod")
        if not _mod:
            return
        func = getattr(_mod, func_attr, None)
        if not func:
            return
        if call_adapter:
            func = call_adapter(func)
        wrapper = _wrap_cols if wrap_kind == "cols" else _wrap_places
        REGISTRY[key] = wrapper(func, name, group, attributes, description)
    except Exception:
        pass


# ---------- Tìm kiếm không có thông tin (Uninformed Search) ----------

_try_register("BFS", "from .ext import bfs as _mod", "bfs", "cols",
              "BFS", "Tìm kiếm không có thông tin",
              "Rộng trước – Không tối ưu",
              "Thuật toán tìm kiếm theo chiều rộng, mở rộng tất cả các nút cùng cấp trước.")

_try_register("DFS", "from .ext import dfs as _mod", "dfs", "cols",
              "DFS", "Tìm kiếm không có thông tin",
              "Sâu trước – Không tối ưu",
              "Thuật toán tìm kiếm theo chiều sâu, đi sâu xuống nhánh trước khi quay lại.")

_try_register("DLS", "from .ext import dls as _mod", "dls", "cols",
              "DLS", "Tìm kiếm không có thông tin",
              "Giới hạn độ sâu",
              "Tìm kiếm theo chiều sâu nhưng giới hạn ở một độ sâu nhất định.",
              call_adapter=lambda f: (lambda goal: f(goal, limit=8)))

_try_register("IDS", "from .ext import ids as _mod", "ids", "cols",
              "IDS", "Tìm kiếm không có thông tin",
              "Lặp sâu tăng dần",
              "Kết hợp DFS và DLS: tăng giới hạn độ sâu dần để đảm bảo tìm thấy nghiệm tối ưu.",
              call_adapter=lambda f: (lambda goal: f(goal, 8)))

_try_register("UCS", "from .ext import ucs as _mod", "ucs", "cols",
              "UCS", "Tìm kiếm không có thông tin",
              "Chi phí đồng nhất",
              "Luôn mở rộng nút có chi phí tích lũy thấp nhất.")


# ---------- Tìm kiếm ràng buộc (CSP Search) ----------

_try_register("Backtracking", "from .ext import backtracking as _mod", "backtracking", "cols",
              "Backtracking", "Tìm kiếm ràng buộc (CSP)",
              "Quay lui cổ điển",
              "Thử và loại trừ")

_try_register("Forward Checking", "from .ext import forward_checking as _mod", "forward_checking", "cols",
              "Forward Checking", "Tìm kiếm ràng buộc (CSP)",
              "Dự đoán trước ràng buộc",
              "Giảm không gian tìm kiếm bằng cách kiểm tra ràng buộc trước khi mở rộng nút.")

_try_register("AC-3","from .ext import AC_3 as _mod","ac3","places",
            "AC-3(CSP)","Ràng buộc (CSP)",
            "Duy trì tính nhất quán cung (arc-consistency) cho ràng buộc nhị phân; tiền xử lý/lan truyền ràng buộc; kết hợp Backtracking.",
            "Môi trường quan sát đầy đủ (Fully Observable).")

# ---------- Tìm kiếm có thông tin (Informed / Heuristic Search) ----------

_try_register("Greedy Best-First", "from .ext import greedy as _mod", "greedy", "places",
              "Greedy Best-First", "Tìm kiếm có thông tin",
              "Tham lam theo heuristic",
              "Chọn nút có giá trị heuristic thấp nhất (ước lượng gần đích nhất).")

_try_register("A*", "from .ext import astar as _mod", "astar", "places",
              "A*", "Tìm kiếm có thông tin",
              "Tối ưu theo heuristic",
              "Kết hợp chi phí thực tế và heuristic (f = g + h) để tìm đường đi ngắn nhất.")


# ---------- Tìm kiếm cục bộ (Local Search) ----------

_try_register("Hill-Climbing", "from .ext import hill_climbing as _mod", "hill_climbing", "places",
              "Hill-Climbing", "Tìm kiếm cục bộ",
              "Leo đồi",
              "Luôn di chuyển sang trạng thái lân cận tốt hơn cho đến khi đạt cực đại cục bộ.")

_try_register("Beam Search", "from .ext import beam_search as _mod", "beam_search", "places",
              "Beam Search", "Tìm kiếm cục bộ",
              "Tìm kiếm chùm tia",
              "Giữ lại K trạng thái tốt nhất ở mỗi bước để giới hạn không gian tìm kiếm.")

_try_register("Genetic Algorithm", "from .ext import genetic as _mod", "genetic_algorithm", "places",
              "Genetic Algorithm", "Tìm kiếm cục bộ",
              "Giải thuật di truyền",
              "Mô phỏng tiến hóa sinh học với các phép lai, đột biến và chọn lọc.")

_try_register("Simulated Annealing", "from .ext import simulated_annealing as _mod", "simulated_annealing", "places",
              "Simulated Annealing", "Tìm kiếm cục bộ",
              "Tôi luyện mô phỏng",
              "Cho phép bước lùi có xác suất giảm dần để thoát khỏi cực trị cục bộ.")


# ---------- Tìm kiếm trong không gian niềm tin (Belief-State) ----------

_try_register("AND–OR Search", "from .ext import and_or as _mod", "and_or_search", "places",
              "AND–OR Search", "Tìm kiếm trong không gian niềm tin",
              "Tìm kiếm cây AND–OR",
              "Giải bài toán khi có nhiều nhánh kết hợp logic (AND/OR).")

_try_register("Belief-State Search", "from .ext import belief_state as _mod", "belief_state", "places",
              "Belief-State Search", "Tìm kiếm trong không gian niềm tin",
              "Không gian niềm tin (Belief)",
              "Duy trì tập hợp các trạng thái có thể có dựa trên quan sát và hành động.")

_try_register("Belief-State (PO)", "from .ext import belief_state_PartiallyObservable as _mod", "belief_statePO", "places",
              "Belief-State (PO)", "Tìm kiếm trong không gian niềm tin",
              "Môi trường quan sát một phần",
              "Tìm kiếm trong điều kiện thông tin không đầy đủ hoặc bị ẩn (Partially Observable).")




# ---------- Public API ----------

def get_names():
    return list(REGISTRY.keys())

def get(name: str):
    item = REGISTRY[name]
    class ModuleLike:
        META = item["META"]
        @staticmethod
        def solve(goal):
            return item["solve"](goal)
    return ModuleLike
