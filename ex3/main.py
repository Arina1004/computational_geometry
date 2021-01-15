import math

def rotation(p1, p2, p3):
    return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])

def is_convex(points):
  n = len(points)
  left_turn = 0
  right_turn = 0

  for i in range(1,n):
    right_index = (i + 1) % len(points)
    if rotation(points[i-1], points[i], points[right_index]) > 0:
        left_turn = 1
    else:
        right_turn = 1
  return left_turn != right_turn
