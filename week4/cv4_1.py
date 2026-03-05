import sys
sys.path.append(r'C:\Users\Jakub Osička\Desktop\vut\SVD\week4C:\diplomka')
from calcDel import trian_2D
def main():
    points_list  = []

    while True:
        s = input("Input 2 numbers or X for exit: ")
        if s  == "X":
            break
        point = [float(v) for v in s.split()]
        points_list.append(point)

        points_array = np.array(points_list)

    trian_2D(points_array)


if __name__ == "__main__":
    main()