"""Offline fallback engine — provides responses when the API is unavailable."""

from __future__ import annotations

from io import BytesIO
from typing import Any, Callable, Optional

import cv2
import numpy as np
from PIL import Image


def _match(pattern_words, text):
    """Return True if ANY of the pattern words exist in the lowercased text."""
    return any(w in text for w in pattern_words)


def generate_code_offline(problem: str) -> str:
    """Return a template-based Python solution for common problems."""
    p = problem.lower().strip()

    # ------------------------------------------------------------------
    # ALGORITHMS: Sorting & Searching
    # ------------------------------------------------------------------
    if _match(("bubble sort", "bubble_sort"), p):
        return (
            "def bubble_sort(arr: list) -> list:\n"
            '    """Sort a list using the bubble sort algorithm."""\n'
            "    n = len(arr)\n"
            "    for i in range(n):\n"
            "        swapped = False\n"
            "        for j in range(0, n - i - 1):\n"
            "            if arr[j] > arr[j + 1]:\n"
            "                arr[j], arr[j + 1] = arr[j + 1], arr[j]\n"
            "                swapped = True\n"
            "        if not swapped:\n"
            "            break\n"
            "    return arr\n"
        )

    if _match(("selection sort", "selection_sort"), p):
        return (
            "def selection_sort(arr: list) -> list:\n"
            '    """Sort a list using selection sort."""\n'
            "    n = len(arr)\n"
            "    for i in range(n):\n"
            "        min_idx = i\n"
            "        for j in range(i + 1, n):\n"
            "            if arr[j] < arr[min_idx]:\n"
            "                min_idx = j\n"
            "        arr[i], arr[min_idx] = arr[min_idx], arr[i]\n"
            "    return arr\n"
        )

    if _match(("insertion sort", "insertion_sort"), p):
        return (
            "def insertion_sort(arr: list) -> list:\n"
            '    """Sort a list using insertion sort."""\n'
            "    for i in range(1, len(arr)):\n"
            "        key = arr[i]\n"
            "        j = i - 1\n"
            "        while j >= 0 and arr[j] > key:\n"
            "            arr[j + 1] = arr[j]\n"
            "            j -= 1\n"
            "        arr[j + 1] = key\n"
            "    return arr\n"
        )

    if _match(("merge sort", "merge_sort", "merge sort"), p):
        return (
            "def merge_sort(arr: list) -> list:\n"
            '    """Sort a list using merge sort (divide & conquer)."""\n'
            "    if len(arr) <= 1:\n"
            "        return arr\n"
            "    mid = len(arr) // 2\n"
            "    left = merge_sort(arr[:mid])\n"
            "    right = merge_sort(arr[mid:])\n"
            "    return _merge(left, right)\n\n"
            "def _merge(left: list, right: list) -> list:\n"
            "    result = []\n"
            "    i = j = 0\n"
            "    while i < len(left) and j < len(right):\n"
            "        if left[i] <= right[j]:\n"
            "            result.append(left[i])\n"
            "            i += 1\n"
            "        else:\n"
            "            result.append(right[j])\n"
            "            j += 1\n"
            "    result.extend(left[i:])\n"
            "    result.extend(right[j:])\n"
            "    return result\n"
        )

    if _match(("quick sort", "quicksort", "quick_sort"), p):
        return (
            "def quick_sort(arr: list) -> list:\n"
            '    """Sort a list using quick sort (pivot-based)."""\n'
            "    if len(arr) <= 1:\n"
            "        return arr\n"
            "    pivot = arr[len(arr) // 2]\n"
            "    left = [x for x in arr if x < pivot]\n"
            "    middle = [x for x in arr if x == pivot]\n"
            "    right = [x for x in arr if x > pivot]\n"
            "    return quick_sort(left) + middle + quick_sort(right)\n"
        )

    if _match(("binary search tree", "binary_search_tree", "bst"), p):
        return (
            "class TreeNode:\n"
            "    def __init__(self, val):\n"
            "        self.val = val\n"
            "        self.left = None\n"
            "        self.right = None\n\n"
            "class BST:\n"
            '    """Binary Search Tree with insert, search, inorder."""\n'
            "    def __init__(self):\n"
            "        self.root = None\n\n"
            "    def insert(self, val):\n"
            "        self.root = self._insert(self.root, val)\n\n"
            "    def _insert(self, node, val):\n"
            "        if node is None:\n"
            "            return TreeNode(val)\n"
            "        if val < node.val:\n"
            "            node.left = self._insert(node.left, val)\n"
            "        elif val > node.val:\n"
            "            node.right = self._insert(node.right, val)\n"
            "        return node\n\n"
            "    def search(self, val) -> bool:\n"
            "        return self._search(self.root, val)\n\n"
            "    def _search(self, node, val) -> bool:\n"
            "        if node is None:\n"
            "            return False\n"
            "        if node.val == val:\n"
            "            return True\n"
            "        return (self._search(node.left, val) if val < node.val\n"
            "                else self._search(node.right, val))\n\n"
            "    def inorder(self) -> list:\n"
            "        result = []\n"
            "        self._inorder(self.root, result)\n"
            "        return result\n\n"
            "    def _inorder(self, node, result):\n"
            "        if node:\n"
            "            self._inorder(node.left, result)\n"
            "            result.append(node.val)\n"
            "            self._inorder(node.right, result)\n"
        )

    if _match(("binary search array", "binary_search_array", "binary search"), p) and "tree" not in p:
        return (
            "def binary_search(arr: list, target: int) -> int:\n"
            '    """Return the index of target in sorted arr, or -1 if not found."""\n'
            "    left, right = 0, len(arr) - 1\n"
            "    while left <= right:\n"
            "        mid = (left + right) // 2\n"
            "        if arr[mid] == target:\n"
            "            return mid\n"
            "        elif arr[mid] < target:\n"
            "            left = mid + 1\n"
            "        else:\n"
            "            right = mid - 1\n"
            "    return -1\n"
        )

    if _match(("linear search", "linear_search", "sequential search"), p):
        return (
            "def linear_search(arr: list, target: int) -> int:\n"
            '    """Return the index of target in arr, or -1 if not found."""\n'
            "    for i, val in enumerate(arr):\n"
            "        if val == target:\n"
            "            return i\n"
            "    return -1\n"
        )

    # ------------------------------------------------------------------
    # DATA STRUCTURES
    # ------------------------------------------------------------------
    if _match(("stack", "push", "pop"), p):
        return (
            "class Stack:\n"
            '    """A basic LIFO stack implementation."""\n'
            "    def __init__(self):\n"
            "        self.items = []\n\n"
            "    def push(self, item):\n"
            "        self.items.append(item)\n\n"
            "    def pop(self):\n"
            "        if self.is_empty():\n"
            "            raise IndexError('pop from empty stack')\n"
            "        return self.items.pop()\n\n"
            "    def peek(self):\n"
            "        return self.items[-1] if not self.is_empty() else None\n\n"
            "    def is_empty(self) -> bool:\n"
            "        return len(self.items) == 0\n\n"
            "    def size(self) -> int:\n"
            "        return len(self.items)\n"
        )

    if _match(("queue", "enqueue", "dequeue"), p):
        return (
            "from collections import deque\n\n"
            "class Queue:\n"
            '    """A basic FIFO queue implementation."""\n'
            "    def __init__(self):\n"
            "        self.items = deque()\n\n"
            "    def enqueue(self, item):\n"
            "        self.items.append(item)\n\n"
            "    def dequeue(self):\n"
            "        if self.is_empty():\n"
            "            raise IndexError('dequeue from empty queue')\n"
            "        return self.items.popleft()\n\n"
            "    def front(self):\n"
            "        return self.items[0] if not self.is_empty() else None\n\n"
            "    def is_empty(self) -> bool:\n"
            "        return len(self.items) == 0\n\n"
            "    def size(self) -> int:\n"
            "        return len(self.items)\n"
        )

    if _match(("linked list", "linked_list", "linkedlist"), p):
        return (
            "class Node:\n"
            '    """A single node in a linked list."""\n'
            "    def __init__(self, data):\n"
            "        self.data = data\n"
            "        self.next = None\n\n"
            "class LinkedList:\n"
            '    """A singly linked list."""\n'
            "    def __init__(self):\n"
            "        self.head = None\n\n"
            "    def append(self, data):\n"
            "        if not self.head:\n"
            "            self.head = Node(data)\n"
            "            return\n"
            "        curr = self.head\n"
            "        while curr.next:\n"
            "            curr = curr.next\n"
            "        curr.next = Node(data)\n\n"
            "    def prepend(self, data):\n"
            "        new_node = Node(data)\n"
            "        new_node.next = self.head\n"
            "        self.head = new_node\n\n"
            "    def delete(self, data):\n"
            "        if not self.head:\n"
            "            return\n"
            "        if self.head.data == data:\n"
            "            self.head = self.head.next\n"
            "            return\n"
            "        curr = self.head\n"
            "        while curr.next and curr.next.data != data:\n"
            "            curr = curr.next\n"
            "        if curr.next:\n"
            "            curr.next = curr.next.next\n\n"
            "    def display(self) -> list:\n"
            "        result = []\n"
            "        curr = self.head\n"
            "        while curr:\n"
            "            result.append(curr.data)\n"
            "            curr = curr.next\n"
            "        return result\n"
        )

    if _match(("graph", "bfs", "dfs", "breadth", "depth"), p):
        return (
            "from collections import deque\n\n"
            "class Graph:\n"
            "    def __init__(self):\n"
            "        self.adj = {}\n\n"
            "    def add_edge(self, u, v):\n"
            "        if u not in self.adj:\n"
            "            self.adj[u] = []\n"
            "        if v not in self.adj:\n"
            "            self.adj[v] = []\n"
            "        self.adj[u].append(v)\n"
            "        self.adj[v].append(u)\n\n"
            "    def bfs(self, start):\n"
            '        """Breadth-first traversal."""\n'
            "        visited = set()\n"
            "        q = deque([start])\n"
            "        result = []\n"
            "        while q:\n"
            "            node = q.popleft()\n"
            "            if node not in visited:\n"
            "                visited.add(node)\n"
            "                result.append(node)\n"
            "                q.extend(n for n in self.adj[node] if n not in visited)\n"
            "        return result\n\n"
            "    def dfs(self, start):\n"
            '        """Depth-first traversal."""\n'
            "        visited = set()\n"
            "        result = []\n\n"
            "        def _dfs(node):\n"
            "            visited.add(node)\n"
            "            result.append(node)\n"
            "            for neighbor in self.adj[node]:\n"
            "                if neighbor not in visited:\n"
            "                    _dfs(neighbor)\n\n"
            "        _dfs(start)\n"
            "        return result\n"
        )

    # ------------------------------------------------------------------
    # STRING OPERATIONS
    # ------------------------------------------------------------------
    if _match(("palindrome", "palindrom"), p):
        return (
            "def is_palindrome(s: str) -> bool:\n"
            '    """Return True if s is a palindrome (case-insensitive)."""\n'
            "    s = s.replace(' ', '').lower()\n"
            "    return s == s[::-1]\n"
        )

    if _match(("reverse string", "reverse a string", "string reverse"), p):
        return (
            "def reverse_string(s: str) -> str:\n"
            '    """Return the reversed version of s."""\n'
            "    return s[::-1]\n"
        )

    if _match(("anagram", "anagram"), p):
        return (
            "def is_anagram(s1: str, s2: str) -> bool:\n"
            '    """Check if two strings are anagrams of each other."""\n'
            "    s1 = s1.replace(' ', '').lower()\n"
            "    s2 = s2.replace(' ', '').lower()\n"
            "    return sorted(s1) == sorted(s2)\n"
        )

    if _match(("pangram",), p):
        return (
            "import string\n\n"
            "def is_pangram(s: str) -> bool:\n"
            '    """Return True if s contains every letter of the alphabet."""\n'
            "    return set(string.ascii_lowercase).issubset(set(s.lower()))\n"
        )

    if _match(("vowel", "count vowels", "count_vowels"), p):
        return (
            "def count_vowels(s: str) -> int:\n"
            '    """Return the number of vowels (a, e, i, o, u) in s."""\n'
            "    return sum(1 for ch in s.lower() if ch in 'aeiou')\n"
        )

    if _match(("substring", "sub string"), p):
        return (
            "def is_substring(s: str, sub: str) -> bool:\n"
            '    """Check if sub is a substring of s (without using in)."""\n'
            "    for i in range(len(s) - len(sub) + 1):\n"
            "        if s[i:i + len(sub)] == sub:\n"
            "            return True\n"
            "    return False\n"
        )

    # ------------------------------------------------------------------
    # ARRAY / LIST OPERATIONS
    # ------------------------------------------------------------------
    if _match(("rotate array", "rotate list", "array rotate", "list rotate"), p):
        return (
            "def rotate_list(arr: list, k: int) -> list:\n"
            '    """Rotate array to the right by k steps."""\n'
            "    n = len(arr)\n"
            "    k %= n\n"
            "    return arr[-k:] + arr[:-k]\n"
        )

    if _match(("remove duplicate", "remove_duplicate", "unique"), p):
        return (
            "def remove_duplicates(arr: list) -> list:\n"
            '    """Remove duplicates while preserving order."""\n'
            "    seen = set()\n"
            "    result = []\n"
            "    for item in arr:\n"
            "        if item not in seen:\n"
            "            seen.add(item)\n"
            "            result.append(item)\n"
            "    return result\n"
        )

    if _match(("two sum", "two_sum", "pair sum"), p):
        return (
            "def two_sum(nums: list[int], target: int) -> list[int]:\n"
            '    """Return indices of two numbers that add up to target."""\n'
            "    seen = {}\n"
            "    for i, num in enumerate(nums):\n"
            "        complement = target - num\n"
            "        if complement in seen:\n"
            "            return [seen[complement], i]\n"
            "        seen[num] = i\n"
            "    return []\n"
        )

    if _match(("max subarray", "maximum subarray", "kadane"), p):
        return (
            "def max_subarray_sum(arr: list[int]) -> int:\n"
            '    """Return the maximum sum of any contiguous subarray (Kadane)."""\n'
            "    max_ending = max_so_far = arr[0]\n"
            "    for num in arr[1:]:\n"
            "        max_ending = max(num, max_ending + num)\n"
            "        max_so_far = max(max_so_far, max_ending)\n"
            "    return max_so_far\n"
        )

    if _match(("find max", "find min", "maximum", "minimum"), p):
        return (
            "def find_max_min(arr: list) -> tuple:\n"
            '    """Return (min, max) from an array."""\n'
            "    if not arr:\n"
            "        return None, None\n"
            "    return min(arr), max(arr)\n"
        )

    if _match(("missing number", "missing_number", "find missing"), p):
        return (
            "def find_missing_number(nums: list[int], n: int) -> int:\n"
            '    """Find the missing number from 1..n in an unsorted list."""\n'
            "    expected = n * (n + 1) // 2\n"
            "    actual = sum(nums)\n"
            "    return expected - actual\n"
        )

    # ------------------------------------------------------------------
    # MATHEMATICAL PROBLEMS
    # ------------------------------------------------------------------
    if _match(("prime", "primality", "is prime"), p):
        return (
            "def is_prime(n: int) -> bool:\n"
            '    """Return True if n is a prime number."""\n'
            "    if n < 2:\n"
            "        return False\n"
            "    for i in range(2, int(n ** 0.5) + 1):\n"
            "        if n % i == 0:\n"
            "            return False\n"
            "    return True\n"
        )

    if _match(("fibonacci", "fib", "fibbo"), p):
        return (
            "def fibonacci(n: int) -> list[int]:\n"
            '    """Return the first n Fibonacci numbers."""\n'
            "    if n <= 0:\n"
            "        return []\n"
            "    if n == 1:\n"
            "        return [0]\n"
            "    fib = [0, 1]\n"
            "    for _ in range(2, n):\n"
            "        fib.append(fib[-1] + fib[-2])\n"
            "    return fib\n"
        )

    if _match(("factorial", "fact"), p):
        return (
            "def factorial(n: int) -> int:\n"
            '    """Return n! (factorial of n)."""\n'
            "    if n < 0:\n"
            "        raise ValueError('Factorial not defined for negative numbers')\n"
            "    if n == 0:\n"
            "        return 1\n"
            "    result = 1\n"
            "    for i in range(2, n + 1):\n"
            "        result *= i\n"
            "    return result\n"
        )

    if _match(("fizzbuzz", "fizz buzz", "fizz"), p):
        return (
            "def fizzbuzz(n: int) -> list[str]:\n"
            '    """Return FizzBuzz sequence up to n."""\n'
            "    result = []\n"
            "    for i in range(1, n + 1):\n"
            "        if i % 15 == 0:\n"
            "            result.append('FizzBuzz')\n"
            "        elif i % 3 == 0:\n"
            "            result.append('Fizz')\n"
            "        elif i % 5 == 0:\n"
            "            result.append('Buzz')\n"
            "        else:\n"
            "            result.append(str(i))\n"
            "    return result\n"
        )

    if _match(("gcd", "lcm", "hcf"), p):
        return (
            "def gcd(a: int, b: int) -> int:\n"
            '    """Return greatest common divisor using Euclidean algorithm."""\n'
            "    while b:\n"
            "        a, b = b, a % b\n"
            "    return a\n\n"
            "def lcm(a: int, b: int) -> int:\n"
            '    """Return least common multiple."""\n'
            "    return a * b // gcd(a, b)\n"
        )

    if _match(("sieve", "eratosthenes", "prime numbers up to"), p):
        return (
            "def sieve_of_eratosthenes(n: int) -> list[int]:\n"
            '    """Return all primes up to n using the Sieve of Eratosthenes."""\n'
            "    is_prime = [True] * (n + 1)\n"
            "    is_prime[0] = is_prime[1] = False\n"
            "    for i in range(2, int(n ** 0.5) + 1):\n"
            "        if is_prime[i]:\n"
            "            for j in range(i * i, n + 1, i):\n"
            "                is_prime[j] = False\n"
            "    return [i for i in range(n + 1) if is_prime[i]]\n"
        )

    if _match(("armstrong", "armstrong number", "narcissistic"), p):
        return (
            "def is_armstrong(n: int) -> bool:\n"
            '    """Check if n is an Armstrong (narcissistic) number."""\n'
            "    digits = [int(d) for d in str(n)]\n"
            "    power = len(digits)\n"
            "    return sum(d ** power for d in digits) == n\n"
        )

    if _match(("perfect number", "perfect_number"), p):
        return (
            "def is_perfect_number(n: int) -> bool:\n"
            '    """Return True if n is a perfect number."""\n'
            "    if n < 2:\n"
            "        return False\n"
            "    divisors_sum = 1\n"
            "    for i in range(2, int(n ** 0.5) + 1):\n"
            "        if n % i == 0:\n"
            "            divisors_sum += i\n"
            "            if i != n // i:\n"
            "                divisors_sum += n // i\n"
            "    return divisors_sum == n\n"
        )

    if _match(("power of", "exponent", "pow"), p):
        return (
            "def power(base: int, exp: int) -> int:\n"
            '    """Compute base ** exp using fast exponentiation."""\n'
            "    if exp == 0:\n"
            "        return 1\n"
            "    half = power(base, exp // 2)\n"
            "    if exp % 2 == 0:\n"
            "        return half * half\n"
            "    return base * half * half\n"
        )

    # ------------------------------------------------------------------
    # FILE / IO OPERATIONS
    # ------------------------------------------------------------------
    if _match(("read file", "read_file", "open file", "file read"), p):
        return (
            "def read_file(filepath: str) -> str:\n"
            '    """Read and return the entire contents of a file."""\n'
            "    with open(filepath, 'r', encoding='utf-8') as f:\n"
            "        return f.read()\n"
        )

    if _match(("write file", "write_file", "file write", "save to file"), p):
        return (
            "def write_file(filepath: str, content: str) -> None:\n"
            '    """Write content to a file (overwrite mode)."""\n'
            "    with open(filepath, 'w', encoding='utf-8') as f:\n"
            "        f.write(content)\n"
        )

    if _match(("csv", "comma separated", "read csv", "write csv"), p):
        return (
            "import csv\n\n"
            "def read_csv(filepath: str) -> list[dict]:\n"
            '    """Read a CSV file and return rows as dictionaries."""\n'
            "    with open(filepath, 'r', newline='', encoding='utf-8') as f:\n"
            "        return list(csv.DictReader(f))\n\n"
            "def write_csv(filepath: str, data: list[dict], fieldnames: list[str]) -> None:\n"
            '    """Write a list of dicts to a CSV file."""\n'
            "    with open(filepath, 'w', newline='', encoding='utf-8') as f:\n"
            "        writer = csv.DictWriter(f, fieldnames=fieldnames)\n"
            "        writer.writeheader()\n"
            "        writer.writerows(data)\n"
        )

    if _match(("json", "json read", "json write", "parse json"), p):
        return (
            "import json\n\n"
            "def read_json(filepath: str) -> dict | list:\n"
            '    """Read and parse a JSON file."""\n'
            "    with open(filepath, 'r', encoding='utf-8') as f:\n"
            "        return json.load(f)\n\n"
            "def write_json(filepath: str, data: dict | list, indent: int = 2) -> None:\n"
            '    """Write data to a JSON file."""\n'
            "    with open(filepath, 'w', encoding='utf-8') as f:\n"
            "        json.dump(data, f, indent=indent)\n"
        )

    # ------------------------------------------------------------------
    # WEB / API
    # ------------------------------------------------------------------
    if _match(("http request", "http get", "http post", "fetch url", "api request", "requests.get"), p):
        return (
            "import requests\n\n"
            "def fetch_url(url: str) -> dict | str:\n"
            '    """Fetch JSON data from a URL using an HTTP GET request."""\n'
            "    try:\n"
            "        response = requests.get(url, timeout=10)\n"
            "        response.raise_for_status()\n"
            "        return response.json()\n"
            "    except requests.exceptions.RequestException as e:\n"
            "        return f'Request failed: {e}'\n"
        )

    if _match(("web scrape", "webscrape", "scrape", "bs4", "beautifulsoup"), p):
        return (
            "import requests\n"
            "from bs4 import BeautifulSoup\n\n"
            "def scrape_title(url: str) -> str | None:\n"
            '    """Scrape the page title from a URL."""\n'
            "    try:\n"
            "        response = requests.get(url, timeout=10)\n"
            "        response.raise_for_status()\n"
            "        soup = BeautifulSoup(response.text, 'html.parser')\n"
            "        return soup.title.string.strip() if soup.title else None\n"
            "    except Exception as e:\n"
            "        return f'Error: {e}'\n"
        )

    if _match(("download", "download file"), p):
        return (
            "import requests\n\n"
            "def download_file(url: str, save_path: str) -> bool:\n"
            '    """Download a file from a URL and save it locally."""\n'
            "    try:\n"
            "        response = requests.get(url, timeout=30, stream=True)\n"
            "        response.raise_for_status()\n"
            "        with open(save_path, 'wb') as f:\n"
            "            for chunk in response.iter_content(chunk_size=8192):\n"
            "                f.write(chunk)\n"
            "        return True\n"
            "    except Exception as e:\n"
            "        print(f'Download failed: {e}')\n"
            "        return False\n"
        )

    # ------------------------------------------------------------------
    # OPENCV / IMAGE PROCESSING
    # ------------------------------------------------------------------
    if _match(("opencv", "cv2", "image processing", "read image", "show image", "load image"), p):
        return (
            "import cv2\n\n"
            "# Read an image\n"
            "image = cv2.imread('input.jpg')\n\n"
            "# Convert to grayscale\n"
            "gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)\n\n"
            "# Apply Gaussian blur\n"
            "blurred = cv2.GaussianBlur(gray, (5, 5), 0)\n\n"
            "# Edge detection\n"
            "edges = cv2.Canny(blurred, 50, 150)\n\n"
            "# Display or save\n"
            "cv2.imshow('Original', image)\n"
            "cv2.imshow('Edges', edges)\n"
            "cv2.waitKey(0)\n"
            "cv2.destroyAllWindows()\n"
            "cv2.imwrite('result.jpg', edges)\n"
        )

    if _match(("resize image", "resize_image", "scale image"), p):
        return (
            "import cv2\n\n"
            "def resize_image(image_path: str, width: int, height: int) -> None:\n"
            '    """Resize an image to the given dimensions."""\n'
            "    image = cv2.imread(image_path)\n"
            "    resized = cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)\n"
            "    cv2.imwrite('resized.jpg', resized)\n"
        )

    # ------------------------------------------------------------------
    # COMMON ALGORITHM / RECURSION
    # ------------------------------------------------------------------
    if _match(("tower of hanoi", "towerofhanoi", "hanoi"), p):
        return (
            "def tower_of_hanoi(n: int, source: str, target: str, auxiliary: str) -> None:\n"
            '    """Print steps to move n disks from source to target."""\n'
            "    if n == 1:\n"
            "        print(f'Move disk 1 from {source} to {target}')\n"
            "        return\n"
            "    tower_of_hanoi(n - 1, source, auxiliary, target)\n"
            "    print(f'Move disk {n} from {source} to {target}')\n"
            "    tower_of_hanoi(n - 1, auxiliary, target, source)\n"
        )

    if _match(("n queen", "nqueen", "n-queen"), p):
        return (
            "def solve_n_queens(n: int) -> list[list[str]]:\n"
            "    '''Solve the N-Queens puzzle and return all board configurations.'''\n"
            "    cols = set()\n"
            "    pos_diag = set()\n"
            "    neg_diag = set()\n"
            "    board = [['.'] * n for _ in range(n)]\n"
            "    result = []\n\n"
            "    def backtrack(row):\n"
            "        if row == n:\n"
            "            result.append([''.join(r) for r in board])\n"
            "            return\n"
            "        for col in range(n):\n"
            "            if col in cols or (row + col) in pos_diag or (row - col) in neg_diag:\n"
            "                continue\n"
            "            cols.add(col)\n"
            "            pos_diag.add(row + col)\n"
            "            neg_diag.add(row - col)\n"
            "            board[row][col] = 'Q'\n"
            "            backtrack(row + 1)\n"
            "            board[row][col] = '.'\n"
            "            cols.remove(col)\n"
            "            pos_diag.remove(row + col)\n"
            "            neg_diag.remove(row - col)\n\n"
            "    backtrack(0)\n"
            "    return result\n"
        )

    if _match(("binary to decimal", "binary_to_decimal", "bin to dec", "decimal to binary", "dec to bin"), p):
        return (
            "def binary_to_decimal(binary_str: str) -> int:\n"
            '    """Convert binary string to decimal integer."""\n'
            "    return int(binary_str, 2)\n\n"
            "def decimal_to_binary(n: int) -> str:\n"
            '    """Convert decimal integer to binary string."""\n'
            "    return bin(n)[2:]\n"
        )

    # ------------------------------------------------------------------
    # REGEX / DATE / FORMATTING
    # ------------------------------------------------------------------
    if _match(("validate", "email regex", "email pattern"), p) and "email" in p:
        return (
            "import re\n\n"
            "def is_valid_email(email: str) -> bool:\n"
            '    """Validate an email address with a simple regex pattern."""\n'
            "    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'\n"
            "    return bool(re.match(pattern, email))\n"
        )

    if _match(("current date", "current time", "get date", "get time", "datetime"), p):
        return (
            "from datetime import datetime\n\n"
            "def get_current_datetime() -> str:\n"
            '    """Return the current date and time as a formatted string."""\n'
            "    now = datetime.now()\n"
            "    return now.strftime('%Y-%m-%d %H:%M:%S')\n"
        )

    # ------------------------------------------------------------------
    # HELPFUL FALLBACK
    # ------------------------------------------------------------------
    if _match(("opencv", "cv2", "image", "canny", "blur", "edge", "contour", "filter", "face", "detect"), p):
        return (
            "import cv2\nimport numpy as np\n\n"
            "image = cv2.imread('input.jpg')\n"
            "gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)\n\n"
            "# Apply your filter here\n"
            "result = cv2.GaussianBlur(gray, (5, 5), 0)\n\n"
            "cv2.imshow('Result', result)\n"
            "cv2.waitKey(0)\n"
            "cv2.destroyAllWindows()\n"
            "cv2.imwrite('output.jpg', result)\n"
        )

    # Extract key nouns to give a better fallback hint
    words_of_interest = [w for w in p.split() if len(w) > 3]
    hint = ""
    if words_of_interest:
        top_hints = list(set(words_of_interest))[:3]
        hint = f'# Hint: your query mentioned: {", ".join(top_hints)}\n'

    return (
        hint + "# Python solution template\n"
        "def solve(data):\n"
        '    """Implement your solution logic here."""\n'
        "    # TODO: Replace with actual implementation\n"
        "    return data\n\n\n"
        'if __name__ == "__main__":\n'
        '    sample_input = "example"\n'
        "    result = solve(sample_input)\n"
        "    print(result)\n"
    )


