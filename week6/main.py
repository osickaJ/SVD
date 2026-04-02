import cv2
import matplotlib.pyplot as plt
from marching_squares import Grid, MarchingSquares

def main():
    img = cv2.imread("testImage.jpg", cv2.IMREAD_GRAYSCALE)
    im2fl = img.astype(float).tolist()
    grid = Grid(im2fl)
    segments = MarchingSquares(grid, thr=128).extract()

    def plot_segments(ax, segments):
        for (x1, y1), (x2, y2) in segments:
            ax.plot([x1, x2], [y1, y2], color="red", linewidth=0.8)

    _, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))

    ax1.set_title("Contours only")
    ax1.invert_yaxis()
    ax1.set_aspect("equal")
    plot_segments(ax1, segments)

    ax2.set_title("Contours on the original image")
    ax2.imshow(img, cmap="gray")
    plot_segments(ax2, segments)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()