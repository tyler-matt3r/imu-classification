from memory_profiler import memory_usage
import time

def memory_profile(repetitions):
    def decorator(func):
        def wrapper(*args, **kwargs):
            mem_usages = []

            for _ in range(repetitions):
                start_mem = memory_usage(-1, interval=0.1, timeout=None)[0]
                result = func(*args, **kwargs)
                end_mem = memory_usage(-1, interval=0.1, timeout=None)[0]

                mem_usage = end_mem - start_mem
                mem_usages.append(mem_usage)

            average_mem_usage = sum(mem_usages) / repetitions
            print(f"Average memory usage (over {repetitions} runs): {average_mem_usage:.6f} MiB")
            return result

        return wrapper
    return decorator

def inference_profile(repetitions):
    def decorator(func):
        def wrapper(*args, **kwargs):
            elapsed_times = []
            for _ in range(repetitions):
                start_time = time.perf_counter()
                result = func(*args, **kwargs)
                end_time = time.perf_counter()

                elapsed_time = end_time - start_time
                elapsed_times.append(elapsed_time)

            average_elapsed_time = sum(elapsed_times) / repetitions
            print(f"Average inference speed (over {repetitions} runs): {average_elapsed_time:.6f} seconds")
            return result
        return wrapper
    return decorator