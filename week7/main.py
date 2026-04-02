import numpy as np
from splajn import Bezier
from bsplajn import Bspline 

def main():
    print("ahj")


    #body=np.array([[0,2],[1,3],[3,8],[4,7]])

    body_xy = np.array([
    [0, 0],
    [3, 5],
    [-3, 5],
    [0, 0]])
    
    #body_xy = np.array([
    #[0, 0],
    #[2, 3],
    #[4, -3],
    #[6, 0]
#])
    #stupen=3

    body = np.array([
        [0, 0],
        [3, 5],
        [-3, 5],
        [0, 0],
        [2, 8]
    ])

    stupen = 3

    uzlVektor = np.array([0, 0, 0, 0, 0.5, 1, 1, 1, 1])

    bspline = Bspline(body, stupen, uzlVektor)

    # test index
    t = 0.3
    print(f"Index pro t={t} je:", bspline.najdiIndexUzlu(t))

    bspline.vykresliKrivku()

    #bezier=Bezier(body,stupen)

    #bezierr=Bezier(body,stupen,vahy)
    #bezierr.vypisStupen()

    #bezierr.vykresliKrivku()

    


if __name__=="__main__":
    main()