"""Code for channel selection."""

import numpy as np

from pyriemann.utils.distance import distance
from pyriemann.classification import MDM
from pyriemann.tangentspace import TangentSpace
from pyriemann.estimation import Covariances

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression


class ElectrodeSelection(BaseEstimator, TransformerMixin):
    """Channel selection based on a Riemannian geometry criterion. \n

    For each class, a centroid is estimated, and the channel selection is based
    on the maximization of the distance between centroids. This is done by a
    backward elimination where the electrode that carries the less distance is
    removed from the subset at each iteration.
    This algorithm is described in [1].

    Parameters \n
    ---------- \n
    nelec : int (default 16) \n
        the number of electrode to keep in the final subset. \n
    metric : string | dict (default: 'riemann') \n
        The type of metric used for centroid and distance estimation. 
        see `mean_covariance` for the list of supported metric. 
        the metric could be a dict with two keys, `mean` and `distance` in
        order to pass different metric for the centroid estimation and the
        distance estimation. Typical usecase is to pass 'logeuclid' metric for
        the mean in order to boost the computional speed and 'riemann' for the
        distance in order to keep the good sensitivity for the selection. \n
    n_jobs : int, (default: 1) \n
        The number of jobs to use for the computation. This works by computing
        each of the class centroid in parallel.
        If -1 all CPUs are used. If 1 is given, no parallel computing code is
        used at all, which is useful for debugging. For n_jobs below -1,
        (n_cpus + 1 + n_jobs) are used. Thus for n_jobs = -2, all CPUs but one
        are used. \n

    Attributes \n
    ---------- \n
    covmeans_ : list \n
        the class centroids. \n
    dist_ : list \n
        list of distance at each interaction. \n

    References
    ----------
    [1] A. Barachant and S. Bonnet, "Channel selection procedure using
    riemannian distance for BCI applications," in 2011 5th International
    IEEE/EMBS Conference on Neural Engineering (NER), 2011, 348-351
    """
    def __init__(self, nelec=16, metric='riemann', n_jobs=1):
        self.nelec = nelec
        self.metric = metric
        self.n_jobs = n_jobs
        self.mdm = MDM(metric=self.metric, n_jobs=self.n_jobs)
        self.pipeline = make_pipeline(TangentSpace('riemann'), LogisticRegression('l2'))

        self.covmeans_ = None
        self.dist_ = []
        self.subelec_ = None

    def fit(self, X, y=None, sample_weight=None):
        """Find the optimal subset of electrodes. \n

        Parameters \n
        ---------- \n
        X : ndarray, shape (n_trials, n_channels, n_channels) \n
            ndarray of SPD matrices. \n
        y : ndarray shape (n_trials, 1) \n
            labels corresponding to each trial. \n
        sample_weight : None | ndarray shape (n_trials, 1) \n
            the weights of each sample. if None, each sample is treated with 
            equal weights. \n

        Returns \n
        ------- \n
        self : ElectrodeSelection instance \n
            The ElectrodeSelection instance. \n
        """
        self.mdm.fit(X, y, sample_weight=sample_weight)
        self.covmeans_ = self.mdm.covmeans_

        Ne, _ = self.covmeans_[0].shape
        self.subelec_ = list(range(0, Ne, 1))

        while (len(self.subelec_)) > self.nelec:
            di = np.zeros((len(self.subelec_), 1))
            for idx in range(len(self.subelec_)):
                sub = self.subelec_[:]
                sub.pop(idx)
                di[idx] = 0
                for i in range(len(self.covmeans_)):
                    for j in range(i + 1, len(self.covmeans_)):
                        di[idx] += distance(self.covmeans_[i][:, sub][sub, :], self.covmeans_[j][:, sub][sub, :],
                                            metric=self.mdm.metric_dist)
            torm = di.argmax()
            self.dist_.append(di.max())
            self.subelec_.pop(torm)

        X = self.transform(X)
        self.pipeline.fit(X, y)
        return self

    def transform(self, X):
        """Return reduced matrices. \n

        Parameters \n
        ---------- \n
        X : ndarray, shape (n_trials, n_channels, n_channels) \n
            ndarray of SPD matrices. \n

        Returns \n
        ------- \n
        covs : ndarray, shape (n_trials, n_elec, n_elec) \n
            The covariances matrices after reduction of the number of channels. \n
        """
        return X[:, self.subelec_, :][:, :, self.subelec_]

    def score(self, estimator, x_test, y_test):
        x_test = self.transform(x_test)
        score = 0
        predictions = self.pipeline.predict(x_test)
        for i in range(y_test.shape[0]):
            if predictions[i] == y_test[i]:
                score += 1
        score = score/y_test.shape[0]
        return score


class ElectrodeSelectionRaw(BaseEstimator, TransformerMixin):
    def __init__(self, nelec=16, metric='riemann', n_jobs=1):
        """Init."""
        self.nelec = nelec
        self.metric = metric
        self.n_jobs = n_jobs
        self.mdm = MDM(metric=self.metric, n_jobs=self.n_jobs)

        self.covmeans_ = None
        self.dist_ = []
        self.subelec_ = None

    def fit(self, X, y=None, sample_weight=None):
        """Find the optimal subset of electrodes.
        """
        cov = Covariances("oas")
        X = cov.transform(X)
        self.mdm.fit(X, y, sample_weight=sample_weight)
        self.covmeans_ = self.mdm.covmeans_

        Ne, _ = self.covmeans_[0].shape
        self.subelec_ = list(range(0, Ne, 1))

        while (len(self.subelec_)) > self.nelec:
            di = np.zeros((len(self.subelec_), 1))
            for idx in range(len(self.subelec_)):
                sub = self.subelec_[:]
                sub.pop(idx)
                di[idx] = 0
                for i in range(len(self.covmeans_)):
                    for j in range(i + 1, len(self.covmeans_)):
                        di[idx] += distance(self.covmeans_[i][:, sub][sub, :], self.covmeans_[j][:, sub][sub, :],
                                            metric=self.mdm.metric_dist)
            torm = di.argmax()
            self.dist_.append(di.max())
            self.subelec_.pop(torm)

        X = self.transform(X)

        return self

    def transform(self, X):
        """Return reduced matrices.
        """
        return X[:, self.subelec_, :]