def explain_code_offline(code: str) -> str:
    """Return a generic explanation for the given code."""
    lines = code.strip().split("\n")
    explanation = ["**Code Explanation (Offline Mode)**\n"]

    for line in lines[:15]:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("def "):
            func_name = stripped.split("(")[0].replace("def ", "")
            explanation.append(f"- `{stripped}` — Defines a function named `{func_name}`.")
        elif stripped.startswith("class "):
            class_name = stripped.split("(")[0].replace("class ", "").strip(":")
            explanation.append(f"- `{stripped}` — Defines a class named `{class_name}`.")
        elif stripped.startswith("if ") and ":" in stripped:
            explanation.append(f"- `{stripped}` — Conditional branch.")
        elif stripped.startswith("for ") or stripped.startswith("while "):
            explanation.append(f"- `{stripped}` — Loop construct.")
        elif stripped.startswith("import ") or stripped.startswith("from "):
            explanation.append(f"- `{stripped}` — Imports a module.")
        elif stripped.startswith("return "):
            explanation.append(f"- `{stripped}` — Returns a value from the function.")
        elif stripped.startswith("print"):
            explanation.append(f"- `{stripped}` — Outputs data to the console.")
        elif stripped.startswith("#"):
            explanation.append(f"- Comment: {stripped.lstrip('# ')}")
        else:
            explanation.append(f"- `{stripped}` — Executes an assignment or operation.")

    explanation.append(
        "\n*Tip: Connect to the API for a detailed line-by-line explanation.*"
    )
    return "\n".join(explanation)


