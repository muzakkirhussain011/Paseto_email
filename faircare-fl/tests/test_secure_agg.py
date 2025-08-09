import numpy as np
from faircare.core.secure_agg import mask_vector, unmask_sum

def test_secure_sum():
    vecs = [np.array([1.0,2.0]), np.array([3.0,4.0])]
    masked = []
    masks = []
    for i,v in enumerate(vecs):
        mv, m = mask_vector(v, seed=i)
        masked.append(mv)
        masks.append(m)
    total = unmask_sum(masked, masks)
    assert np.allclose(total, sum(vecs))
