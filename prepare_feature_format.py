

from time import time
from sklearn import decomposition
from sklearn.decomposition import RandomizedPCA
import pandas as pd
from nltk.corpus import stopwords
import nltk


def preprocessing(features_train,  labels_train, is_string=False, features_test = [], labels_test = [], feature_selection_precent=100):
    if is_string:
        print "running text processing"
        features_train = text_normalisation(features_train)
        if len(features_test) > 0: features_test = text_normalisation(features_test)
        features_train, features_test, feature_names = text_vectorisation(features_train, features_test)

        if feature_selection_precent < 100: features_train, features_test = feature_selection(features_train, features_test,
                                                                                              labels_train,labels_test,feature_selection_precent)
    else:
        features_train = feature_scaling(features_train)
        if len(features_test) > 0: features_test = feature_scaling(features_test)
        features_train, features_test = pca(features_train, features_test, 4) # TODO: 4
    return features_train, features_test

def pca(x_train,x_test, n_components=10):

    print "Extracting the top %d features from %d transactions" % (n_components, x_train.shape[0])
    t0 = time()
    pca = decomposition.PCA(n_components=n_components, whiten=True).fit(x_train)
    print "done in %0.3fs" % (time() - t0)
    print "pca explained variance ratio", pca.explained_variance_ratio_
    x_train = pca.transform(x_train)
    if len(x_test) > 0 : x_test = pca.transform(x_test)
    return x_train, x_test

def text_normalisation(text_df):
    text_df = text_df.map(lambda x: x.lstrip('+-').rstrip('_/*@&-'))
    text_df = text_df.str.replace('\d+', '')
    return text_df


def text_vectorisation (features_train, features_test):
    ### text vectorization--go from strings to lists of numbers
    from sklearn.feature_extraction.text import TfidfVectorizer
    #sw = stopwords.words('english')
    #print "number of stopwords in corpus ",len(sw)
    vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5,
                                     stop_words='english')
    features_train_transformed = vectorizer.fit_transform(features_train)
    if len(features_test)>0: features_test_transformed = vectorizer.transform(features_test)
    else: features_test_transformed = features_test
    feature_names = vectorizer.get_feature_names()
    return features_train_transformed, features_test_transformed, feature_names



def feature_selection (features_train, features_test, labels_train,  labels_test, percent):
    from sklearn.feature_selection import SelectPercentile, f_classif
    ### feature selection, because text is high dimensional and can be really computationally intensive as a result
    selector = SelectPercentile(f_classif, percentile=percent)
    selector.fit(features_train, labels_train)
    features_train_transformed = selector.transform(features_train)
    if len(features_test) > 0: features_test_transformed = selector.transform(features_test)
    else: features_test_transformed = features_test
    return features_train_transformed, features_test_transformed


def feature_scaling(features):
    # -- feature scaling
    from sklearn.preprocessing import MinMaxScaler
    scaler = MinMaxScaler()
    return scaler.fit_transform(features)

