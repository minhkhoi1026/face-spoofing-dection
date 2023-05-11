from typing import List
import torch
from torch import nn
from . import METRIC_REGISTRY
import numpy as np


@METRIC_REGISTRY.register()
class Accuracy:
    """
    Accuracy Score
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.threshold = kwargs.get('threshold') or 0.5
        self.reset()

    def update(self, preds, targets):
        """
        Perform calculation based on prediction and targets
        """
        preds = preds >= self.threshold
        preds = preds.detach().cpu().float()
        targets = targets.detach().cpu().float()
        self.preds += preds.numpy().tolist()
        self.targets += targets.numpy().tolist()

    def reset(self):
        self.targets = []
        self.preds = []

    def value(self):
        score = np.mean(np.array(self.targets) == np.array(self.preds))
        return {f"accuracy": score}
