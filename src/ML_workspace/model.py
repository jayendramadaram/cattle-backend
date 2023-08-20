from enum import Enum
from ML_workspace import fcClassifier

classifiers = {
    "fcClassifier": fcClassifier
}

class Model(object):
    def __init__(self, fileId : str , classifierModel = "fcClassifier") -> None:
        self.model = classifiers[classifierModel]
    
    def predict(self):
        resp = self.model.Predict()
        return resp

    def __repr__(self) -> str:
        return "ALL SET"