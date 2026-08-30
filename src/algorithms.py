import random

# Типы списков

def gen_rand(n):
    return [random.randint(0, n * 10) for _ in range(n)]

def gen_sort(n):
    return list(range(n))

def gen_rev(n):
    return list(range(n - 1, -1, -1))

def gen_a_sort(n, percent=0.05):
    lst = list(range(n))
    k = max(1, int(n * percent))
    ids = random.sample(range(n), k)
    vals = [lst[i] for i in ids]
    random.shuffle(vals)
    for i, idx in enumerate(ids):
        lst[idx] = vals[i]
    return lst

# Алгоритмы

def bubble_sort(arr): #https://www.geeksforgeeks.org/python/python-program-for-bubble-sort/
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break  
    return arr

def selection_sort(arr): #https://www.geeksforgeeks.org/python/python-program-for-selection-sort/
    size = len(arr)
    for ind in range(size - 1):
        min_index = ind

        for j in range(ind + 1, size):
            if arr[j] < arr[min_index]:
                min_index = j

        arr[ind], arr[min_index] = arr[min_index], arr[ind]
    return arr

def insertion_sort(arr): #https://www.geeksforgeeks.org/python/python-program-for-insertion-sort/
    n = len(arr)
    
    if n <= 1:
        return
    for i in range(1, n):
        key = arr[i]         
        j = i - 1
        while j >= 0 and key < arr[j]: 
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key 
    return arr

def quick_sort(arr, low=0, high=-1): #https://www.geeksforgeeks.org/dsa/python-program-for-quicksort/
    if high == -1:
        high = len(arr) - 1
    if low < high:
        #Random pivot
        rand_idx = random.randint(low, high)
        arr[rand_idx], arr[high] = arr[high], arr[rand_idx]

        p = partition(arr, low, high)
        quick_sort(arr, low, p - 1)
        quick_sort(arr, p + 1, high)
    return arr

def partition(arr, low, high): #https://www.geeksforgeeks.org/dsa/python-program-for-quicksort/
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

def merge_sort(arr, l=0, r=-1): #https://www.geeksforgeeks.org/python/python-program-for-merge-sort/
    if r == -1:
            r = len(arr) - 1
    if l < r:
        m = l + (r - l) // 2
        merge_sort(arr, l, m)
        merge_sort(arr, m + 1, r)
        merge(arr, l, m, r)
    return arr

def merge(arr, l, m, r): #https://www.geeksforgeeks.org/python/python-program-for-merge-sort/
    n1 = m - l + 1
    n2 = r - m

    L = [0] * n1
    R = [0] * n2

    for i in range(n1):
        L[i] = arr[l + i]
    for j in range(n2):
        R[j] = arr[m + 1 + j]

    i = j = 0
    k = l

    while i < n1 and j < n2:
        if L[i] <= R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1

    while i < n1:
        arr[k] = L[i]
        i += 1
        k += 1
    while j < n2:
        arr[k] = R[j]
        j += 1
        k += 1

def heap_sort(arr): #https://www.geeksforgeeks.org/dsa/python-program-for-heap-sort/
    n = len(arr)

    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]  # Swap max to end
        heapify(arr, i, 0)
    return arr

def heapify(arr, n, i): #https://www.geeksforgeeks.org/dsa/python-program-for-heap-sort/
    largest = i    
    l = 2 * i + 1    
    r = 2 * i + 2  

    if l < n and arr[l] > arr[largest]:
        largest = l

    if r < n and arr[r] > arr[largest]:
        largest = r

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)

def counting_sort(arr): #https://www.geeksforgeeks.org/python/python-program-for-counting-sort/
    max_val = max(arr)
    count = [0] * (max_val + 1)
    output = [0] * len(arr)

    for num in arr:
        count[num] += 1

    for i in range(1, len(count)):
        count[i] += count[i - 1]

    for num in reversed(arr):
        output[count[num] - 1] = num
        count[num] -= 1

    for i in range(len(arr)):
        arr[i] = output[i]

    return arr

def radix_sort(arr): #https://www.geeksforgeeks.org/python/python-program-for-radix-sort/
    max_num = max(arr)
    exp = 1  # Represents current digit place (1, 10, 100, ...)

    while max_num // exp > 0:
        n = len(arr)
        output = [0] * n
        count = [0] * 10  # For digits 0–9

        # Count occurrences of each digit
        for num in arr:
            index = (num // exp) % 10
            count[index] += 1

        # Convert count[] to actual positions
        for i in range(1, 10):
            count[i] += count[i - 1]

        # Build output array (in reverse for stability)
        for i in range(n - 1, -1, -1):
            index = (arr[i] // exp) % 10
            output[count[index] - 1] = arr[i]
            count[index] -= 1

        # Copy output to arr[]
        for i in range(n):
            arr[i] = output[i]

        exp *= 10
    return arr

def bucket_sort(arr): #https://www.geeksforgeeks.org/dsa/bucket-sort-in-python/
    n = len(arr)
    buckets = [[] for _ in range(n)]

    for num in arr:
        # Scale num to [0, n-1] based on max value
        bi = int((num / max(arr)) * (n - 1))
        # Safety clamp (due to floating point)
        bi = min(bi, n - 1)
        buckets[bi].append(num)

    # Sort individual buckets using insertion sort
    for bucket in buckets:
        insertion_sort(bucket)

    # Concatenate all buckets into arr[]
    index = 0
    for bucket in buckets:
        for num in bucket:
            arr[index] = num
            index += 1
    return arr
