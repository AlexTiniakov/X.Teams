import matplotlib.pyplot as plt
import numpy as np

def curve():
    a = 7
    b = 9

    x=np.arange(-2.0,6.0,0.003)
    f = plt.figure()
    sub = plt.subplot()
    sub.plot(x,(x ** 3 + a * x + b) ** 0.5, color="blue")
    sub.plot(x,-(x ** 3 + a * x + b) ** 0.5, color="blue")
    sub.grid(True)
    plt.show()
    f.savefig('./plot.png')

if __name__ == "__main__":
    curve()