import numpy as np

class FaceRotComp:
    def __init__(self, alpha=0.7):
        self.smooth_correction = 1
        self.alpha = alpha

    def calculate_correction(self, rex, lex, nosex, eyedist):
        l1 = np.abs(nosex - rex)
        l2 = np.abs(nosex - lex)

        A = np.abs(l1 - l2)/(l1 + l2)
        k = 0.15
        new_correction = 1 + A * k
        self.smooth_correction = self.alpha * new_correction + (1-self.alpha) * self.smooth_correction

    def get_correction(self):
        return self.smooth_correction