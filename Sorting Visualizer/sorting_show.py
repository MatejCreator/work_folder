import pygame
import sys
import random
from typing import Any, Generator
from math import log2, factorial

NEONGREEN = (57, 255, 20)

class SortingShow:
    def __init__(self, screen, mode: str, size: int, speed: int, width, height):
        self.screen = screen
        self.mode = mode
        self.size = size
        self.speed = speed
        self.width = width
        self.height = height
        self.arr = [random.randint(0, 100) for _ in range(size)]
        self.name = ""

        self.background = pygame.image.load("assets/background_main.png").convert()
        self.title_font = pygame.font.Font("assets/exhotic-personal-use/Exhotic.ttf", 40)
        self.show = self.decider()

    def make_screen(self):
        title_text = self.title_font.render(f"{self.name}", True, NEONGREEN)
        title_rect = title_text.get_rect(center=(self.width / 2, 60))


        self.screen.blit(self.background, (0, 0))
        pygame.draw.line(self.screen, NEONGREEN, (0, self.height - 30), (self.width, self.height - 30), 5)
        self.screen.blit(title_text, title_rect)

    def decider(self):
        if self.mode == "Sorting":
            return [
            ("Bubble Sort", bubbleSort(self.arr.copy())),
            ("Insertion Sort", insertSort(self.arr.copy())),
            ("Heap Sort", heapSort(self.arr.copy())),
            ("Quick Sort", quickSort(self.arr.copy())),
            ("Counting Sort", countingSort(self.arr.copy(), 0, len(self.arr) - 1))
            ]

        elif self.mode == "Complexities":
            return [
            ("Constant", constant(self.size)),
            ("Logarithmic (log2)", log_n(self.size)),
            ("Linear", linear(self.size)),
            ("N log n", n_log_n(self.size)),
            ("Quadratic", quadratic(self.size)),
            ("Exponential", exponential(self.size)),
            ("Factorial (Words of the worst)", worst_of_all(self.size))
        ]

        else:
            raise TypeError

    def draw(self, lst: list[int]):
        self.make_screen()
        n = len(lst)
        max_val = max(lst)
        
        total_width = self.width
        gap = 2
        bar_w = (total_width - (n - 1) * gap) / n
        
        for i, v in enumerate(lst):
            bar_height = (v / max_val) * (self.height - 100) if max_val > 0 else 0
            
            rect = pygame.Rect(0, 0, bar_w, bar_height)
            rect.bottomleft = (i * (bar_w + gap), self.height - 30)
            pygame.draw.rect(self.screen, NEONGREEN, rect)
        
        pygame.display.flip()
        pygame.time.delay(self.speed)


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