""" benchmarking the amount of time it takes to run DTW for
    a single instance (i.e. one dimension).
    Will want to multiply the time taken by 6 if we use all
    dimensions.
"""


import numpy as np
from fastdtw import fastdtw
from profile_utils import memory_profile, inference_profile
from scipy.spatial.distance import euclidean


def create_sample_data(time_length):
    times = np.linspace(0, 8, time_length * 30)  # seconds sampled at 30 Hz
    randoms = 20 * np.random.randn(6, 3)
    data = {'time (s)': times}
    data.update(
        {
            key: randoms[i, 0] * np.sin(times + randoms[i, 1] + randoms[i, 2])
            for i, key in enumerate(
                ['lr_acc(m/s^2)', 'bf_acc(m/s^2)', 'vert_acc(m/s^2)',
                    'lr_w(rad/s)', 'bf_w(rad/s)', 'vert_w(rad/s)']
            )
        }
    )
    return data

# @memory_profile(1)
@inference_profile(10)
def benchmark_dtw(data_0, data_1):
    x = np.column_stack((data_0['time (s)'], data_0['lr_acc(m/s^2)']))
    y = np.column_stack((data_1['time (s)'], data_1['lr_acc(m/s^2)']))
    distance, path = fastdtw(x, y, dist=euclidean)

if __name__ == "__main__":

    for time_window in range(6,15,2):
        print(f"benchmarking dynamic time warping for {time_window} second window")
        # generate some sample data
        data_0 = create_sample_data(8)
        data_1 = create_sample_data(time_window)
        benchmark_dtw(data_0, data_1)