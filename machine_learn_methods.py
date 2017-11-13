

def bernoulli_naive_bayes(): #69%
    from sklearn.naive_bayes import BernoulliNB
    return BernoulliNB(binarize=False)

def gaussian_naive_bayes(): #75%
    from sklearn.naive_bayes import GaussianNB
    return GaussianNB()

def svm( C= 1000.0, kernel = 'rbf'):
    from sklearn import svm
    return svm.SVC(C, kernel)

def decision_tree():
    from sklearn import tree
    return tree.DecisionTreeClassifier(min_samples_split=10)

def k_nearest_neighbours(n_neighbors = 2):
    from sklearn import neighbors
    return neighbors.KNeighborsClassifier(n_neighbors, weights='distance')

def random_forest_classifier(n_estimators=100):
    from sklearn.ensemble import RandomForestClassifier
    return RandomForestClassifier(n_estimators)

def adaboost(n_estimators=10):
    from sklearn.ensemble import AdaBoostClassifier
    return AdaBoostClassifier(n_estimators)

def k_means(num_clusters = 5):
    from sklearn.cluster import KMeans
    return KMeans(n_clusters=num_clusters, init='k-means++', max_iter=100, n_init=1)