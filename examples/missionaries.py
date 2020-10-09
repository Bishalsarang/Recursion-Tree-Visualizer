from visualiser.visualiser import Visualiser as vs

start_state = (3, 3, 1)
goal_state = (0, 0, 0)

options = [(2, 0), (1, 1), (0, 2), (1, 0), (0, 1)]
visited = dict()


def is_valid(m, c):
    return 0 <= m <= 3 and 0 <= c <= 3


@vs(ignore_args=["node_num", "level"])
def dfs(m, c, s, level):
    if (m, c, s) == goal_state:
        return True

    if 0 < m < c:
        return False

    right_side_m = 3 - m
    right_side_c = 3 - c
    if 0 < right_side_m < right_side_c:
        return False

    visited[(m, c, s)] = True

    if s == 1:
        op = -1
    else:
        op = 1

    solved = False
    for i in range(5):
        next_m, next_c, next_side = m + op * options[i][0], c + op * options[i][1], int(not s)

        if is_valid(next_m, next_c):

            if (next_m, next_c, next_side) not in visited:
                solved = (solved or dfs(m=next_m, c=next_c, s=next_side, level=level + 1))

                if solved:
                    return True
    return solved


if dfs(m=3, c=3, s=1, level=0):
    print("SOlution Found")
    # Save recursion tree to a file
    vs.make_animation("missionaries.gif", delay=2)
