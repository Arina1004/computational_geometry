import math

def get_angle(point1, point2):
  print(point1, point2)
  def dist(p1, p2):
    print(p1, p2)
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

  angle_cos = math.acos((point2[0] - point1[0]) / dist(point1, point2))
  angle_sin = math.asin((point2[1] - point1[1]) / dist(point1, point2))

  if angle_sin >= 0:
      return angle_cos * 180 / math.pi
  else:
      return (2 * math.pi - angle_cos) * 180 / math.pi

def get_turn_sign(vector, point):
  x1, y1 = vector[0][:2]

  x2, y2 = vector[1][:2]

  x3, y3 = point[:2]

  a = (x2 - x1, y2 - y1)
  b = (x3 - x2, y3 - y2)

  result = 1 if ((x2 - x1) * (y3 - y2) - (x3 - x2) * (y2 - y1)) > 0 else -1

  return result

def localization_with_turn(points, point, eps):
  sum = 0

  for i in range(len(points)):
      angle = abs(get_angle(point, points[i]) - get_angle(point, points[(i + 1) % len(points)]))

      angle = 360 - angle if angle > 180 else angle
      sum += get_turn_sign([point, points[i]], points[(i + 1) % len(points)]) * angle

  if abs(360 - abs(sum)) < eps:
      return True

  return False