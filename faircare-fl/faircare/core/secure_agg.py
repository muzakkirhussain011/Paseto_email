import numpy as np


def mask_vector(vec, seed):
    rng = np.random.default_rng(seed)
    mask = rng.normal(size=vec.shape)
    return vec + mask, mask


def unmask_sum(masked_vecs, masks):
    return sum(masked_vecs) - sum(masks)
