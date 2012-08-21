import isoweek
from datetime import datetime, date

class Pagination(object):
  def __init__(self, year, week):
    self.week = week
    self.year = year
    self.page = week

    current_date = datetime.today()
    if current_date:
      isocalendar = date(current_date.year, current_date.month, current_date.day).isocalendar()
    

  @property
  def has_prev(self):
    return self.week > 1

  @property
  def has_next(self):
    return isoweek.Week(self.year, self.week) < isoweek.Week.last_week_of_year(self.year)

  def iter_pages(self, left_edge=52, left_current=3, middle = 26, right_limit=3):

    left_edge=self.page
    left_limit=3
    middle=(self.page)/2
    right_limit=3
    
    last = self.page + 1

    print last, left_edge, left_limit, middle, right_limit

    for num in xrange(self.page, 0, -1):
      if num >= left_edge - left_limit + 1 or \
        (num >= middle - 1 and \
        num <= middle + 1) or \
        num <= right_limit:

        if last - 1 != num:
          yield None
        
        yield num
        last = num

