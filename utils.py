import numpy as np


def gkern(l, sig, multi):
    """
    creates gaussian kernel with side length `l` and a sigma of `sig`
    """
    ax = np.linspace(-(l - 1) / 2., (l - 1) / 2., l)
    gauss = np.exp(-0.5 * np.square(ax) / np.square(sig))
    kernel = np.outer(gauss, gauss)
    return kernel / np.sum(kernel) * multi

def fdm_kern(D=24.192):
    kernel = D*np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]])
    return kernel
