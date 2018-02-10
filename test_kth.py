from pytest import fixture

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


