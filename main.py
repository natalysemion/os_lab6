import random
import concurrent.futures
import time
import threading

n, m, k = 100, 100, 100
A = [[random.randint(0, 9) for _ in range(m)] for _ in range(n)]
B = [[random.randint(0, 9) for _ in range(k)] for _ in range(m)]
C = [[0] * k for _ in range(n)]
mtx = threading.Lock()

def compute_element(i, j):
    result = sum(A[i][x] * B[x][j] for x in range(m))
    with mtx:
       # print(f"Thread-{i * k + j + 1}: [{i},{j}]={result}")
        C[i][j] = result

def compute_segment(row):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for j in range(k):
            futures.append(executor.submit(compute_element, row, j))
        concurrent.futures.wait(futures)

def matrix_multiply_threads(num_threads):
    start = time.time()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(compute_segment, range(num_threads))
    finish = time.time()
    return finish - start


def task_1():
    thread_counts = [1, 10, 100, 500, 1000]
    for count in thread_counts:
        time_taken = matrix_multiply_threads(count)
        print(f" {count} threads: {time_taken} seconds.")

shared_variable = 0
mtx = threading.Lock()

def increment_without_lock(num_iterations):
    global shared_variable
    for _ in range(num_iterations):
        shared_variable += 1

def increment_with_lock(num_iterations):
    global shared_variable
    for _ in range(num_iterations):
        with mtx:
            shared_variable += 1

def task_2():
    num_iterations = 1000000

    # scenario 1: Without Lock
    global shared_variable
    shared_variable = 0
    thread1 = threading.Thread(target=increment_without_lock, args=(num_iterations,))
    thread2 = threading.Thread(target=increment_without_lock, args=(num_iterations,))
    start_time = time.time()
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    end_time = time.time()
    result_without_lock = shared_variable
    time_without_lock = end_time - start_time

    # reset shared variable
    shared_variable = 0

    # scenario 2: With Lock
    thread3 = threading.Thread(target=increment_with_lock, args=(num_iterations,))
    thread4 = threading.Thread(target=increment_with_lock, args=(num_iterations,))
    start_time = time.time()
    thread3.start()
    thread4.start()
    thread3.join()
    thread4.join()
    end_time = time.time()
    result_with_lock = shared_variable
    time_with_lock = end_time - start_time

    # output results
    print("\nResult without lock:", result_without_lock)
    print("Time:", time_without_lock, "seconds")
    print("Result with lock:", result_with_lock)
    print("Time:", time_with_lock, "seconds")

shared_variable = 0
mtx = threading.Lock()

def increment_with_batch(num_iterations, batch_size):
    global shared_variable
    local_sum = 0
    for _ in range(num_iterations):
        local_sum += 1
        if local_sum == batch_size:
            with mtx:
                shared_variable += local_sum
                local_sum = 0
    if local_sum > 0:
        with mtx:
            shared_variable += local_sum

def increment_without_lock_context_switch(num_iterations):
    global shared_variable
    for _ in range(num_iterations):
        value = shared_variable
        for _ in range(1000000):  # Emulating some computational work
            pass
        shared_variable = value + 1

def optimized_task_2():
    num_iterations = 1000000
    batch_size = 10000

    # Reset shared variable
    global shared_variable
    shared_variable = 0

    thread1 = threading.Thread(target=increment_with_batch, args=(num_iterations, batch_size))
    thread2 = threading.Thread(target=increment_with_batch, args=(num_iterations, batch_size))
    start_time = time.time()
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    end_time = time.time()
    result_with_batch = shared_variable
    time_with_batch = end_time - start_time

    # Output results
    print("\nResult with batched lock:", result_with_batch)
    print("Time:", time_with_batch, "seconds")
def fully_synchronized_task_2():
    num_iterations = 1000

    # scenario 1: Without Lock
    global shared_variable
    shared_variable = 0
    thread1 = threading.Thread(target=increment_without_lock_context_switch, args=(num_iterations,))
    thread2 = threading.Thread(target=increment_without_lock_context_switch, args=(num_iterations,))
    start_time = time.time()
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    end_time = time.time()
    result_without_lock = shared_variable
    time_without_lock = end_time - start_time

    print("\nResult:", result_without_lock)
    print("Time:", time_without_lock, "seconds")

if __name__ == "__main__":
    task_1()
    task_2()
    optimized_task_2()
    fully_synchronized_task_2()