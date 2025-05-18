import tkinter as tk
# from tkinter import ttk
import random
from collections import deque
from typing import Any, Generator
from math import log2, factorial

# --- BubbleSort ---
def bubbleSort(arr: list[int]) -> Generator[list[int], Any, None]:
    for i in range(len(arr) - 1):
        for j in range(len(arr) - i - 1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                yield arr[:]

# --- InsertSort ---
def insertSort(arr: list[int]) -> Generator[list[int], Any, None]:
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1

        while j >= 0 and arr[j] > key:
            arr[j+1] = arr[j]
            j -= 1
            yield arr[:]

        arr[j+1] = key
        yield arr[:]

# --- QuickSort ---
def partition(a: list[int], lo: int, hi: int) -> int:
    pivot = a[hi]
    i = lo
    for j in range(lo, hi):
        if a[j] <= pivot:
            a[i], a[j] = a[j], a[i]
            i += 1
    a[i], a[hi] = a[hi], a[i]
    return i

def quickSort(arr: list[int]) -> Generator[list[int], Any, None]:
    if len(arr) < 2:
        return

    stack: list[tuple[int, int]] = [(0, len(arr) - 1)]
    while stack:
        lo, hi = stack.pop()
        if lo >= hi:
            continue

        p = partition(arr, lo, hi)
        yield arr[:]

        left  = (lo, p - 1)
        right = (p + 1, hi)
        if (left[1] - left[0]) > (right[1] - right[0]):
            stack.append(left)
            stack.append(right)
        else:
            stack.append(right)
            stack.append(left)

# --- Second QuickSort ---
def quickSort_Partitions(arr: list[int], i: int, j: int) -> list[int]:
    if i < j:
        pivot = classic_partitions(arr, i, j)

        quickSort_Partitions(arr, i, pivot - 1)
        quickSort_Partitions(arr, pivot + 1, j)

    return arr

def classic_partitions(arr: list[int], i: int, j: int) -> int:
    pivot = arr[j]
    k = i - 1
    for idx in range(i, j):
        if arr[idx] <= pivot:
            k += 1
            arr[k], arr[idx] = arr[idx], arr[k]
    arr[k + 1], arr[j] = arr[j], arr[k + 1]
    return k + 1

# --- HeapSort ---
def heapify(arr: list[int], n: int, root: int) -> list[list[int]]:
    lst = []

    maxi = root
    left = 2 * root + 1
    right = 2 * root + 2

    if left < n and arr[left] > arr[maxi]:
        maxi = left
    if right < n and arr[right] > arr[maxi]:
        maxi = right

    if maxi != root:
        arr[root], arr[maxi] = arr[maxi], arr[root]
        prev = heapify(arr, n, maxi)
        if prev:
            lst.extend(prev)
        lst.append(arr[:])
    return lst

def heapSort(arr: list[int]) -> Generator[list[int], Any, None]:
    n = len(arr)

    for i in range(n // 2 - 1, -1, -1):
        prev = heapify(arr, n, i)
        for a in prev:
            yield a
        yield arr[:]

    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        prev = heapify(arr, i, 0)
        for a in prev:
            yield a
        yield arr[:]

# --- CountingSort ---
def countingSort(arr: list[int], low: int, high: int) -> Generator[list[int], Any, None]:
    ran = high - low + 1
    count = [0 for _ in range(ran)]

    for num in arr:
        count[num - low] += 1

    for i in range(1, len(count)):
        count[i] += count[i - 1]

    res = [0 for _ in range(len(arr))]

    for num in reversed(arr):
        index = num - low
        count[index] -= 1
        res[count[index]] = num
        yield res[:]


# --- MergeSort ---
def merge():
    pass


def mergeSort():
    pass

# --- BucketSort ---
def bucketSort():
    pass

# NEW PART
# --- Complexities ---
def constant(n: int) -> Generator[list[int], None, None]:
    arr = [1 for _ in range(n)]
    for _ in range(10):
        yield arr[:]

def log_n(n: int) -> Generator[list[int], None, None]:
    arr = [1 for _ in range(n)]
    yield arr[:]

    for i in range(1, len(arr)):
        arr[i] = int(log2(i + 1))
        for j in range(i+1, len(arr)):
            arr[j] = arr[i]
        yield arr[:]

def linear(n: int) -> Generator[list[int], None, None]:
    arr = [1 for _ in range(n)]
    yield arr[:]

    for i in range(len(arr)):
        for j in range(i, len(arr)):
            arr[j] += 1
        yield arr[:]

def n_log_n(n: int) -> Generator[list[int], None, None]:
    arr = [1 for _ in range(n)]
    yield arr[:]

    for i in range(1, len(arr)):
        arr[i] = int((i + 1) * log2(i + 1))
        for j in range(i + 1, len(arr)):
            arr[j] = arr[i]
        yield arr[:]

def quadratic(n: int) -> Generator[list[int], None, None]:
    arr = [1 for _ in range(n)]
    yield arr[:]

    for i in range(1, len(arr)):
        arr[i] = i ** 2
        for j in range(i + 1, len(arr)):
            arr[j] = arr[i]
        yield arr[:]

def exponential(n: int) -> Generator[list[int], None, None]:
    arr = [1 for _ in range(n)]
    yield arr[:]

    for i in range(1, len(arr)):
        arr[i] = 2 ** i
        for j in range(i + 1, len(arr)):
            arr[j] = arr[i]
        yield arr[:]

def worst_of_all(n: int) -> Generator[list[int], None, None]:
    arr = [1 for _ in range(n)]
    yield arr[:]

    for i in range(1, len(arr)):
        arr[i] = factorial(i)
        for j in range(i + 1, len(arr)):
            arr[j] = arr[i]
        yield arr[:]

# --- MAIN PART ---
def setup_bars(canvas, n):
    ids = []
    for i in range(n):
        ids.append(canvas.create_rectangle(0, 0, 0, 0, fill="lime", outline=""))
    return ids

def update_bars(canvas, ids, arr):
    w, h = int(canvas["width"]), int(canvas["height"])
    n = len(arr)
    max_val = max(arr) or 1
    bar_w = w / n
    for i, v in enumerate(arr):
        x0 = i * bar_w
        y0 = h - (v / max_val) * (h - 40)
        x1 = (i + 1) * bar_w - 3
        canvas.coords(ids[i], x0, y0, x1, h)

def animate_next(canvas: tk.Canvas,
                 algo_queue: deque[tuple[str, Generator[list[int], None, None]]],
                 ids, delay: int = 50):
    if not algo_queue:
        return

    title, gen = algo_queue[0]
    canvas.winfo_toplevel().title(f"{title}")

    try:
        state = next(gen)
        update_bars(canvas, ids, state)
        canvas.after(delay, animate_next, canvas, algo_queue, ids, delay)

    except StopIteration:
        algo_queue.popleft()
        canvas.after(delay, animate_next, canvas, algo_queue, ids, delay)


def main():
    print("--- Welcome to a Sorting algorithms and Complexity Visualizer ---\n"
          "-----------------------------------------------------------------\n"
          "First we need to choose MODE, data set SIZE and SPEED")
    mode = int(input("MODE (1 for sorting, 2 for complexities): "))
    if mode == 1 or mode == 2:
        pass
    else:
        raise TypeError

    size = int(input("------------------------------------------------------------\n"
                     "Data set SIZE: (type 0 for default 50)\n"
                     "If you wish to choose, type a valid number please between 1 - 150: "))
    if size == 0:
        size = 50
    elif 0 < size < 150:
        pass
    else:
        raise TypeError

    speed = int(input("--------------------------------------------------------\n"
                      "And lastly the speed you wish (type 0 for default 20ms)\n"
                      "Please choose between 15 - 100: "))
    if speed == 0:
        speed = 20
    elif 101 > speed > 14:
        pass
    else:
        raise TypeError

    root = tk.Tk()
    root.title("--- Welcome humans!!! ---")
    root.configure(bg="black")

    canvas = tk.Canvas(root, bg="black", width=1000, height=700)
    canvas.pack(padx=10, pady=10)
    canvas.focus_force()
    canvas.focus_force()
    canvas.focus()

    arr = [random.randint(0, 100) for _ in range(size)]


    if mode == 1:
        sorting = deque([
            ("Bubble Sort", bubbleSort(arr.copy())),
            ("Insertion Sort", insertSort(arr.copy())),
            ("Heap Sort", heapSort(arr.copy())),
            ("Quick Sort", quickSort(arr.copy())),
            ("Counting Sort", countingSort(arr.copy(), 0, len(arr) - 1))]
        )

        ids = setup_bars(canvas, size)
        animate_next(canvas, sorting, ids, speed)

    elif mode == 2:
        complexities = deque([
            ("Constant", constant(size)),
            ("Logarithmic (log2)", log_n(size)),
            ("Linear", linear(size)),
            ("N log n", n_log_n(size)),
            ("Quadratic", quadratic(size)),
            ("Exponential", exponential(size)),
            ("Factorial (Words of the worst)", worst_of_all(size))
        ])

        ids = setup_bars(canvas, size)
        animate_next(canvas, complexities, ids, speed)

    root.mainloop()



if __name__ == "__main__":
    main()
