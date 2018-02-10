import time
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

def average_function_duration(x, fn):
    start = time.time()
    for ii in range(x):
        fn()
    stop = time.time()
    return (stop-start)/x

def main():
    input = list(range(1000000))
    #output = ksmallest_inplace(5, input)
    #output = ksmallest_inplace(5, input)
    #print(output)

    trial_size = 4
    t1 = average_function_duration(trial_size, lambda:ksmallest(5, input))
    print("copying version averaged {}".format(t1))
    #t2 = average_function_duration(trial_size, lambda:ksmallest_inplace(5, input))
    #print("inplace version averaged {}".format(t2))

if __name__ == '__main__':
    main()
