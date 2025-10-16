# Minimal heuristics for 8 Rooks
# Accepts goal as either: list[int] (cols) or list[(row,col)] (placements)

def _goal_to_cols(goal):
    if not goal:
        return [0,1,2,3,4,5,6,7]
    g0 = goal[0]
    if isinstance(g0, (list, tuple)):
        # convert placements to columns, sorted by row
        cols = [None]*8
        for r, c in goal:
            cols[r] = c
        return cols
    return goal

# def conflict_cost(state, goal=None):
#     """Simple 'g' cost: sum distance to goal for placed rows."""
#     cols = _goal_to_cols(goal)
#     return sum(abs(c - cols[r]) for r, c in state)

def cost_place_rook(vt, new_col, goal):
    row = len(vt)
    return 0 if new_col == goal[row] else 1

def cost_place_rook2(vt, goal):
    cost=0
    for r,c in vt:
        if c:=goal[r]:
            cost+=1
    return cost



def heuristic(state, goal):
    """General heuristic for local search/GA/beam: sum per-row distance to goal."""
    cols = _goal_to_cols(goal)
    return sum(abs(c - cols[r]) for r, c in state)

