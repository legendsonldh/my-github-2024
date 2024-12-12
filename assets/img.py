import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import CubicSpline

def plot_commits(data, xlabel, ylabel, title, xticks, xlim):
    if data[0] != data[-1]:
        data.append(data[0])
    x = np.arange(len(data))
    y = np.array(data)
    x_new = np.linspace(x.min(), x.max(), 300)
    cs = CubicSpline(x, y, bc_type='periodic')
    y_smooth = cs(x_new)
    plt.plot(x_new, y_smooth)
    plt.xticks(np.arange(0, xticks, 1))
    plt.xlim(0, xlim)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid()
    plt.show()

commits_hourly_num = [27, 16, 6, 3, 1, 0, 0, 0, 2, 1, 5, 11, 12, 25, 42, 46, 53, 70, 39, 37, 54, 41, 44, 50]
plot_commits(commits_hourly_num, 'Hour', 'Commits', 'Commits Hourly', 24, 24)

commits_monthly_num = [10, 0, 50, 60, 65, 109, 62, 4, 18, 50, 102, 55]
plot_commits(commits_monthly_num, 'Month', 'Commits', 'Commits Monthly', 12, 12)