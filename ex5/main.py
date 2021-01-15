import math

def rotation(p1, p2, p3):
    return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])

def clockwise(points):
  n = len(points)

  min_point_index = 0
  min_point = points[0]
  for i in range(1,n):
      if points[i][1] == min_point[1] and  min_point[0] > points[i][0]:
          min_point = points[i]
          min_point_index = i
      elif points[i][1] > min_point[1]:
          min_point = points[i]
          min_point_index = i
  if rotation(points[min_point_index-1], points[min_point_index], points[(min_point_index + 1) % n]) < 0:
      return False
  return True