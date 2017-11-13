import calendar

import pandas as pd
import numpy as np
from Extract_Data import *
from Data_Manip import *
from Date_Manip import *

class BankData:

    def __init__(self, directoryPath=None):

        if directoryPath is None:
            self.DF = pd.DataFrame()
        else:
            self.DF = extract_data(directoryPath)
            print "creating dataframe for bank data"
            self.columns = {'month':'month','week day':'week day','week day id':'week day id',
                            'Category':'Category','spending':'spending', 'trans type id':'trans type id',
                            'Day': 'Day'}

            self.columns['Debit'] = return_column_in_DF_containing(self.DF, 'Debit')
            self.columns['Credit'] = return_column_in_DF_containing(self.DF, 'Credit')
            self.columns['Date'] = return_column_in_DF_containing(self.DF, 'Date')
            self.columns['Balance'] = return_column_in_DF_containing(self.DF, 'Balance')
            self.columns['Description'] = return_column_in_DF_containing(self.DF, 'Description')
            self.columns['Type'] = return_column_in_DF_containing(self.DF, 'Transaction Type')
            self.col_list_for_category_analysis =['Transaction Type','Sort Code','Account Number','Transaction Description','Debit Amount','Credit Amount','week day']
            self.category_list = self.bank_data_categories()
            self.transaction_type_list = []


    def bank_data_categories(self):
        DF =  self.DF.groupby(self.DF[self.columns['Category']])
        return DF.groups.keys()

    def printself(self):
        print('Printing : Bank Data')
        print(self.DF)

    def prepare_acc_data(self,preformDataChecks, sortValue):
        self.DF = remove_duplicates(self.DF)
        if preformDataChecks: self.performDataChecks()
        sortColumn = return_column_in_DF_containing(self.DF,sortValue)
        self.DF = sort_by(self.DF,sortColumn , True)
        self.add_week_day_to_DF()
        self.add_month_to_DF()
        self.add_spending_column()
        self.add_transaction_type_num()
        self.add_date_integer_column()

    def performDataChecks(self):
        # remove values with null in credit and debit amount
        # & set the remaining values in each column to 0
        self.DF.ix[:, [self.columns['Credit'],self.columns['Debit']]] = update_missing_values(self.DF, [self.columns['Credit'],self.columns['Debit']], 0.00)
        #for all remaining columns remove any null values
        remaining_columns = self.DF.drop([self.columns['Credit'],self.columns['Debit']], axis = 1).columns
        self.DF.ix[:, remaining_columns] = update_missing_values(self.DF, remaining_columns)

    def add_spending_column(self):
        print "adding a spending column"
        spendingSeries = self.DF.ix[:,self.columns['Debit']] - self.DF.ix[:,self.columns['Credit']]
        spendingSeries[spendingSeries < 0] = 0  # only include spending
        self.DF = add_column(self.DF, self.columns['spending'], spendingSeries)


    def add_transaction_type_num(self):
        print "adding transaction type column"
        self.transaction_type_list = list(np.unique(self.DF[self.columns['Type']].values))
        self.DF[self.columns['trans type id']] = [self.transaction_type_list.index(x) for x in self.DF[self.columns['Type']].values]

    def add_date_integer_column(self):
        print "adding date as an integer in a column"
        self.DF[self.columns['Day']] = pd.DatetimeIndex(self.DF[self.columns['Date']]).day


    def add_week_day_to_DF(self):
        print "adding a weekday column"
        weekday_series = []
        weekday_num_series = []
        for date in self.DF[self.columns['Date']]:
            weekday_num_series.append(date.weekday())
            weekday_series.append(calendar.day_name[date.weekday()])
        self.DF = add_column(self.DF,self.columns['week day'],weekday_series)
        self.DF = add_column(self.DF, self.columns['week day id'], weekday_num_series)

    def add_amount_to_DF(self):
        print "adding amount column"
        amount_series = self.DF[self.columns['Credit']] + self.DF[self.columns['Debit']]
        self.DF = add_column(self.DF, self.columns['amount'], amount_series)

    def add_month_to_DF(self):
        print "adding a month column"
        dateseries = self.DF[self.columns['Date']]
        self.DF[self.columns['month']] = dateseries.apply(lambda dt: dt.replace(day=1))

    def bankdata_subset_for_time_horizon(self, startMonth, startyear, endMonth = None, endyear = None):
        print "preparing an object for the time frame %s-%s to %s-%s" %(startMonth, startyear, endMonth, endyear)
        minDate = self.DF[self.columns['Date']].min()
        maxDate = self.DF[self.columns['Date']].max()

        if endMonth is None: startDate, endDate = return_dates(startMonth, startyear, minDate)
        else:
            if endyear is None: endyear = startyear
            startDate, endDate = return_dates(startMonth, startyear, minDate, endMonth, endyear, maxDate)

        outputDF = return_DF_subset(self.DF, self.columns['Date'], startDate, endDate)
        return outputDF

    def spending_summary_by_category(self, startMonth, startyear, endMonth=None, endyear=None):
        print "calculating average spending pre category"
        summaryDF = self.bankdata_subset_for_time_horizon(startMonth, startyear, endMonth, endyear)
        minDate = summaryDF[self.columns['Date']].min()
        maxDate = summaryDF[self.columns['Date']].max()
        title = 'Average Spending from %s to %s' % (
            minDate.strftime("%B %d, %Y"), maxDate.strftime("%B %d, %Y"))
        summaryDF = summaryDF.groupby(summaryDF[self.columns['Category']])
        summaryDF = summaryDF[self.columns['spending']].mean()
        return summaryDF.values, summaryDF.keys(), title

    def spending_time_line(self, startMonth, startyear, endMonth=None, endyear=None):
        print "creating spending time line"
        summaryDF = self.bankdata_subset_for_time_horizon(startMonth, startyear, endMonth, endyear)
        minDate = summaryDF[self.columns['Date']].min()
        maxDate = summaryDF[self.columns['Date']].max()
        title = 'Spending Timeline %s to %s' % (
            minDate.strftime("%B %d, %Y"), maxDate.strftime("%B %d, %Y"))
        summaryByCategory = {}
        for category in self.category_list:
            DF = summaryDF[summaryDF[self.columns['Category']] == category]
            if DF.size > 0 :
                DF = DF.groupby(summaryDF[self.columns['month']])
                DF = DF[self.columns['spending']].sum()
                summaryByCategory[category] = DF

        return summaryByCategory, title

