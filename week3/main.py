import numpy as np
from cv3_point_circ_check import point_in_circle as pic

def main():
    A = (0, 0)
    B = (1, 0)
    C = (0, 1)
    P = (0.7,0.8)
    print(pic(A,B,C,P))

if __name__ == "__main__":
    main()