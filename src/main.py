import defs, time, tracemalloc, sys

sys.setrecursionlimit(1000000)

SIZE = [10, 500, 1000, 50000, 1000000]
ALGOTH = {
    'Bubble': defs.bubble_sort,
    'Selection': defs.selection_sort,
    'Insertion': defs.insertion_sort,
    'Quick': defs.quick_sort,
    'Merge': defs.merge_sort,
    'Heap': defs.heap_sort,
    'Counting': defs.counting_sort,
    'Radix': defs.radix_sort,
    'Bucket': defs.bucket_sort,
    'Built-in': lambda x: x.sort()
}

def test_algorithm(arr, algo_func):
    #Запускает алгоритм на копии списка
    tracemalloc.start()
    copy = arr.copy()
    start = time.perf_counter()
    algo_func(copy)
    elapsed = time.perf_counter() - start
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return elapsed, peak

def main():
    alg_names = list(ALGOTH.keys())
    #Первая строка
    header = ["Size", "Type"]
    for alg in alg_names:
        header.append(f"{alg} Time (s)")
        header.append(f"{alg} Mem (KB)")
    #
    with open("results.md", "w") as f:
        f.write("| " + " | ".join(header) + " |\n")

        for size in SIZE:
            datasets = {
                'Random': defs.gen_rand(size),
                'Sorted': defs.gen_sort(size),
                'Reversed': defs.gen_rev(size),
                'Almost Sorted': defs.gen_a_sort(size)
            }

            for type_name, data in datasets.items():
                row = [str(size), type_name]

                for alg_name in alg_names:
                    timet, peak = test_algorithm(data, ALGOTH[alg_name])
                    memkb = peak / 1024.0
                    row.append(f"{timet:.6f}")
                    row.append(f"{memkb:.2f}")

                f.write("| " + " | ".join(row) + " |\n")

    print("Run plot_resuts.py")

if __name__ == "__main__":
    main()
