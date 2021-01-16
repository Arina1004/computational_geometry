import math

boundary_points = []

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

def distance(point):
    global current_point
    origin = current_point
    refvec = [1, 1]
    # Vector between point and the origin: v = p - o
    vector = [point[0]-origin[0], point[1]-origin[1]]
    # Length of vector: ||v||
    lenvector = math.hypot(vector[0], vector[1])

    return lenvector

def rotation(p1, p2, p3):
    return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])

def localization(point, polygon):
    left = 0
    right = 0
    for i in range(0,len(polygon)):
        right_index = (i + 1) % len(polygon)
        if rotation(polygon[i], polygon[right_index], point) > 0:
            left = 1
        else:
            right = 1
        if left == right:
            return False
    else:
        return True

def crossing(point, vertex, boundary_points):
    left = 0
    right = 0
    for j in range(len(boundary_points)):
        rotate = rotation(point,vertex, boundary_points[j])
        if rotate == 0:
            continue
        elif rotate > 0:
            left = 1
        else:
            right = 1
        if left == right:
            return True
    return False


def scan(points):
    global min_point, current_point
    n = len(points)
    boundary_points = points[:3]
    if not clockwise(boundary_points):
        boundary_points.reverse()

    for i in range(3,n):
        current_point = points[i]
        if not localization(current_point, boundary_points):
            sorted_points = sorted(boundary_points, key=distance)
            start_point_index = boundary_points.index(sorted_points[0])
            left = 0
            right = 0
            for j in range(len(boundary_points)):
                rotate = rotation(current_point,boundary_points[start_point_index], boundary_points[j])
                if rotate == 0:
                    continue
                elif rotate > 0:
                    left = 1
                else:
                    right = 1
                if left == right:
                    left_point_index = (start_point_index + 1 ) % len(boundary_points)
                    right_point_index = start_point_index - 1
                    break
            else:
                if left > 0:
                    left_point_index = start_point_index
                    right_point_index = start_point_index - 1
                else:
                    left_point_index = (start_point_index + 1 ) % len(boundary_points)
                    right_point_index = start_point_index
            while crossing(current_point, boundary_points[left_point_index], boundary_points):
                left_point_index = (left_point_index + 1) % len(boundary_points)
            while crossing(current_point, boundary_points[right_point_index], boundary_points):
                right_point_index = right_point_index - 1

            if left_point_index == 0:
                boundary_points = boundary_points[:(right_point_index % len(boundary_points)) +1] + [current_point]
            else:
                boundary_points = boundary_points[:right_point_index+1] + [current_point] + boundary_points[left_point_index:len(boundary_points)]
    print(boundary_points)
    return boundary_points