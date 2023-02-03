def is_recently_visited(step, max_cycle_len):
    for coordinates in visited[-max_cycle_len:]:
        if coordinates == step:
           return True
    return False


visited = []
visited.append((3,1))
visited.append((3,3))
visited.append((3,4))
visited.append((3,6))
visited.append((3,9))
visited.append((3,10))
visited.append((3,11))
visited.append((3,13))
visited.append((3,14))
visited.append((3,16))

print(is_recently_visited((3, 899), 100))