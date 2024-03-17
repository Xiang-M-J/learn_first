def mergein(arr1, arr2):
    arr_ = []
    i,j = 0,0
    while i < len(arr1) and j < len(arr2):
        if arr1[i] <= arr2[j]:
            arr_.append(arr1[i])
            i += 1
        else:
            arr_.append(arr2[j])
            j += 1
    if i != len(arr1):
        arr_.extend(arr1[i:])
    if j != len(arr2):
        arr_.extend(arr2[j:])
    return arr_
            
def mergesort(arr):
    if len(arr) == 1:
        return arr
    # if len(arr) == 2:
    #     return [min(arr), max(arr)]
    mid = len(arr) // 2
    return mergein(mergesort(arr[:mid]), mergesort(arr[mid:]))

arr = [21,3,42,11,443,112,33,97]
arr1 = [12, 15, 17, 21]
arr2 = [3, 15, 20, 40, 41, 43]
# print(mergein(arr1, arr2))
print(mergesort(arr))