def debug_error_offline(error: str) -> str:
    """Return common debugging tips based on error type."""
    error_lower = error.lower()

    tips = {
        "syntaxerror": (
            "**SyntaxError** — The Python parser found invalid syntax.\n"
            "- Check for missing colons (`:`) after `if`, `for`, `while`, `def`, `class`.\n"
            "- Ensure parentheses, brackets, and quotes are balanced.\n"
            "- Look for stray or missing commas."
        ),
        "indentationerror": (
            "**IndentationError** — Python enforces consistent indentation.\n"
            "- Use 4 spaces per level (avoid mixing tabs and spaces).\n"
            "- Check that all lines in a block are indented evenly."
        ),
        "nameerror": (
            "**NameError** — A variable or function name is not defined.\n"
            "- Check the spelling of the name.\n"
            "- Ensure the variable is defined before use.\n"
            "- Verify the name is in scope."
        ),
        "typeerror": (
            "**TypeError** — An operation is applied to an object of inappropriate type.\n"
            "- Check that you are not calling a non-callable object.\n"
            "- Verify function arguments match the expected types.\n"
            "- Use `type()` to inspect variable types."
        ),
        "valueerror": (
            "**ValueError** — A function received an argument with the right type but wrong value.\n"
            "- Check the value range before passing it to the function.\n"
            "- Use try/except to handle invalid input gracefully."
        ),
        "keyerror": (
            "**KeyError** — A dictionary key was not found.\n"
            "- Use `.get(key, default)` instead of `[key]`.\n"
            "- Check if the key exists with `in` before accessing."
        ),
        "indexerror": (
            "**IndexError** — A list index is out of range.\n"
            "- Ensure the index is within `0` to `len(list)-1`.\n"
            "- Use `if index < len(lst):` before accessing."
        ),
        "attributeerror": (
            "**AttributeError** — An object does not have the requested attribute.\n"
            "- Check the spelling of the attribute.\n"
            "- Verify the object is of the expected type using `type()`."
        ),
        "importerror": (
            "**ImportError** — A module could not be imported.\n"
            "- Ensure the module is installed (`pip install <module>`).\n"
            "- Check the module name spelling."
        ),
        "filenotfounderror": (
            "**FileNotFoundError** — A file path does not exist.\n"
            "- Verify the file path is correct.\n"
            "- Use `os.path.exists()` to check before opening."
        ),
        "zerodivisionerror": (
            "**ZeroDivisionError** — Division by zero occurred.\n"
            "- Check that the denominator is not zero before dividing.\n"
            "- Add an `if denom != 0:` guard."
        ),
    }

    for keyword, tip in tips.items():
        if keyword in error_lower:
            return tip

    return (
        "**Common Debugging Tips**\n"
        "- Read the error message carefully — Python tells you exactly what went wrong.\n"
        "- Look at the line number in the traceback.\n"
        "- Check variable types with `type()`.\n"
        "- Use `print()` or a debugger to inspect intermediate values.\n"
        "- Search the error message online — chances are someone else has solved it.\n"
        "- If using the API, paste the full traceback for a detailed fix."
    )


