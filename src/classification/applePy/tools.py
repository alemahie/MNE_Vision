import numpy as np

from copy import deepcopy

from sklearn.base import BaseEstimator, TransformerMixin

from scipy.signal import welch


class DownSampler(BaseEstimator, TransformerMixin):
    """
    Downsample transformer.
    Source from Cédric Simar.
    """
    def __init__(self, factor=4):
        self.factor = factor

    def fit(self, X, y):
        return self

    def transform(self, X):
        return X[:, :, ::self.factor]


class EpochsVectorizer(BaseEstimator, TransformerMixin):
    """
    Vectorize epochs.
    Source from Cédric Simar.
    """
    def __init__(self):
        pass

    def fit(self, X, y):
        return self

    def transform(self, X):
        X2 = np.array([x.flatten() for x in X])
        return X2


class CospBoostingClassifier(BaseEstimator, TransformerMixin):
    """
    Co-spectral matrix bagging.
    Source from Cédric Simar.
    """
    def __init__(self, baseclf):
        self.baseclf = baseclf
        self.clfs_ = []

    def fit(self, X, y):
        for i in range(X.shape[-1]):
            clf = deepcopy(self.baseclf)
            self.clfs_.append(clf.fit(X[:, :, :, i], y))
        return self

    def predict_proba(self, X):
        proba = []
        for i in range(X.shape[-1]):
            proba.append(self.clfs_[i].predict_proba(X[:, :, :, i]))
        proba = np.mean(proba, axis=0)
        return proba

    def transform(self, X):
        proba = []
        for i in range(X.shape[-1]):
            proba.append(self.clfs_[i].predict_proba(X[:, :, :, i]))
        proba = np.concatenate(proba, 1)
        return proba


class PSDfiltering(BaseEstimator, TransformerMixin):
    """
    Power Spectral Density class.
    Code inspired from Cédric Simar.
    """
    def __init__(self, frequencies=np.array([[1, 4], [4, 8], [8, 15], [15, 20], [30, 40]]), sampling_freq=512,
                 overlap=0.25):
        self.frequencies = frequencies
        self.sampling_freq = sampling_freq
        self.overlap = overlap

    def fit(self, X, y):
        return self

    def compute_power_spectral_density(self, windowed_signal, psd_freqs, sampling_freq, overlap):
        """
        Compute the PSD of each 32 electrodes and form a binned spectrogram of 5 frequency bands.
        Return the log_10 on the 32 spectrogram.
        """
        # Windowed signal of shape (9 x 513)
        n_electrodes = windowed_signal.shape[0]
        ret = np.empty((psd_freqs.shape[0], n_electrodes), dtype=np.float32)

        # Welch parameters
        sliding_window = sampling_freq
        n_overlap = int(sliding_window * overlap)

        # compute psd using Welch method
        freqs, power = welch(windowed_signal, fs=sampling_freq, nperseg=sliding_window, noverlap=n_overlap)
        for i, psd_freq in enumerate(psd_freqs):
            tmp = (freqs >= psd_freq[0]) & (freqs < psd_freq[1])
            ret[i] = power[:, tmp].mean(1)
        return np.log(ret)

    def transform(self, X):
        psd_frequencies = []
        for epoch in X:
            signal_psd = self.compute_power_spectral_density(epoch, self.frequencies, self.sampling_freq, self.overlap)
            signal_psd = np.ndarray.flatten(signal_psd)
            psd_frequencies.append(signal_psd)
        psd_frequencies = np.asarray(psd_frequencies)
        return psd_frequencies


def source_estimation():
    return None