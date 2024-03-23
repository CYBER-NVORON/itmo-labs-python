import numpy as np
from time import perf_counter
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pylab
from functools import partial

def base_multiply(arr_1, arr_2):
    return [x * y for x, y in zip(arr_1, arr_2)]


def task_1():
    print("Задание 1:")

    arr_1 = [np.random.randint(0, 1_000_000) for _ in range(1_000_000)]
    arr_2 = np.array([np.random.randint(0, 1_000_000) for _ in range(1_000_000)])
    
    numpy_start = perf_counter()
    np.multiply(arr_1, arr_2)
    numpy_time = perf_counter() - numpy_start
    
    base_start = perf_counter()
    base_multiply(arr_1, arr_2)
    base_time = perf_counter() - base_start

    print(  f"Время затраченное на перемножение через функцию NumPy: {numpy_time}",
            f"Время затраченное на перемножение через обычный перебор: {base_time}",
            f"Разница: {abs(base_time - numpy_time)}", sep="\n")


def task_2():
    print("Задание 2:")

    arr = np.genfromtxt('data2.csv', delimiter = ',')
    arr = [arr[i][3] for i in range(len(arr))]
    chloramines = arr[1:]

    pylab.subplot (2, 2, 1)
    pylab.hist(chloramines, 25)
    pylab.title ("Гистограма")

    pylab.subplot (2, 2, 2)
    pylab.hist(chloramines, 25, density = True)
    pylab.title("Нормализованная гистограмма")

    print(f"Среднеквадратичное отклонение: {np.std(chloramines)}")

    pylab.show()


def task_3():
    print("Задание 3:")
    
    xs = np.linspace(-3*np.pi, 3*np.pi)
    ys = np.cos(xs)
    zs = xs / np.sin(xs)
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(xs, ys, zs, color='green')
    ax.set_title("3d")
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    plt.show()


def animation_function(num, ax, ani_array):
    ax.clear()
    
    ax.plot3D(ani_array[0, :num+1], 
              ani_array[1, :num+1],
              ani_array[2, :num+1], 
              c='blue')
    ax.scatter(ani_array[0,num],
               ani_array[1, num],
               ani_array[2, num],
               c='blue',
               marker='o')
    ax.plot3D(ani_array[0, 0],
              ani_array[1, 0],
              ani_array[2, 0],
              c='black',
              marker='o')

    ax.set_xlim3d([-3*np.pi, 3*np.pi])
    ax.set_ylim3d([-1, 1])
    ax.set_zlim3d([-10, 10])


def extra_task():
    print("Дополнительное задание:")
    
    xs = np.linspace(-3*np.pi, 3*np.pi)
    ys = np.sin(xs)
    zs = xs * 0

    fig = plt.figure()
    ax = plt.axes(projection='3d')
    
    ani_fun = partial(animation_function,
                      ax = ax, 
                      ani_array = np.array([xs, ys, zs]))
    
    line =  FuncAnimation(fig, ani_fun, interval=100, frames = len(xs))
    plt.show()


if __name__ == "__main__":
    print("Вариант 8")
    task_1()
    task_2()
    task_3()
    extra_task()