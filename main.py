
from BankData import BankData
from Data_visualisation import DataVis
from assign_category import *
from Extract_Data import *

directoryPath = 'C:\\Users\\soreil\\Documents\\budget project\\BankStatementData'

username = 'soreil'
api_key = 'nb6dtUWqoE0Ig0AmG6kn'

LlyodsCA = BankData(directoryPath)
Graphs = DataVis(username,api_key)

LlyodsCA.prepare_acc_data(True,'Date') #delete duplicates = true & sort by 'date'


#--print LlyodsCA.DF
#create summary charts for spending
#data, labels, title = LlyodsCA.spending_summary_by_category('Jan',2017,'Dec',2017)
#Graphs.pie_chart(data, labels, title)

#--time series chart
#DF_dictionary,title = LlyodsCA.spending_time_line('Jan',2017,'Dec',2017)
#Graphs.time_series_graph(DF_dictionary,title)

#--attempt at subplots
#Graphs.graph_all (data,labels,DF_dictionary)

#--learn categories
label_column = LlyodsCA.columns['Category']
#features_DF = LlyodsCA.DF[LlyodsCA.columns['Description']]
features_columns = [LlyodsCA.columns['Credit'],LlyodsCA.columns['Debit'],
                    LlyodsCA.columns['trans type id'],LlyodsCA.columns['Day'],
                    LlyodsCA.columns['week day id']]
features_DF = LlyodsCA.DF.loc[:, features_columns]

#-- unsupervised model

text_output = classify_categories(LlyodsCA.DF[LlyodsCA.columns['Description']],LlyodsCA.DF[label_column],'k_means',False)
#resultDF = text_output

features_DF.loc[:, 'text_clf'] = text_output.loc[:, text_output.columns[0]]
resultDF = classify_categories(features_DF,LlyodsCA.DF[label_column],'k_means')

#-- supervised model

#resultDF = classify_categories(LlyodsCA.DF[LlyodsCA.columns['Description']],LlyodsCA.DF[label_column],'svm')

#determineCategories.print_feature_importance()

#-- output
resultDF[LlyodsCA.columns['week day']] = LlyodsCA.DF[LlyodsCA.columns['week day']]
resultDF[LlyodsCA.columns['Type']] = LlyodsCA.DF[LlyodsCA.columns['Type']]
resultDF[LlyodsCA.columns['Description']] = LlyodsCA.DF[LlyodsCA.columns['Description']]

output_to_excel('output.xlsx','Sheet1',resultDF)