def improve_code_offline(code: str) -> str:
    """Return an improved version of the given code with refactoring applied."""
    original = code.strip()
    improved = original
    changes = []

    # 1. Add missing type hints to function definitions
    import re as _re
    defs = _re.findall(r'^def (\w+)\((.*?)\):', improved, _re.MULTILINE)
    for func_name, args_str in defs:
        old_sig = f"def {func_name}({args_str}):"
        if args_str.strip() and ":" not in args_str and args_str.strip() != "self":
            hinted_args = []
            for a in args_str.split(","):
                a = a.strip()
                if a and a != "self" and ":" not in a:
                    hinted_args.append(f"{a}: Any")
                else:
                    hinted_args.append(a)
            new_sig = f"def {func_name}({', '.join(hinted_args)}):"
            improved = improved.replace(old_sig, new_sig)
            if old_sig != new_sig:
                changes.append(f"Added type hints to `{func_name}()` parameters")
        if "->" not in old_sig and func_name != "__init__":
            new_sig2 = f"def {func_name}({args_str}) -> Any:"
            improved = improved.replace(old_sig, new_sig2)
            changes.append(f"Added return type hint to `{func_name}()`")

    # 2. Replace print with f-strings
    prints = _re.findall(r"print\((.*?)\)", improved)
    for p in prints:
        if "+" in p and '"' in p:
            old_p = f"print({p})"
            parts = p.split("+")
            f_content = "".join(
                f"{{{part.strip()}}}" if not part.strip().startswith('"') and not part.strip().startswith("'")
                else part.strip().strip("'\"")
                for part in parts
            )
            new_p = f"print(f\"{f_content}\")"
            improved = improved.replace(old_p, new_p)
            changes.append("Converted print() to f-string")

    # 3. Replace manual file open/close with context manager
    for m in _re.finditer(r"(\w+)\s*=\s*open\(([^)]+)\)", improved):
        var_name = m.group(1)
        args = m.group(2)
        if var_name not in improved.split(".close()", 1)[0]:
            continue
        close_pattern = _re.escape(var_name) + r"\.close\(\)"
        indented = _re.search(
            rf"^{var_name}\s*=\s*open\({_re.escape(args)}\)\n((?:[ \t]+.*\n?)*)",
            improved, _re.MULTILINE
        )
        if indented:
            block = indented.group(1)
            indent = "    "
            with_block = f"with open({args}) as {var_name}:\n"
            for line in block.split("\n"):
                if line.strip() and var_name not in line or ".close()" not in line:
                    with_block += f"{indent}{line}\n" if line.strip() else "\n"
            improved = improved.replace(f"{var_name} = open({args})\n{block}", with_block)
            improved = _re.sub(rf"\n\s*{_re.escape(var_name)}\.close\(\)", "", improved)
            changes.append("Replaced manual file open/close with `with` context manager")

    # 4. Replace for i in range(len(...)) with direct iteration + enumerate
    for m in _re.finditer(r"for\s+(\w+)\s+in\s+range\(len\((\w+)\)\):", improved):
        idx_var = m.group(1)
        collection = m.group(2)
        body_match = _re.search(
            rf"for\s+{idx_var}\s+in\s+range\(len\({collection}\)\):((?:\n[ \t]+.*)*)",
            improved
        )
        if body_match:
            body = body_match.group(1)
            new_body = body.replace(f"{collection}[{idx_var}]", "item")
            new_loop = f"for item in {collection}:{new_body}"
            improved = improved.replace(body_match.group(0), new_loop)
            changes.append(f"Replaced indexed loop with direct iteration over `{collection}`")

    # 5. Add if __name__ guard if main logic is present without it
    if "if __name__" not in improved and _re.search(r"(print\(|main\(|run\(|app\.)", improved):
        first_def = _re.search(r"^def ", improved, _re.MULTILINE)
        if first_def:
            after_defs = improved[first_def.start():]
            last_line = [l for l in after_defs.split("\n") if l.strip()][-1]
            if not last_line.startswith("if ") and not last_line.startswith("#"):
                improved += '\n\nif __name__ == "__main__":\n    # TODO: Add main execution logic\n    pass\n'
                changes.append("Added `if __name__ == '__main__':` guard")

    # 6. Replace == None / != None with is None / is not None
    if "== None" in improved:
        improved = improved.replace("== None", "is None")
        changes.append("Replaced `== None` with `is None`")
    if "!= None" in improved:
        improved = improved.replace("!= None", "is not None")
        changes.append("Replaced `!= None` with `is not None`")

    # 7. Add try/except around file I/O operations
    for m in _re.finditer(r"with open\(([^)]+)\) as (\w+):\n((?:\s+.*\n?)*)", improved):
        full_match = m.group(0)
        stmt = m.group(1)
        var = m.group(2)
        body = m.group(3)
        if "try" not in improved.split(full_match)[-1][:50]:
            indented_body = "\n".join(f"    {line}" if line.strip() else "" for line in body.split("\n"))
            try_block = (
                f"try:\n"
                f"    with open({stmt}) as {var}:\n"
                f"{indented_body}"
                f"except IOError as e:\n"
                f"    print(f'Error accessing file: {{e}}')\n"
            )
            improved = improved.replace(full_match, try_block)
            changes.append("Wrapped file I/O with try/except error handling")

    summary_lines = ["## Improved & Refactored Code\n"]
    summary_lines.append("**Changes applied:**")
    for c in changes:
        summary_lines.append(f"  ✅ {c}")
    if not changes:
        summary_lines.append("  ℹ️ Code already follows best practices — no refactoring needed.")
    summary_lines.append("")
    summary_lines.append("---\n")

    return "\n".join(summary_lines) + "\n" + improved


