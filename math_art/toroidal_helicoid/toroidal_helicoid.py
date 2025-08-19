import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

destination = '../'


def create_toroidal_helicoid_plot(n):
    """ Create a plot of a helicoid wrapped around a torus, with n half-twists """
    destination = f'../{n}.png'
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    r = np.linspace(-1, 1, 1000)
    theta = np.linspace(-np.pi, np.pi, 1000)
    radius = 2
    R, Theta = np.meshgrid(r, theta)
    X = (radius + R * np.cos(n / 2 * Theta)) * np.cos(Theta)
    Y = (radius + R * np.cos(n / 2 * Theta)) * np.sin(Theta)
    Z = R * np.sin(n / 2 * Theta)
    ax.plot_surface(X, Y, Z, cmap='jet')
    ax.set_aspect('equal')
    ax.set_axis_off()
    plt.savefig(destination, bbox_inches='tight', pad_inches=0, transparent=True)
    image = Image.open(destination)
    image_cropped = image.crop(image.getbbox())
    image_cropped.save(destination)


if __name__ == '__main__':
    for n in range(1, 6):
        create_toroidal_helicoid_plot(n)