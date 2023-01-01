import sys
import re
from collections import defaultdict
import copy

energy_map = {
    "A": 1,
    "B": 10,
    "C": 100,
    "D": 1000
}


def room_corridor_coordinate(room_id) -> int:
    return 2 * room_id + 2


def is_sorted(rooms) -> bool:
    # if a room only consists of one type of pod then the set of the room will be of length 1
    for room in rooms.values():
        if len(set(room)) == 2:
            return False

    return True


def corridor_empty(corridor):
    # if a pod is in any coordinate in the corridor return false
    for c in corridor:
        if c is not None:
            return False
    return True


def can_go_to_room(rooms, corridor, corridor_c, room_id):
    if corridor_empty(corridor[corridor_c + 1:room_corridor_coordinate(room_id) + 1]):
        if len(rooms[room_id]) == 0:
            # empty room, no problem
            return True
        elif len(rooms[room_id]) == 1:
            if corridor[corridor_c] == rooms[room_id][0]:
                # if room has one occupant of the same pod type
                return True

    return False


def go_to_room(rooms, corridor):
    if not corridor_empty(corridor):
        pass


def pod_sort(rooms, corridor, cost):
    if is_sorted(rooms):
        return cost


pod_type_room_col = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8,
}


def corridor_free(c, t, corridor):
    if c < t:
        # c = 1, t = 6
        for i in range(c + 1, t + 1):
            if corridor[i] != ".":
                return False
    else:
        # t = 2, c = 7
        for i in range(c - 1, t - 1, -1):
            if corridor[i] != ".":
                return False

    return True


moves_memo = {}


def moves(pod, board, locked):
    frozen_board = tuple(
        tuple(row)
        for row in board
    )
    key = (pod, frozen_board, tuple(locked))
    if key in moves_memo:
        # print("could make use of memo")
        return moves_memo[key]
    # ((x,y), cost)
    ms = []
    pod_type = board[pod[0]][pod[1]]
    target_col = pod_type_room_col[pod_type]
    energy = energy_map[pod_type]
    if pod[0] == 0:
        # in corridor need to go to its room
        valid = False
        nr_steps = abs(pod[1] - target_col)
        target = None

        if corridor_free(pod[1], target_col, board[0]):
            if board[2][target_col] == ".":
                nr_steps += 2
                valid = True
                target = (2, target_col)
            elif board[1][target_col] == "." and board[2][target_col] == pod_type:
                nr_steps += 1
                valid = True
                target = (1, target_col)
            if valid:
                ms.append((target, nr_steps * energy))
    elif pod[0] == 1:
        # top of room
        if pod[1] == target_col and board[2][pod[1]] == pod_type:
            locked.add(pod)
        elif pod not in locked:
            # right
            for s, i in enumerate(range(pod[1], 11)):
                if board[0][i] != ".":
                    break
                if i not in [2, 4, 6, 8]:
                    ms.append(((0, i), (1 + s) * energy))
            for s, i in enumerate(range(pod[1], 0 - 1, -1)):
                if board[0][i] != ".":
                    break
                if i not in [2, 4, 6, 8]:
                    ms.append(((0, i), (1 + s) * energy))
    elif pod[0] == 2:
        # bottom
        if pod[1] == pod_type_room_col:
            # already in correct spot, lock it
            locked.add(pod)
        else:
            if pod not in locked and board[1][pod[1]] == ".":
                for s, i in enumerate(range(pod[1], 11)):
                    if board[0][i] != ".":
                        break
                    if i not in [2, 4, 6, 8]:
                        ms.append(((0, i), (2 + s) * energy))
                for s, i in enumerate(range(pod[1], 0 - 1, -1)):
                    if board[0][i] != ".":
                        break
                    if i not in [2, 4, 6, 8]:
                        ms.append(((0, i), (2 + s) * energy))

            if pod[1] == pod_type_room_col and pod not in locked:
                locked.add(pod)
    else:
        assert False

    moves_memo[key] = ms
    return ms


def moves2(pod, board, locked):
    frozen_board = tuple(
        tuple(row)
        for row in board
    )
    key = (pod, frozen_board, tuple(locked))
    if key in moves_memo:
        # print("could make use of memo")
        return moves_memo[key]
    # ((x,y), cost)
    ms = []
    pod_type = board[pod[0]][pod[1]]
    tgt_col = pod_type_room_col[pod_type]
    energy = energy_map[pod_type]
    if pod[0] == 0:
        # in corridor need to go to its room
        valid = False
        nr_steps = abs(pod[1] - tgt_col)
        target = None

        if corridor_free(pod[1], tgt_col, board[0]):
            if board[4][tgt_col] == ".":
                nr_steps += 4
                valid = True
                target = (4, tgt_col)
            elif board[3][tgt_col] == "." and board[4][tgt_col] == pod_type:
                nr_steps += 3
                valid = True
                target = (3, tgt_col)
            elif board[2][tgt_col] == "." and board[3][tgt_col] == board[4][tgt_col] == pod_type:
                nr_steps += 2
                valid = True
                target = (2, tgt_col)
            elif board[1][tgt_col] == "." and board[2][tgt_col] == board[3][tgt_col] == board[4][tgt_col] == pod_type:
                nr_steps += 1
                valid = True
                target = (1, tgt_col)
            if valid:
                ms.append((target, nr_steps * energy))
    else:
        row = pod[0]

        if can_lock(board, pod[1], row, pod_type):
            locked.add(pod)
        else:
            # if at the bottom and free above OR
            # if second to the bottom and free above OR
            # if second to the top and free above OR
            # if at entrance -> move pod
            if (row == 4 and board[row - 1][pod[1]] == ".") or \
                    (row == 3 and board[row - 1][pod[1]] == ".") or \
                    (row == 2 and board[row - 1][pod[1]] == ".") or row == 1:

                for s, i in enumerate(range(pod[1], 11)):
                    if board[0][i] != ".":
                        break
                    if i not in [2, 4, 6, 8]:
                        ms.append(((0, i), (row + s) * energy))
                for s, i in enumerate(range(pod[1], 0 - 1, -1)):
                    if board[0][i] != ".":
                        break
                    if i not in [2, 4, 6, 8]:
                        ms.append(((0, i), (row + s) * energy))

    moves_memo[key] = ms
    return ms