def add_comments_offline(code: str) -> str:
    """Add detailed documentation comments to the given Python code."""
    lines = code.strip().split("\n")
    result = []
    prev_was_comment = False
    has_module_doc = False
    import re as _re

    # Extract module-level info from function names
    func_names = _re.findall(r"^def (\w+)\(", code, _re.MULTILINE)
    class_names = _re.findall(r"^class (\w+)", code, _re.MULTILINE)

    # Add module-level docstring if no comment exists at top
    first_line = lines[0].strip() if lines else ""
    if first_line and not first_line.startswith("#") and not first_line.startswith('"""'):
        summary_parts = []
        if class_names:
            summary_parts.append(f"Defines the `{class_names[0]}` class")
        elif func_names:
            summary_parts.append(f"Provides the `{func_names[0]}()` function")
        if summary_parts:
            result.append(f"# {'. '.join(summary_parts)}.")
            result.append("")

    for line in lines:
        stripped = line.strip()

        if not stripped:
            result.append(line)
            prev_was_comment = False
            continue

        if stripped.startswith("#") or stripped.startswith('"""'):
            result.append(line)
            prev_was_comment = True
            continue

        # Import statements
        if stripped.startswith("import ") or stripped.startswith("from "):
            module = stripped.split()[1] if stripped.startswith("import ") else stripped.split()[1]
            if stripped.startswith("from "):
                module = f"{stripped.split()[1]}.{stripped.split()[3]}"
            result.append(f"# Import the `{module}` module for {_comment_for_import(module)}")
            result.append(line)

        # Function definitions
        elif stripped.startswith("def "):
            func_name = stripped.split("(")[0].replace("def ", "")
            args_part = stripped[stripped.find("(") + 1 : stripped.find(")")]
            args_list = [a.strip().split(":")[0] for a in args_part.split(",") if a.strip()]
            result.append(f"# Define `{func_name}()` — {'Calculate ' if 'calc' in func_name or 'compute' in func_name or 'get_' in func_name or 'find_' in func_name else 'Check ' if 'is_' in func_name or 'has_' in func_name or func_name.startswith('check') else 'Process ' if 'process' in func_name or 'convert' in func_name or 'transform' in func_name else 'Handle '}")
            result.append(f"# Args: {', '.join(args_list) if args_list else '(none)'}")
            result.append(line)
            prev_was_comment = True
            continue

        # Class definitions
        elif stripped.startswith("class "):
            class_name = stripped.split("(")[0].replace("class ", "").strip(":")
            parent = ""
            if "(" in stripped:
                parent = stripped.split("(")[1].split(")")[0]
            result.append(f"# Define the `{class_name}` class" + (f" inheriting from `{parent}`" if parent else ""))
            result.append(f"# Encapsulates related data and behavior for {class_name.lower().replace('_', ' ')}")
            result.append(line)

        # Return statements
        elif stripped.startswith("return "):
            ret_val = stripped[7:]
            if ret_val in ("True", "False"):
                result.append("# Return boolean result indicating success or failure")
            elif ret_val == "None":
                result.append("# Exit function with no return value")
            else:
                result.append(f"# Return the computed `{ret_val}` to the caller")
            result.append(line)

        # Print statements
        elif stripped.startswith("print"):
            result.append("# Display output to the console for user inspection")
            result.append(line)

        # If/elif/else
        elif stripped.startswith("if ") or stripped.startswith("elif "):
            condition = stripped[3:] if stripped.startswith("if ") else stripped[5:]
            result.append(f"# Branch: execute only when `{condition}` is True")
            result.append(line)
        elif stripped == "else:" or stripped == "else :":
            result.append("# Fallback: execute when no prior condition matched")
            result.append(line)

        # Loops
        elif stripped.startswith("for "):
            loop_var = stripped.split()[1]
            iterable = stripped.split(" in ")[-1].rstrip(":")
            result.append(f"# Iterate over each element in `{iterable}`, assigning to `{loop_var}`")
            result.append(line)
        elif stripped.startswith("while "):
            condition = stripped[6:]
            result.append(f"# Repeat while `{condition}` remains True")
            result.append(line)

        # Try/except
        elif stripped.startswith("try:"):
            result.append("# Attempt the following block; handle exceptions gracefully if they occur")
            result.append(line)
        elif stripped.startswith("except "):
            exc_type = stripped.split()[1] if len(stripped.split()) > 1 else "Exception"
            result.append(f"# Handle `{exc_type}` if raised in the try block above")
            result.append(line)
        elif stripped.startswith("finally:"):
            result.append("# Cleanup: this block always executes, regardless of exceptions")
            result.append(line)

        # with statement
        elif stripped.startswith("with "):
            ctx = stripped[5:].rstrip(":")
            result.append(f"# Context manager: automatically clean up `{ctx.split(' as ')[0].strip()}`")
            result.append(line)

        # Assignments
        elif "=" in stripped and not stripped.startswith("="):
            var_name = stripped.split("=")[0].strip()
            r_val = stripped.split("=", 1)[1].strip()
            if r_val.startswith("(") or r_val.startswith("["):
                result.append(f"# Initialize `{var_name}` as a collection")
            elif any(kw in r_val for kw in ("open(", "read(", "write(")):
                result.append(f"# Open a file handle and assign to `{var_name}`")
            elif r_val.startswith("lambda"):
                result.append(f"# Define an anonymous (lambda) function for `{var_name}`")
            elif any(kw in r_val for kw in ("cv2.", "np.", "pd.")):
                lib = "OpenCV" if "cv2." in r_val else "NumPy" if "np." in r_val else "Pandas"
                result.append(f"# Use {lib} library to compute `{var_name}`")
            else:
                result.append(f"# Compute and store the result in `{var_name}`")
            result.append(line)

        # All other code
        else:
            result.append(f"# {stripped}")
            result.append(line)

        prev_was_comment = False

    return "\n".join(result)


