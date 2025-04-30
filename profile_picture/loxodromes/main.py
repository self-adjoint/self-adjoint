from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

filename = Path(__file__).parent / 'loxodromes.png'

if __name__ == '__main__':
    fig = plt.figure(figsize=(20, 20), dpi=300)
    ax = fig.add_subplot(projection='3d')
    lat = np.linspace(-np.pi / 2, np.pi / 2, 128)  # Latitude
    long = np.linspace(0, 2 * np.pi, 256)  # Longitude
    Lat, Long = np.meshgrid(lat, long)
    X = np.cos(Lat) * np.cos(Long)
    Y = np.cos(Lat) * np.sin(Long)
    Z = np.sin(Lat)

    bearing = np.pi / 3
    color_numbers = ((Long - np.tan(bearing) * np.asinh(np.tan(Lat))) / (2 * np.pi)) % 1
    colors = plt.cm.hsv(color_numbers)
    ax.plot_surface(X, Y, Z, facecolors=colors, antialiased=False)

    shifts = np.array([-5/8, -1/8, 3/8, 7/8]) * np.pi
    starting_lats = np.array([-1/12, -1/4, 7/24, 1/8]) * np.pi

    for shift, start in zip(shifts, starting_lats, strict=True):
        lats = np.linspace(start, np.pi / 2, 1000)
        loxs = np.tan(bearing) * np.asinh(np.tan(lats)) + shift
        xs = np.cos(lats) * np.cos(loxs)
        ys = np.cos(lats) * np.sin(loxs)
        zs = np.sin(lats)
        ax.plot3D(xs, ys, zs, color='silver', zorder=3)

    ax.set_xlim((-1, 1))
    ax.set_ylim((-1, 1))
    ax.set_zlim((-1, 1))
    ax.set_aspect('equal')
    ax.set_axis_off()

    plt.savefig(filename, bbox_inches='tight', pad_inches=0, transparent=True)
    image = Image.open(filename)
    image_cropped = image.crop(image.getbbox())
    image_cropped.save(filename)
    width, height = image_cropped.size
    print(f'Created image ({width} \u00D7 {height} pixels)')
    print(f'Saved to {filename}')
