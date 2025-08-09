from faircare.data.partition import dirichlet_partition

def test_partition_sizes():
    parts = dirichlet_partition(100, 5, alpha=0.5, seed=0)
    assert sum(len(p) for p in parts) == 100
    assert len(parts) == 5