def _comment_for_import(module_name: str) -> str:
    """Return a short description for commonly imported modules."""
    descriptions = {
        "cv2": "computer vision (OpenCV)",
        "numpy": "numerical computing (NumPy)",
        "np": "numerical computing (NumPy)",
        "pandas": "data manipulation (Pandas)",
        "pd": "data manipulation (Pandas)",
        "matplotlib": "data visualization (Matplotlib)",
        "plt": "plotting (Matplotlib)",
        "tensorflow": "deep learning (TensorFlow)",
        "torch": "deep learning (PyTorch)",
        "sklearn": "machine learning (scikit-learn)",
        "requests": "HTTP requests",
        "flask": "web framework (Flask)",
        "fastapi": "web framework (FastAPI)",
        "django": "web framework (Django)",
        "streamlit": "data app framework (Streamlit)",
        "st": "Streamlit components",
        "os": "operating system interface",
        "sys": "system-specific parameters",
        "re": "regular expressions",
        "json": "JSON encoding/decoding",
        "csv": "CSV file reading/writing",
        "collections": "specialized container datatypes",
        "deque": "double-ended queue",
        "datetime": "date and time handling",
        "pathlib": "object-oriented filesystem paths",
        "typing": "type hint support",
        "math": "mathematical functions",
        "random": "random number generation",
        "time": "time access and conversions",
        "io": "stream handling",
        "base64": "base64 encoding/decoding",
        "hashlib": "hashing algorithms",
        "functools": "higher-order functions",
        "itertools": "iterator building blocks",
    }
    for key, desc in descriptions.items():
        if key in module_name.lower():
            return desc
    return f"the `{module_name}` library"


