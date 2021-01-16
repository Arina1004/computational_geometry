import math
min_point = 0
boundary_points = []

def clockwiseangle_and_distance(point):
    global min_point
    origin = min_point
    refvec = [1, 1]
    # Vector between point and the origin: v = p - o
    vector = [point[0]-origin[0], point[1]-origin[1]]
    # Length of vector: ||v||
    lenvector = math.hypot(vector[0], vector[1])
    # If length is zero there is no angle
    if lenvector == 0:
        return -math.pi, 0
    # Normalize vector: v/||v||
    normalized = [vector[0]/lenvector, vector[1]/lenvector]
    dotprod  = normalized[0]*refvec[0] + normalized[1]*refvec[1]     # x1*x2 + y1*y2
    diffprod = refvec[1]*normalized[0] - refvec[0]*normalized[1]     # x1*y2 - y1*x2
    angle = math.atan2(diffprod, dotprod)
    # Negative angles represent counter-clockwise angles so we need to subtract them
    # from 2*pi (360 degrees)
    if angle < 0:
        return 2*math.pi+angle, lenvector
    # I return first the angle because that's the primary sorting criterium
    # but if two vectors have the same angle then the shorter distance should come first.
    return angle, lenvector

def rotation(p1, p2, p3):
    return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])

def graham_scan(points):
  global min_point
  n = len(points)
  min_point = points[0]
  min_point_index = 0
  boundary_points = []

  #find p1
  for i in range(1,n):
      if points[i][1] == min_point[1] and min_point[0] > points[i][0]:
          min_point = points[i]
          min_point_index = i
      elif points[i][1] > min_point[1]:
          min_point = points[i]
          min_point_index = i
  # del boundary_points[:min_point_index]
  boundary_points.append(min_point)
  sorted_points = sorted(points, key=clockwiseangle_and_distance)
  boundary_points.append(sorted_points[1])
  for s in sorted_points[2:]:
      while rotation(boundary_points[-2], boundary_points[-1], s) >= 0:
          del boundary_points[-1]
      boundary_points.append(s)
  print(boundary_points)
  return boundary_points
