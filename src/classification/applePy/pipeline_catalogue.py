from mne.decoding import CSP as MNE_CSP

from pyriemann.estimation import Covariances, XdawnCovariances, CospCovariances, HankelCovariances
from pyriemann.classification import MDM
from pyriemann.tangentspace import TangentSpace, FGDA
from pyriemann.channelselection import ElectrodeSelection as pyriemannElectrodeSelection
from pyriemann.spatialfilters import Xdawn, CSP

from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression

from classification.applePy.channel_selection import ElectrodeSelectionRaw
from classification.applePy.tools import DownSampler, EpochsVectorizer, CospBoostingClassifier, PSDfiltering

CONST_DEFAULT_RANDOMIZEDSEARCH_NBITER = 10


class Pipeline_catalogue:
    """
    Pipeline catalogue is mainly composed of the catalogue and the parameters to fit.
    The catalogue contains 12 pre-made pipelines, and the parameters to fit contains, for each pipeline,
    the different parameters that should be tested in order to obtain better results.
    """
    def __init__(self, used_pipeline=None, channels_selected=False):
        self.XDAWN_filters = [1, 3, 5]
        self.down_filters = [1, 2, 5, 10]
        self.csp_filters = [1, 3, 5]
        self.nb_elec = [5, 10, 20]
        self.catalogue = {}
        self.parameters_to_fit = {}

        if used_pipeline is None:   # Use all pipelines
            used_pipeline = ['XdawnCovTSLR', 'XdawnCov', 'Xdawn', 'CSP', 'CSP2', 'cov', 'Cosp', 'HankelCov', 'CSSP',
                             'PSD', 'MDM', 'FgMDM']
        for pipeline in used_pipeline:
            if pipeline == 'XdawnCovTSLR':
                self.catalogue['XdawnCovTSLR'] = make_pipeline(XdawnCovariances(3, estimator='oas', xdawn_estimator='oas'),
                                                               TangentSpace('riemann'),
                                                               LogisticRegression('l2', solver='liblinear'))
                self.parameters_to_fit["XdawnCovTSLR"] = [1, {"xdawncovariances__nfilter": self.XDAWN_filters}]
            elif pipeline == 'XdawnCov':
                self.catalogue['XdawnCov'] = make_pipeline(XdawnCovariances(3, estimator='oas', xdawn_estimator='oas'),
                                                           MDM(metric=dict(mean='riemann', distance='riemann')))
                self.parameters_to_fit["XdawnCov"] = [1, {"xdawncovariances__nfilter": self.XDAWN_filters}]
            elif pipeline == 'Xdawn':
                self.catalogue['Xdawn'] = make_pipeline(Xdawn(12, estimator='oas'), DownSampler(5), EpochsVectorizer(),
                                                        LogisticRegression('l2', solver='liblinear'))
                self.parameters_to_fit["Xdawn"] = [1, {"xdawn__nfilter": self.XDAWN_filters,
                                                       "downsampler__factor": self.down_filters}]
            elif pipeline == 'CSP':
                self.catalogue['CSP'] = make_pipeline(Xdawn(12, estimator='oas'), MNE_CSP(8, reg='shrinkage'),
                                                      LogisticRegression('l2', solver='liblinear'))
                self.parameters_to_fit["CSP"] = [1, {"xdawn__nfilter": self.XDAWN_filters,
                                                     "csp__n_components": self.csp_filters}]
            elif pipeline == 'CSP2':
                if not channels_selected:
                    self.catalogue['CSP2'] = make_pipeline(ElectrodeSelectionRaw(10), MNE_CSP(8, reg='shrinkage'),
                                                           LogisticRegression('l2', solver='liblinear'))
                else:
                    self.catalogue['CSP2'] = make_pipeline(MNE_CSP(8, reg='shrinkage'),
                                                           LogisticRegression('l2', solver='liblinear'))
                if "electrodeselectionraw" in self.catalogue['CSP2'].named_steps:
                    self.parameters_to_fit["CSP2"] = [1, {"electrodeselectionraw__nelec": self.nb_elec,
                                                          "csp__n_components": self.csp_filters}]
                else:
                    self.parameters_to_fit["CSP2"] = [1, {"csp__n_components": self.csp_filters}]
            # Induced activity models
            elif pipeline == 'cov':
                if not channels_selected:
                    self.catalogue['cov'] = make_pipeline(Covariances("oas"), pyriemannElectrodeSelection(10),
                                                          TangentSpace('riemann'),
                                                          LogisticRegression('l1', solver='liblinear'))
                else:
                    self.catalogue['cov'] = make_pipeline(Covariances("oas"), TangentSpace('riemann'),
                                                          LogisticRegression('l1', solver='liblinear'))
                if "electrodeselection" in self.catalogue['cov'].named_steps:
                    self.parameters_to_fit["cov"] = [1, {"electrodeselection__nelec": self.nb_elec}]
                else:
                    self.parameters_to_fit["cov"] = [0]
            elif pipeline == 'Cosp':
                self.catalogue['Cosp'] = make_pipeline(CospCovariances(fs=512, window=32, overlap=0.75, fmax=300, fmin=1),
                                                       CospBoostingClassifier(self.catalogue['cov']))
                self.parameters_to_fit["Cosp"] = [0]
            elif pipeline == 'HankelCov':
                self.catalogue['HankelCov'] = make_pipeline(DownSampler(2),
                                                            HankelCovariances(delays=[2, 4, 8, 12, 16], estimator='oas'),
                                                            TangentSpace('logeuclid'),
                                                            LogisticRegression('l1', solver='liblinear'))
                self.parameters_to_fit["HankelCov"] = [1, {"downsampler__factor": self.down_filters}]
            elif pipeline == 'CSSP':
                self.catalogue['CSSP'] = make_pipeline(HankelCovariances(delays=[2, 4, 8, 12, 16], estimator='oas'),
                                                       CSP(30), LogisticRegression('l1', solver='liblinear'))
                self.parameters_to_fit["CSSP"] = [1, {"csp__nfilter": self.csp_filters}]
            # Additional pipelines
            elif pipeline == 'PSD':
                self.catalogue['PSD'] = make_pipeline(PSDfiltering(), LogisticRegression())
                self.parameters_to_fit["PSD"] = [0]
            elif pipeline == 'MDM':
                self.catalogue['MDM'] = make_pipeline(Covariances("oas"), MDM(metric=dict(mean='riemann', distance='riemann')))
                self.parameters_to_fit["MDM"] = [0]
            elif pipeline == 'FgMDM':
                self.catalogue['FgMDM'] = make_pipeline(Covariances("oas"), FGDA(),
                                                        MDM(metric=dict(mean='riemann', distance='riemann')))
                self.parameters_to_fit["FgMDM"] = [0]

    def modify_add_pipeline(self, name, pipeline, parameters):
        """
        Allows the user to add their own pipeline to the available catalogue, or to modify a pipeline (for example, using their own
        hyper-values for a pipeline, such as the number of electrodes to select, of CSP filters, of xDAWN filters, etc...).
        Code  : 0 = no need to tune
                1 = Grid Search
                2 = Randomized Search
        if grid search : parameters = [1, [,,,]]
        if randomized search : parameters = [2, [,,,], nb_iter*]

        Parameters
        ----------
        name :  string
                name of the pipeline
        pipeline :  instance of pipeline
                    the pipeline to be used
        parameters :    see above
                    the notation for the parameters to fit
        """
        self.catalogue[name] = pipeline
        if (parameters[0] == 2) and (len(parameters) == 2):
            parameters.append(CONST_DEFAULT_RANDOMIZEDSEARCH_NBITER)
        self.parameters_to_fit[name] = parameters

    def delete_pipeline(self, name):
        """
        Deletes a pipeline and the pipeline's parameters to fit.
        Parameters
        ----------
        name :  string
                name of the pipeline
        """
        if name not in self.catalogue.keys():
            text = "Pipeline " + name + " does not exist."
            raise Exception(text)
        del self.catalogue[name]
        del self.parameters_to_fit[name]

    def modify_parameters(self, name, parameters):
        """
        Replaces the old parameters for a pipeline by new ones.
        Parameters
        ----------
        name :  string
                name of the pipeline
        parameters :    see modify_pipeline
                        the notation for the parameters to fit
        """
        if name not in list(self.catalogue.keys()):
            text = "Pipeline " + name + " does not exist."
            raise Exception(text)

        self.parameters_to_fit[name] = parameters

    def change_logReg(self, new_classifier, channels_selected=None):
        self.catalogue['XdawnCovTSLR'] = make_pipeline(XdawnCovariances(3, estimator='oas', xdawn_estimator='oas'),
                                                       TangentSpace('riemann'), new_classifier)
        self.catalogue['Xdawn'] = make_pipeline(Xdawn(12, estimator='oas'), DownSampler(5), EpochsVectorizer(),
                                                new_classifier)
        self.catalogue['CSP'] = make_pipeline(Xdawn(12, estimator='oas'), MNE_CSP(8, reg='shrinkage'), new_classifier)

        if not channels_selected:
            self.catalogue['CSP2'] = make_pipeline(ElectrodeSelectionRaw(10), MNE_CSP(8, reg='shrinkage'),
                                                   new_classifier)
        else:
            self.catalogue['CSP2'] = make_pipeline(MNE_CSP(8, reg='shrinkage'), new_classifier)

        # Induced activity models
        if not channels_selected:
            self.catalogue['cov'] = make_pipeline(Covariances("oas"), pyriemannElectrodeSelection(10),
                                                  TangentSpace('riemann'), new_classifier)
        else:
            self.catalogue['cov'] = make_pipeline(Covariances("oas"), TangentSpace('riemann'), new_classifier)

        self.catalogue['HankelCov'] = make_pipeline(DownSampler(2),
                                                    HankelCovariances(delays=[2, 4, 8, 12, 16], estimator='oas'),
                                                    TangentSpace('logeuclid'), new_classifier)
        self.catalogue['CSSP'] = make_pipeline(HankelCovariances(delays=[2, 4, 8, 12, 16], estimator='oas'),
                                               CSP(30), new_classifier)
