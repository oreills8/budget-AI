from time import time
from sklearn.decomposition import RandomizedPCA



def pca(x_train,x_test, n_components=10):

    print "Extracting the top %d features from %d transactions" % (n_components, x_train.shape[0])
    t0 = time()
    pca = RandomizedPCA(n_components=n_components, whiten=True).fit(x_train)
    print "done in %0.3fs" % (time() - t0)
    print "pca explained variance ratio", pca.explained_variance_ratio_
    x_train = pca.transform(x_train)
    if len(x_test) > 0 : x_test = pca.transform(x_test)
    return x_train, x_test

# def identify_powerful_features(self):
