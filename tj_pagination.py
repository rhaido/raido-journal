import isoweek
from datetime import datetime, date

class Pagination(object):
  def __init__(self, year, week):
    self.week = week
    self.year = year
    self.page = week

    current_date = datetime.today()
    self.isocalendar = []

    if current_date:
      self.isocalendar = date(current_date.year, current_date.month, current_date.day).isocalendar()
    

  @property
  def has_prev(self):
    return self.week > 1

  @property
  def has_next(self):
    return isoweek.Week(self.year, self.week) < isoweek.Week.last_week_of_year(self.year)

  def iter_pages(self, left_edge=52, left_current=3, middle = 26, right_limit=3):
    left_edge=(self.isocalendar)[1]
    left_limit=1
    middle=self.page
    right_limit=1
    
    last = self.page + 1

    print last, left_edge, left_limit, middle, right_limit

    for num in xrange(left_edge, 0, -1):
      if num >= left_edge - left_limit or \
        (num >= middle - 1 and \
        num <= middle + 1) or \
        num <= right_limit + 1 or \
        num == (self.page + left_edge)/2 or \
        num == (self.page + 1)/2:

        if last - 1 != num:
          yield None
        
        yield num
        last = num

  def iter_years(self):
    for num in xrange(2000, self.year):
      yield num