def can_lock(board, col, row, pod_type) -> bool:
    col_for_pod = pod_type_room_col[pod_type]
    if col != col_for_pod:
        # the pod at row, col is in the wrong room
        return False

    # the current pod is in the right room, need to check pods below it
    # only if all of them are of the same pod type then we can lock
    for r in range(row, 5):
        if board[r][col] != pod_type:
            return False

    return True


def make_move(pod, move, board, locked):
    # move the pod on the board, removing the old placement and put "." in it's place
    # return the new coordinates for the pod, the new board and if pod is back in a room, add to locked
    new_board = copy.deepcopy(board)
    val = board[pod[0]][pod[1]]
    (row, col), cost = move
    new_board[row][col] = val
    new_board[pod[0]][pod[1]] = "."

    if row in [1, 2, 3, 4]:
        new_locked = copy.deepcopy(locked)
        new_locked.add((row, col))
    else:
        new_locked = locked

    return (row, col), new_board, new_locked, cost


def board_freeze(board):
    return (
        tuple(tuple(r) for r in board)
    )


cost_memo = {}

solutions = []
costs = set()


def solve(board, target, pods, locked, cost, m, p2):
    if len(costs) > 0 and cost > min(costs):
        return 1e9

    frozen_board = board_freeze(board)
    key = (frozen_board, target, tuple(pods), tuple(locked), cost)
    if key in cost_memo:
        return cost_memo[key]
    if frozen_board == target:
        solutions.append((cost, m))
        costs.add(cost)
        return cost

    c_min = 1e9
    for i in range(len(pods)):
        if pods[i] in locked:
            continue
        if not p2:
            ms = moves(pods[i], board, locked)
        else:
            ms = moves2(pods[i], board, locked)
        for move in ms:
            new_pod, new_board, new_locked, move_cost = make_move(pods[i], move, board, locked)
            new_pods = copy.deepcopy(pods)
            new_pods[i] = new_pod
            c = solve(new_board, target, new_pods, new_locked, cost + move_cost, m + [(board[pods[i][0]][pods[i][1]], pods[i], move)], p2)
            if c < c_min:
                c_min = c

    cc = cost + c_min
    cost_memo[key] = cc
    return cc


def main():
    board = [
        [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", "C", ".", "B", ".", "D", ".", "A", ".", "."],
        [".", ".", "B", ".", "D", ".", "A", ".", "C", ".", "."]
    ]
    board2 = [
        [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", "C", ".", "B", ".", "D", ".", "A", ".", "."],
        [".", ".", "D", ".", "C", ".", "B", ".", "A", ".", "."],
        [".", ".", "D", ".", "B", ".", "A", ".", "C", ".", "."],
        [".", ".", "B", ".", "D", ".", "A", ".", "C", ".", "."]
    ]
    target = (
        (".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."),
        (".", ".", "A", ".", "B", ".", "C", ".", "D", ".", "."),
        (".", ".", "A", ".", "B", ".", "C", ".", "D", ".", ".")
    )

    target2 = (
        (".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."),
        (".", ".", "A", ".", "B", ".", "C", ".", "D", ".", "."),
        (".", ".", "A", ".", "B", ".", "C", ".", "D", ".", "."),
        (".", ".", "A", ".", "B", ".", "C", ".", "D", ".", "."),
        (".", ".", "A", ".", "B", ".", "C", ".", "D", ".", ".")
    )

    pods = [
        (1, 2), (1, 4), (1, 6), (1, 8),
        (2, 2), (2, 4), (2, 6), (2, 8)
    ]

    pods2 = [
        (1, 2), (1, 4), (1, 6), (1, 8),
        (2, 2), (2, 4), (2, 6), (2, 8),
        (3, 2), (3, 4), (3, 6), (3, 8),
        (4, 2), (4, 4), (4, 6), (4, 8)
    ]

    solve(board, target, pods, set(), 0, [], p2=False)
    print("part1", min(solutions, key=lambda x: x[0]))
    moves_memo.clear()
    cost_memo.clear()
    solutions.clear()
    costs.clear()
    solve(board2, target2, pods2, set(), 0, [], p2=True)
    print("part2", min(solutions, key=lambda x: x[0]))


if __name__ == '__main__':
    main()
