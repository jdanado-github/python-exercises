import argparse
import csv
import sys

"""
This implementation will fail if the input if not correct. It assumes that all values
are correct numbers separated by commas.

There may be floating point problems as well due to the use of the isclose function to
perform equality between floating point numbers.

N - Number of points
The runtime complexity of the code is: O(N3). There is an inner loop and add_2_line searches
for all points again

It can be optimized but it was an initial solution available for the amount of time
 
@Author: Jose Danado
"""


class Point(object):
  """ Point class represents and manipulates x,y coords. """

  def __init__(self, x, y):
    """ Create a new point at the origin

    Args:
      x: X coordinate
      y: Y coordinate
      """
    self.x = x
    self.y = y

  def __str__(self):
    """ Represent the object as a string. """
    return '{},{}'.format(self.x, self.y)

  def __eq__(self, other):
    """Equality operation

    Args:
      other: Another point
    """
    return self.x == other.x and self.y == other.y

  def __ne__(self, other):
    """Inequality operation

    Args:
      other: Another point
    """
    return not self.__eq__(other)


class Line(object):
  """ Line class represents a line with its points and slope. """

  id_ = 0

  def __init__(self, p1, p2):
    """ Create a new Line and adds 2 points to it.

    Args:
      p1: Point p1 of the line
      p2: Point p2 of the line
    """
    self.points = []

    if p1 == p2:
      raise Exception('Cannot create a line with the same point {}'.format(p1))

    self.points.append(p1)
    self.points.append(p2)
    self.calculate_line_(p1, p2)
    Line.id_ += 1
    self.l_id = Line.id_

  def calculate_line_(self, p1, p2):
    """ calculate the slope of the line.

    Args:
      p1: Point p1 of the line
      p2: Point p2 of the line
    """
    if p2.x == p1.x:
      self.slope = None
      self.b = p1.x
    else:
      self.slope = (p2.y - p1.y) / (p2.x - p1.x)
      self.b = p1.y - self.slope * p1.x

  def point_exists(self, p):
    return any(p1.x == p.x and p1.y == p.y for p1 in self.points)

  def add_2_line(self, p):
    """Add a point is in line and not added, add it

    Args:
      p: A point p to add to the line
    """
    if self.point_exists(p):
      print 'Point {} already exists'.format(p)
      return

    p2 = self.points[0]

    if ((self.slope == None and p2.x == p.x) or
        isclose(self.slope, ((p2.y - p.y) / (p2.x - p.x)))):
      self.points.append(p)
    else:
      print 'point {} not in line {}'.format(p, self.__str__())

  def __str__(self):
    """Return a string with a representation of the object.

    Return:
      A string with format
    """
    return '{},{}'.format(self.l_id, ','.join([p.__str__() for p in self.points]))

  def id(self):
    """Identifier for this line"""
    return '{}_{}'.format(self.slope, self.b)

  def __eq__(self, other):
    return (other.slope == self.slope and other.b == self.b)

  def __ne__(self, other):
    return not self.__eq__(other)

  def size(self):
    """Returns the number of points in this line.

    Returns:
      Number of points
    """
    return len(self.points)


class Lines:
  """Read CSV files, calculate lines and write result to CSV file.
  """

  def __init__(self):
    """Creates a list of points to use"""
    self.points = []
    self.lines = {}

  def read_csv(self, csvfile):
    """Reads data from a file and stores it in points

    Args:
      csvfile: CSV file to use for input
      """
    reader = csv.reader(csvfile, delimiter=',')
    for line in reader:
      self.points.append(Point(float(line[0]), float(line[1])))
    csvfile.close()

  def calculate_lines(self):
    """Calculates all lines with two or more common points"""

    size = len(self.points)

    # Generate all lines with two points
    for i in range(0, size - 1):
      for j in range(i + 1, size):
        line = Line(self.points[i], self.points[j])

        # Get the identifier for this line
        id_ = line.id()

        if id_ in self.lines:
          self.lines[id_].add_2_line(self.points[i])
          self.lines[id_].add_2_line(self.points[j])
        else:
          self.lines[id_] = line

    # Try to add a point to a line
    for k in range(size):
      for line in self.lines:
        self.lines[line].add_2_line(self.points[k])

  def write_csv(self, csvfile):
    """Writes a list of lines found into the file

    Args:
      csvfile: CSV file to use for input
      """
    for line in self.lines:
      line_obj = self.lines[line]
      if line_obj.size() >= 3:
        csvfile.write('{}\n'.format(self.lines[line]))
    csvfile.close()


def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
  """If two floats are close"""
  return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


def main():
  """Main method with command-line parameters."""

  parser = argparse.ArgumentParser(description='Check lines with 3 or more common points.')
  parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin,
                      help='Path to the CSV input file (stdin if none)')
  parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout,
                      help='Path to the CSV output file (stdout if none)')
  args = parser.parse_args()

  # Process lines
  lines = Lines()
  lines.read_csv(args.infile)
  lines.calculate_lines()
  lines.write_csv(args.outfile)


if __name__ == "__main__":
  main()
