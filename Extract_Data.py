
import pandas as pd
import os

def extract_data (directoryPath):
    print "extracting data from", directoryPath
    bankData = pd.DataFrame()
    for root, dirs, files in os.walk(directoryPath, topdown=False):

        for name in files:
            filePath = os.path.join(root, name)
            bankDataTemp = pd.read_csv(filePath)
            bankData = bankData.append(bankDataTemp, ignore_index=True)
    if_date_convert_to_date_time(bankData)
    return bankData

def if_date_convert_to_date_time(DF):
    date_columns = DF.columns[DF.columns.astype(str).str.contains('Date')]
    for i in date_columns:
        DF[i] = pd.to_datetime(DF[i], format="%d/%m/%Y")
    return DF

def output_to_excel(filename,sheet, df):
    print "printing to file", filename
    writer = pd.ExcelWriter(filename)
    df.to_excel(writer, sheet)
    writer.save()