from typing import Any



def bubble_sort(arr: Any) -> Any:
    # PERFORMANCE ISSUE: O(n²) algorithm
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

def linear_search(arr: Any, target: Any) -> Any:
    # PERFORMANCE ISSUE: O(n) when binary search possible
    for i, val in enumerate(arr):
        if val == target:
            return i
    return -1

def duplicate_finder(arr: Any) -> Any:
    # PERFORMANCE ISSUE: O(n²)
    duplicates = []
    for i in range(len(arr)):
        for j in range(i+1, len(arr)):
            if arr[i] == arr[j] and arr[i] not in duplicates:
                duplicates.append(arr[i])
    return duplicates
