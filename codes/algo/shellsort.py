def shellsort(arr):
    k = len(arr) // 2
    while k >= 1:
        for i in range(len(arr)-k):
            if arr[i] > arr[i+k]:
                arr[i], arr[i+k] = arr[i+k], arr[i]
        k -= 1
    return arr

arr = [13, 8, 27, 19, 78, 57, 99, 33]
print(shellsort(arr))
