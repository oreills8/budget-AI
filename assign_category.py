
from sklearn.model_selection import train_test_split
from prepare_feature_format import *
from machine_learn_methods import *
from Extract_Data import *
from sklearn.metrics import accuracy_score



available_models = ['k_means', 'adaboost', 'random_forest_classifier', 'k_nearest_neighbours', 'decision_tree',
                    'svm', 'gaussian_naive_bayes', 'bernoulli_naive_bayes']


def classify_categories(DF_features, DF_labels, classifier, return_input_vals=True, act='Actual Category', predict='Predicted Values'):

    clf,algo_type_supervised,fit_clf = return_clf_model(classifier)
    data_contains_text = isinstance(DF_features.ix[0, 0], basestring)
    outputDF = pd.DataFrame()
    print "preparing data for machine learning"

    test_train_split = .30 if algo_type_supervised else .0

    x_train, x_test, y_train, y_test = train_test_split(
        DF_features, DF_labels, test_size=test_train_split, random_state=17)

    predicted_values, output_features, output_labels = run_classification_model(x_train, y_train, x_test, y_test,
                                                                                data_contains_text, clf, classifier)
    if len(predicted_values)>0: outputDF = create_output_DF(outputDF, return_input_vals, predicted_values,
                                                                act, predict, output_features, output_labels)
    return outputDF


def run_classification_model(x_train, y_train, x_test, y_test, data_contains_text, clf, classifier_name):

    processed_x_train, processed_x_test = preprocessing(x_train, y_train, data_contains_text, x_test, y_test)

    predicted_values = fit_classification_model(clf, classifier_name, processed_x_train, y_train, processed_x_test, y_test)

    output_features = x_test if len(y_test)>0 else x_train
    output_labels = y_test if len(y_test)>0 else y_train

    return predicted_values,output_features,output_labels


def return_clf_model(classifier):
    print "running model : ", classifier
    algo_type_supervised = True
    fit_clf = True

    if classifier == available_models[0]:
        clf = k_means()
        algo_type_supervised = False
    elif classifier == available_models[1]:clf = adaboost()
    elif classifier == available_models[2]:clf = random_forest_classifier()
    elif classifier == available_models[3]:clf = k_nearest_neighbours()
    elif classifier == available_models[4]:clf = decision_tree()
    elif classifier == available_models[5]:clf = svm()
    elif classifier == available_models[6]:clf = gaussian_naive_bayes()
    elif classifier == available_models[7]:clf = bernoulli_naive_bayes()
    else:
        print "classifer %s not recognised" %classifier
        fit_clf = False
        print "available categories: "
        for model in available_models:
            print model
    return clf, algo_type_supervised, fit_clf


def fit_classification_model(clf,classifier_name, x_train, y_train, x_test, y_test):
    if len(y_test)>0:

        clf.fit(x_train, y_train)
        predicted_values = clf.predict(x_test)
        acc_score = accuracy_score(y_test, predicted_values) * 100
        print("accuracy of %s model is :  %f%%" % (classifier_name, acc_score))
    else:
        clf.fit(x_train)
        predicted_values = clf.labels_

    return predicted_values

# def print_feature_importance(self):
#     resultDF = pd.DataFrame()
#     resultDF['feature name'] = self.feature_names
#     resultDF['feature importance'] = self.importance
#     output_to_excel('output.xlsx','Sheet2',resultDF)


def create_output_DF(outputDF,return_input_vals,prediction_series,act,predict,features = [],labels_series=[]):

    if return_input_vals:
        try:
            for column in features.columns:
                outputDF.loc[:, column] = features.loc[:, column]
        except: outputDF.loc[:, 'feature'] = features
        outputDF.loc[:, act] = labels_series
    outputDF.loc[:, predict] = prediction_series
    return outputDF