def chat_offline(message: str) -> str:
    """Provide keyword-aware conversational responses in offline mode."""
    m = message.lower().strip()

    # Greetings
    if _match(("hello", "hi ", "hey", "greetings", "good morning", "good evening"), m):
        return (
            "Hello! I'm VisionCode AI running in **offline mode**. I can help you with:\n\n"
            "1. **Generate Code** — Python solutions for common problems\n"
            "2. **Explain Code** — Breakdown of how code works\n"
            "3. **Debug Error** — Find and fix Python errors\n"
            "4. **Improve Code** — Refactor for performance & readability\n"
            "5. **Add Comments** — Document your code\n"
            "6. **CV Lab** — Real-time OpenCV image processing\n\n"
            "What would you like help with today?"
        )

    # Python / coding general
    if _match(("python", "coding", "programming", "language"), m):
        return (
            "Python is a versatile, beginner-friendly programming language widely used in:\n"
            "- **Web development** (Django, Flask, FastAPI)\n"
            "- **Data science & ML** (NumPy, Pandas, TensorFlow, PyTorch)\n"
            "- **Computer vision** (OpenCV, Pillow, scikit-image)\n"
            "- **Automation & scripting**\n"
            "- **Desktop apps** (Tkinter, PyQt, Streamlit)\n\n"
            "What specific aspect of Python would you like to explore?"
        )

    # OpenCV / CV questions
    if _match(("opencv", "cv2", "computer vision", "image processing", "canny", "contour", "feature detection"), m):
        return (
            "**OpenCV** is the leading open-source computer vision library. Here are common operations I can help with:\n\n"
            "- Read/display/save images: `cv2.imread()`, `cv2.imshow()`, `cv2.imwrite()`\n"
            "- Color conversions: `cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)`\n"
            "- Filtering: `cv2.GaussianBlur()`, `cv2.bilateralFilter()`\n"
            "- Edge detection: `cv2.Canny()`\n"
            "- Contour analysis: `cv2.findContours()`, `cv2.drawContours()`\n"
            "- Feature detection: face/eye Haar cascades, Hough transforms\n\n"
            "Visit the **CV Lab (Playground)** in the sidebar to try these interactively!"
        )

    # Streamlit
    if _match(("streamlit", "st."), m):
        return (
            "**Streamlit** is a fast way to build data apps in pure Python. Key elements:\n\n"
            "- `st.title()`, `st.header()`, `st.markdown()` — text\n"
            "- `st.image()`, `st.dataframe()`, `st.plotly_chart()` — media\n"
            "- `st.button()`, `st.slider()`, `st.selectbox()`, `st.text_input()` — widgets\n"
            "- `st.sidebar.*` — sidebar layout\n"
            "- `st.columns()`, `st.tabs()`, `st.expander()` — layout\n"
            "- `st.cache_data` / `st.cache_resource` — performance\n\n"
            "What Streamlit feature would you like to learn about?"
        )

    # Machine learning
    if _match(("machine learning", "ml", "deep learning", "neural network", "tensorflow", "pytorch", "model training"), m):
        return (
            "**Machine Learning** workflow typically involves:\n\n"
            "1. **Data preparation** — cleaning, splitting, normalization\n"
            "2. **Model selection** — regression, classification, clustering\n"
            "3. **Training** — fitting the model to data\n"
            "4. **Evaluation** — accuracy, precision, recall, loss curves\n"
            "5. **Deployment** — API, app, or embedded\n\n"
            "*Tip: Add an API key to get ML code examples generated by AI.*"
        )

    # Data structures & algorithms
    if _match(("algorithm", "time complexity", "space complexity", "big o", "data structure", "sorting", "searching"), m):
        return (
            "Common data structures and their typical time complexities:\n\n"
            "| Structure | Access | Search | Insert | Delete |\n"
            "|-----------|--------|--------|--------|--------|\n"
            "| Array | O(1) | O(n) | O(n) | O(n) |\n"
            "| Stack | O(n) | O(n) | O(1) | O(1) |\n"
            "| Queue | O(n) | O(n) | O(1) | O(1) |\n"
            "| Linked List | O(n) | O(n) | O(1) | O(1) |\n"
            "| Hash Table | O(1) | O(1) | O(1) | O(1) |\n"
            "| BST | O(log n) | O(log n) | O(log n) | O(log n) |\n\n"
            "Want a code example for any of these? Use the **Generate Code** feature!"
        )

    # Error / debugging
    if _match(("error", "bug", "fix", "debug", "exception", "traceback", "crash"), m):
        return (
            "Common Python errors and quick fixes:\n\n"
            "- **SyntaxError** — check colons, brackets, quotes\n"
            "- **NameError** — variable not defined; check spelling & scope\n"
            "- **TypeError** — wrong operation for the data type\n"
            "- **IndexError** — list index out of range\n"
            "- **KeyError** — dict key not found; use `.get()`\n"
            "- **FileNotFoundError** — path doesn't exist\n"
            "- **ZeroDivisionError** — divide by zero\n\n"
            "Use the **Debug Error** feature in the sidebar with a full traceback!"
        )

    # File I/O
    if _match(("file", "read", "write", "open", "csv", "json", "load", "save"), m):
        return (
            "File I/O in Python — quick reference:\n\n"
            "```python\n"
            "# Text file\n"
            "with open('file.txt', 'r') as f:\n"
            "    content = f.read()\n\n"
            "# CSV\n"
            "import csv\n"
            "with open('data.csv', 'r') as f:\n"
            "    reader = csv.DictReader(f)\n"
            "    for row in reader:\n"
            "        print(row)\n\n"
            "# JSON\n"
            "import json\n"
            "with open('data.json', 'r') as f:\n"
            "    data = json.load(f)\n"
            "```"
        )

    # Thank you / appreciation
    if _match(("thank", "thanks", "appreciate", "helpful", "great"), m):
        return "You're welcome! Feel free to ask if you need help with Python, OpenCV, or anything coding-related. Happy coding!"

    # Fallback for anything else
    return (
        "I'm running in **offline mode** without an AI API key. I can still help with:\n\n"
        "| Feature | What it does |\n"
        "|---------|--------------|\n"
        "| **Generate Code** | Python solutions (prime, sort, stack, graph, etc.) |\n"
        "| **Explain Code** | Analyzes functions, classes, loops, conditionals |\n"
        "| **Debug Error** | Identifies 10+ common exception types |\n"
        "| **Improve Code** | Refactors with type hints, error handling, f-strings |\n"
        "| **Add Comments** | Inserts detailed inline documentation |\n"
        "| **CV Lab** | Real-time OpenCV filters, edges, contours, face tracking |\n\n"
        f'You asked: *"{message}"*\n\n'
        "Try one of the features above, or add an OpenRouter API key in the sidebar for full AI-powered chat."
    )


def _analyze_image_properties(img: np.ndarray) -> dict[str, Any]:
    """Extract basic image properties."""
    h, w = img.shape[:2]
    is_grayscale = len(img.shape) == 2
    props = {
        "Dimensions": f"{w} × {h} px",
        "Aspect Ratio": f"{w / h:.2f}",
        "Color Mode": "Grayscale" if is_grayscale else "BGR Color",
        "Total Pixels": f"{h * w:,}",
    }
    if is_grayscale:
        props["Mean Brightness"] = f"{img.mean():.1f}"
        props["Std Dev (Contrast)"] = f"{img.std():.1f}"
    else:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        props["Mean Brightness (Luma)"] = f"{gray.mean():.1f}"
        props["Contrast (Std Dev)"] = f"{gray.std():.1f}"
    return props


