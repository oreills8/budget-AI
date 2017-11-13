
import datetime
import calendar
from dateutil.rrule import rrule, MONTHLY

def datetime_from_string(str):
    return datetime.datetime.strptime(str, "%d/%m/%Y")

def month_num_from_month_name(month):
    if len(month) < 4 :
        #abbriviated month
        abbr_to_num = {name: num for num, name in enumerate(calendar.month_abbr) if num}
        return abbr_to_num[month]
    else :
        abbr_to_num = {name: num for num, name in enumerate(calendar.month) if num}
        return abbr_to_num[month]


def month_name_from_date(date):
    return date.strftime("%b")

def return_dates(startMonth, startyear, minDate, endMonth=None, endyear=None, maxDate=None):
    startMonthNum = month_num_from_month_name(startMonth)
    date_range = calendar.monthrange(startyear, startMonthNum)
    startDate = datetime_from_string('%d/%d/%d' % (1, startMonthNum, startyear))
    #check if date is before first transaction
    if startDate < minDate:
        print(
            "Input Date of %s preceeds the first transaction recorded. Outputing for first transaction recorded of %s"
            % (str(startDate), str(minDate)))
        startDate = minDate

    if endMonth is None:
        endDate = datetime_from_string('%d/%d/%d' % (date_range[1], startMonthNum, startyear))
    else:
        endMonthNum = month_num_from_month_name(endMonth)
        date_range = calendar.monthrange(endyear, endMonthNum)
        endDate = datetime_from_string('%d/%d/%d' % (date_range[1], endMonthNum, endyear))
        # check if date is after last transaction
        if endDate > maxDate:
            print(
            "Input Date of %s exceeds the last transaction recorded. Outputing for last transaction recorded of %s"
            % (endDate.strftime("%B %d, %Y"), maxDate.strftime("%B %d, %Y")))
            endDate = maxDate

    return startDate, endDate
