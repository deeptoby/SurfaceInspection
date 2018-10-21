import numpy as np

def show_projection(meshs, dim, where):
    import matplotlib.pyplot as plt
    array = []
    for m in meshs:
        for v in m.vertices:
            array.append([v[0], v[1], v[2]])
    arr = np.array(array)
    if dim == 2:
        plt.scatter(arr[:, where[0]], arr[:, where[1]])
    else:
        ax = plt.subplot(111, projection='3d')
        from mpl_toolkits.mplot3d import Axes3D
        ax.scatter(arr[:, 0], arr[:, 1], arr[:, 2])
        ax.set_zlabel('Z')  # 坐标轴
        ax.set_ylabel('Y')
        ax.set_xlabel('X')
    plt.show()