def _analyze_edges(img: np.ndarray) -> dict[str, Any]:
    """Run Canny edge detection and return statistics."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img
    edges = cv2.Canny(gray, 50, 150)
    h, w = gray.shape
    edge_ratio = np.sum(edges > 0) / (h * w)
    return {
        "Edge Pixel %": f"{edge_ratio * 100:.1f}%",
        "Edge Density": f"{edge_ratio:.4f}",
        "Likely Content": (
            "Diagram / UI (high edges)"
            if edge_ratio > 0.08
            else "Photo / natural scene (moderate edges)"
            if edge_ratio > 0.02
            else "Uniform / flat region (low edges)"
        ),
    }


def _analyze_contours(img: np.ndarray) -> dict[str, Any]:
    """Detect contours and return shape statistics."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img
    edges = cv2.Canny(gray, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    areas = [cv2.contourArea(c) for c in contours]
    large_contours = sum(1 for a in areas if a > 500)
    return {
        "Total Contours": len(contours),
        "Contours > 500px²": large_contours,
        "Avg Area (all)": f"{np.mean(areas):.1f} px²" if areas else "N/A",
        "Max Area": f"{max(areas):.1f} px²" if areas else "N/A",
    }


def _analyze_colorfulness(img: np.ndarray) -> dict[str, Any]:
    """Estimate how colorful the image is."""
    if len(img.shape) == 2:
        return {"Colorfulness Score": "0.0 (Grayscale)"}
    b, g, r = cv2.split(img.astype(np.float32))
    rg = np.abs(r - g)
    yb = np.abs(0.5 * (r + g) - b)
    score = np.sqrt(rg.var() + yb.var()) + 0.3 * np.sqrt(rg.mean() + yb.mean())
    label = (
        "Very colorful"
        if score > 40
        else "Moderately colorful"
        if score > 20
        else "Muted / subdued"
    )
    return {"Colorfulness Score": f"{score:.1f}", "Verdict": label}


def _detect_blurriness(img: np.ndarray) -> dict[str, Any]:
    """Use Laplacian variance to detect blur."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    return {
        "Blur Score (Laplacian Var)": f"{laplacian_var:.1f}",
        "Sharpness": (
            "Sharp / in focus"
            if laplacian_var > 100
            else "Slightly blurry"
            if laplacian_var > 30
            else "Very blurry / out of focus"
        ),
    }


def _analyze_text_regions(img: np.ndarray) -> dict[str, Any]:
    """Use MSER + contours to estimate potential text regions in a screenshot."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img
    # Simple heuristic: dilated edge regions often indicate text
    edges = cv2.Canny(gray, 30, 100)
    dilated = cv2.dilate(edges, np.ones((2, 2), np.uint8), iterations=1)
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    text_candidates = 0
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        aspect = w / h
        area = cv2.contourArea(c)
        # Text-like regions tend to be small, dense, with moderate aspect ratios
        if area > 20 and area < 5000 and 0.2 < aspect < 10:
            text_candidates += 1
    return {"Potential Text Regions": text_candidates, "Screenshot Likelihood": "High" if text_candidates > 30 else "Moderate" if text_candidates > 10 else "Low"}


def _analyze_symmetry(img: np.ndarray) -> dict[str, Any]:
    """Check horizontal symmetry (common in UI layouts)."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img
    h, w = gray.shape
    left = gray[:, : w // 2]
    right = cv2.flip(gray[:, w // 2 + (w % 2) :], 1)
    if left.shape == right.shape:
        diff = cv2.absdiff(left, right).mean()
    else:
        diff = 255.0
    return {
        "Horizontal Symmetry Error": f"{diff:.1f} / 255",
        "UI Layout Likelihood": "Symmetric (likely UI)" if diff < 20 else "Asymmetric (natural / code)",
    }


def vision_offline(user_input: str, image_bytes: Optional[bytes] = None) -> str:
    """Analyze an image locally using OpenCV when no API key is available."""
    if image_bytes is None:
        return (
            "### 🔍 Offline CV Image Analysis\n\n"
            "Upload an image and I will analyze it using local OpenCV.\n"
            "For full AI-powered vision (OCR, diagram understanding, code extraction), "
            "add an OpenRouter API key in the sidebar."
        )

    try:
        pil_img = Image.open(BytesIO(image_bytes)).convert("RGB")
        img_bgr = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    except Exception as exc:
        return f"❌ Failed to load image: {exc}"

    lines = ["## 🔍 Local OpenCV Analysis (Offline)", ""]
    lines.append(f"**Your question:** _{user_input}_")
    lines.append("")
    lines.append("---")

    # 1. Basic properties
    lines.append("### 📐 Image Properties")
    for k, v in _analyze_image_properties(img_bgr).items():
        lines.append(f"- **{k}:** {v}")
    lines.append("")

    # 2. Colorfulness
    lines.append("### 🎨 Color Analysis")
    for k, v in _analyze_colorfulness(img_bgr).items():
        lines.append(f"- **{k}:** {v}")
    lines.append("")

    # 3. Edges
    lines.append("### ✏️ Edge & Structure Analysis")
    for k, v in _analyze_edges(img_bgr).items():
        lines.append(f"- **{k}:** {v}")
    lines.append("")

    # 4. Contours
    lines.append("### 🔘 Shape / Contour Analysis")
    for k, v in _analyze_contours(img_bgr).items():
        lines.append(f"- **{k}:** {v}")
    lines.append("")

    # 5. Blur detection
    lines.append("### 📷 Focus & Sharpness")
    for k, v in _detect_blurriness(img_bgr).items():
        lines.append(f"- **{k}:** {v}")
    lines.append("")

    # 6. Text region estimation
    lines.append("### 🔤 Text Region Detection")
    for k, v in _analyze_text_regions(img_bgr).items():
        lines.append(f"- **{k}:** {v}")
    lines.append("")

    # 7. Symmetry / UI layout
    lines.append("### 📐 Layout Symmetry")
    for k, v in _analyze_symmetry(img_bgr).items():
        lines.append(f"- **{k}:** {v}")
    lines.append("")

    # 8. Overall interpretation
    lines.append("### 💡 Overall Interpretation")
    h, w = img_bgr.shape[:2]
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    mean_b = gray.mean()
    edges = cv2.Canny(gray, 50, 150)
    edge_ratio = np.sum(edges > 0) / (h * w)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    areas = [cv2.contourArea(c) for c in contours]

    hints = []
    if w > 800 and h > 600:
        hints.append("📺 **Large image** — likely a screenshot or full UI layout.")
    else:
        hints.append("📱 **Small image** — likely a code snippet or cropped region.")

    if mean_b > 200:
        hints.append("☀️ **Very bright** — suggests a light-mode UI or photo with highlights.")
    elif mean_b < 50:
        hints.append("🌙 **Very dark** — suggests dark-mode code editor or low-light scene.")

    if edge_ratio > 0.1:
        hints.append("🏗️ **High edge density** — structured content like UI, diagram, or text.")
    elif edge_ratio > 0.03:
        hints.append("🌄 **Moderate edges** — natural scene or mixed content.")
    else:
        hints.append("🌫️ **Low edge density** — uniform area, gradient, or out-of-focus region.")

    large_shapes = sum(1 for a in areas if a > 2000)
    if large_shapes > 5:
        hints.append("🧩 **Multiple large objects detected** — dashboard, form, or multi-panel diagram.")
    elif large_shapes > 0:
        hints.append("🎯 **Few large objects** — single widget, modal, or focused content.")

    lines.extend(hints)
    lines.append("")
    lines.append("---")
    lines.append(
        "> ⚡ *For OCR text extraction, code generation from screenshots, or detailed diagram "
        "explanation, add an OpenRouter API key in the sidebar to switch to AI-powered mode.*"
    )

    return "\n".join(lines)


OFFLINE_HANDLERS: dict[str, Callable[..., str]] = {
    "generate": generate_code_offline,
    "explain": explain_code_offline,
    "debug": debug_error_offline,
    "improve": improve_code_offline,
    "comment": add_comments_offline,
    "chat": chat_offline,
    "vision": vision_offline,
}


def handle_offline(task: str, user_input: str, image_bytes: Optional[bytes] = None) -> str:
    """Dispatch to the appropriate offline handler."""
    handler = OFFLINE_HANDLERS.get(task)
    if handler is None:
        return "Offline mode: I can help with Python code generation, explanation, debugging, improvement, and comments."
    if task == "vision":
        return handler(user_input, image_bytes=image_bytes)
    return handler(user_input)