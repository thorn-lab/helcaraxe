import matplotlib.pyplot as plt
import numpy as np

def sigmoid():
    x = np.linspace(-5, 5, 1000)

    y = 1 / (1 + np.exp(-x))
    y_r = np.maximum(0, x)
    y_e = np.exp(x)-1

    fig, ax = plt.subplots()
    ax.set_axisbelow(True)
    ax.set_ylim([-1, 2])
    ax.set_xlim([-4, 4])
    ax.xaxis.grid(color="gray", linestyle="dashed")
    ax.yaxis.grid(color="gray", linestyle="dashed")
    ax.plot(x, y, label='sigmoid', color="steelblue", lw=3)
    ax.plot(x, y_r, label='ReLu', color="darkslateblue", lw=3)
    ax.plot(x, y_e, label='eLu', color="darkseagreen",linestyle="dashed", lw=3)

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('f(x)')
    ax.set_xlabel('x')
    ax.set_xticks(np.arange(start=-4, stop=4, step=2))
    ax.set_yticks([-1,0,1,2])
    ax.legend()
    plt.plot(x, y)
    plt.axhline(lw=1, c='black')
    plt.axvline(lw=1, c='black')
    plt.savefig("Activation_functions.svg")
    plt.show()

def fig3_modelfitting():
    plt.rcParams.update({'font.size': 14})
    fig, ax= plt.subplots()
    x = np.arange(start=0,stop=6,step=1)
    y = [1,2.8,2.3,4.8,5.3,5.9]
    y_line = np.array([1,1,1,1,1,1])
    ax.scatter(x,y, color="darkseagreen", edgecolor="black", s=90, label="Data points")
    ax.plot(x,y_line, color="steelblue", lw=4, label="Model")

    ax.set_ylabel("Output variable")
    ax.set_xlabel("Input variable")
    ax.set_xticks([1, 2, 3, 4])
    ax.set_yticks([1, 3, 5,7])
    ax.set_ylim([0, 8])
    ax.set_xlim([0.5, 4.5])
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.legend()
    plt.show()

    fig, ax = plt.subplots()
    ax.scatter(x, y, color="darkseagreen",edgecolor="black",s=90, label="Data points")
    ax.plot(x, x + y_line, color="steelblue", lw=4,label="Model")

    ax.set_ylabel("Output variable")
    ax.set_xlabel("Input variable")
    ax.set_xticks([1,2,3,4])
    ax.set_yticks([1, 3, 5,7])
    ax.set_ylim([0, 8])
    ax.set_xlim([0.5, 4.5])
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.legend()
    plt.show()

def over_underfitting ():
    plt.rcParams.update({'font.size': 14})
    fig, ax = plt.subplots()
    x = [0.1,0.5,1.2,  2,  2.5, 3,   3.5,   4,4.5, 5]
    y = [0.5, 2,5 , 5, 7,  6, 4.6, 5.3, 3.9,1.5]
    ax.scatter(x, y, color="darkseagreen", edgecolor="black", s=90, label="Data points")

    z = np.polyfit(x, y, 1)
    y_hat = np.poly1d(z)(x)
    ax.plot(x, y_hat,color="steelblue", lw=4, label="Model")

    ax.set_ylabel("Output variable")
    ax.set_xlabel("Input variable")
    ax.set_xticks([0, 1, 2, 3, 4, 5])
    ax.set_yticks([0, 2, 4, 6, 8])
    ax.set_xlim([0, 5.1])

    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.legend()
    plt.title("Underfit")
    plt.savefig("under_fitting.svg")
    plt.show()

    fig, ax = plt.subplots()
    ax.scatter(x, y, color="darkseagreen", edgecolor="black", s=90, label="Data points")

    z = np.polyfit(x, y, 2)
    y_hat = np.poly1d(z)(x)
    ax.plot(x, y_hat,color="steelblue", lw=4, label="Model")

    ax.set_ylabel("Output variable")
    ax.set_xlabel("Input variable")
    ax.set_xticks([0, 1, 2, 3, 4, 5])
    ax.set_yticks([0, 2, 4, 6, 8])
    ax.set_xlim([-0.1, 5.1])


    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.legend()
    plt.title("Optimal")
    plt.savefig("optimal_fitting.svg")
    plt.show()

    fig, ax = plt.subplots()
    ax.scatter(x, y, color="darkseagreen", edgecolor="black", s=90, label="Data points")

    z = np.poly1d(np.polyfit(x, y, 10))
    y_hat = np.poly1d(z)(x)
    ax.plot(x, y_hat, color="steelblue", lw=4, label="Model")

    ax.set_ylabel("Output variable")
    ax.set_xlabel("Input variable")
    ax.set_xticks([0, 1, 2, 3, 4, 5])
    ax.set_yticks([0, 2, 4, 6, 8])
    ax.set_xlim([-0.1, 5.1])

    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.legend()
    plt.title("Overfit")
    plt.savefig("over_fitting.svg")
    plt.show()

