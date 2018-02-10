from pytest import fixture
from itertools import islice

def _part(array):
    half = len(array) // 2
    left = array[:half]
    right = array[half:]
    return left, right

def _merge(k, left, right):
    ks = []
    li, ri = 0, 0
    if len(left) == 0:
        return right[:k]
    if len(right) == 0:
        return left[:k]
    for _ii in range(k):
        try:
            lv = left[li] 
        except IndexError:
            ks.extend(right[ri:k - len(ks)])
            return ks
        try:
            rv = right[ri] 
        except IndexError:
            ks.extend(left[li:k - len(ks)])
            return ks
        if lv < rv:
            ks.append(lv)
            li += 1
        else:
            ks.append(rv)
            ri += 1
    return ks

def ksmallest(k, data):
    """Return a list of the k smallest items in data.
    """
    if k >= len(data):
        return sorted(data)
    ll, rr = _part(data)
    return _merge(k, ksmallest(k, ll), ksmallest(k, rr))

def kth_smallest_item(k, data):
    """returns the kth smallest item in data.

    <k> counts like a person, i.e. is not zero-based
    """
    if len(data) < k:
        raise IndexError("there must be more data than k")
    else:
        return ksmallest(k, data)[k-1]


def _part_inplace(extent):
    start, stop = extent
    mid = (stop - start) // 2
    mid += start
    return (start, mid), (mid, stop)

def _merge_inplace(k, lindices, rindices, data):
    ks = []
    li, ri = 0, 0
    for ii in range(k):
        try:
            lidx = lindices[li]
        except IndexError:
            ks.extend(rindices[ri:ri+k-len(ks)])
            continue
        try:
            ridx = rindices[ri]
        except IndexError:
            ks.extend(lindices[li:li+k-len(ks)])
            continue

        if data[lidx] < data[ridx]:
            ks.append(lidx)
            li += 1
        else:
            ks.append(ridx)
            ri += 1
    return ks

def _ksmallest_inner(k, extent, data):
    span = extent[1] - extent[0]
    if span <= k:
        tmp = [(data[idx], idx) for idx in range(extent[0], extent[1])]
        tmp.sort()
        return [tt[1] for tt in tmp]
    else:
        lextent, rextent = _part_inplace(extent)
        return _merge_inplace(k, 
          _ksmallest_inner(k, lextent, data),
          _ksmallest_inner(k, rextent, data),
          data)

def ksmallest_inplace(k, data):
    extent = 0,len(data)
    idxs = _ksmallest_inner(k, extent, data)
    return [ data[ii] for ii in idxs]

@fixture 
def small_test():
    data = [100, 1, -7, 1000, 10000, 0, 12]
    return data

@fixture
def small_k():
    return 3

@fixture 
def small_test_result(small_test, small_k):
    tmp = sorted(small_test)
    return tmp[:small_k]

def test_merge():
    k = 5
    left = [ii for ii in range(5)]
    right = [ii for ii in range(5, 10)]
    assert _merge(k, left, right) == left
    k = 3
    assert _merge(k, left, right) == left[:k]

    k = 5
    left, right = right, left 
    assert _merge(k, left, right) == right
    k = 3
    assert _merge(k, left, right) == right[:k]

def test_merge_empty_arg():
    left = []
    right = [1,2,3,4,5,]
    assert _merge(3, left, right) == [1,2,3]
    assert _merge(7, left, right) == [1,2,3,4,5,]

    left = [1,2,3,4,5,]
    right = []
    assert _merge(3, left, right) == [1,2,3]
    assert _merge(7, left, right) == [1,2,3,4,5,]

    left = []
    right = []
    assert _merge(3, left, right) == []

def test_part():
    left, right = _part([1,2,3,4])
    assert left == [1,2,]
    assert right == [3,4,]

    left, right = _part([1,2,3,])
    assert left == [1,]
    assert right == [2,3,]

    left, right = _part([1,2,])
    assert left == [1,]
    assert right == [2,]

    left, right = _part([1,])
    assert left == []
    assert right == [1,]

def test_ksmalest_correctness(small_k, small_test, small_test_result):
    result = ksmallest(small_k, small_test)
    print(result)
    assert result == small_test_result

def test_kth_smallest_item(small_k, small_test, small_test_result):
    result = kth_smallest_item(small_k, small_test)
    expected = small_test_result[small_k-1]
    print("rcvd:{} expected:{}".format(result, expected))
    assert result == expected

def test_inplace_ksmallest(small_k, small_test, small_test_result):
    result = ksmallest_inplace(small_k, small_test)
    print(result)
    assert result == small_test_result

def test_inplace_merge(small_k, small_test, small_test_result):
    k = 5
    data = [1,2,3,4,5,6,7,8,9,10]
    lindices = [0,1,2,3,4]
    rindices = [5,6,7,8,9]
    assert _merge_inplace(k, lindices, rindices, data) == lindices
    k = 3
    assert _merge_inplace(k, lindices, rindices, data) == lindices[:k]

    data = [6,7,8,9,10,1,2,3,4,5,]
    lindices = [0,1,2,3,4]
    rindices = [5,6,7,8,9]
    k = 5
    assert _merge_inplace(k, lindices, rindices, data) == rindices
    k = 3
    assert _merge_inplace(k, lindices, rindices, data) == rindices[:k]


