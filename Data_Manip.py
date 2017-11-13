
def sort_by (DF, column, asending):
    DF = DF.sort_values(by=[column],ascending=asending)
    DF = DF.reset_index(drop=True)
    return DF

def remove_duplicates (DF):
    return DF.drop_duplicates()

#function which checks for null values in the provided list of columns
# if there are null values and the expectedNull value is set to false these are remove
# if there are null values and the expectedNull value is set to true these are updates to the expected value
# rows that are null for all provided columns are removed
def update_missing_values(DF,columns,newValue = None):
    if newValue is None:
        # remove columns with null values
        return DF.ix[:, columns].dropna()
    else:
        # remove rows that are null for both columns
        nullvaluesDF = DF[DF[columns[0]].isnull()]
        for i in range(1, len(columns)):
            nullvaluesDF = nullvaluesDF[nullvaluesDF[columns[i]].isnull()]
        DF = DF.drop(nullvaluesDF.index)
        # set null values
        return DF.ix[:, columns].fillna(newValue)


def add_column(DF,name,values):
    DF[name] = values
    return DF

def change_sign_of_series(series,sign):
    id = 0
    value = 1
    if sign == 'Positive':
        for data in series.iteritems():
            if data[value] < 0: series.loc[data[id]] = abs(data[value])
        return series
    elif sign == 'Negative':
        for data in series.iteritems():
            if data[value] > 0: series.loc[data[id]] = - data[value]
        return series
    else :
        print("Attempting to change series to unrecognised sign")
        return series

def return_column_in_DF_containing(DF, word):
    matchingColumns = [s for s in DF.columns if word in s]
    if len(matchingColumns) == 0:
        print('there are no columns that match the word' % word)
        return []
    if len(matchingColumns) == 1:
        return matchingColumns[0]
    else:
        print('There are more than one columns containing the word %s, columns include:' % word)
        for column in matchingColumns:
            print(column)
        return []

def return_DF_subset(DF, column, min, max):
    return DF[(DF[column] >= min) & (DF[column] <= max)]