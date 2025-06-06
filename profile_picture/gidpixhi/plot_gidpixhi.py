import csv
from pathlib import Path

import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from PIL import Image

DIRECTORY = Path(__file__).parent

# vertices, faces and cells taken from:
# https://polytope.miraheze.org/wiki/File:Omnitruncated_hecatonicosachoron.off
vertices = np.loadtxt(DIRECTORY / 'vertices.csv', delimiter=',')

with open(DIRECTORY / 'faces.csv', 'r') as f:
    reader = csv.reader(f, delimiter=',')
    faces = list(list(map(int, line)) for line in reader)

with open(DIRECTORY / 'cells.csv', 'r') as f:
    reader = csv.reader(f, delimiter=',')
    cells = list(list(map(int, line)) for line in reader)

destination = DIRECTORY / 'gidpixhi.png'

radius = 13
vertices_projected = vertices[:, :3] / (radius - vertices[:, 3:])

colors = {4: 'red', 6: 'green', 10: 'blue'}

if __name__ == '__main__':
    fig = plt.figure(figsize=(24, 24), dpi=300)
    ax = fig.add_subplot(projection='3d', azim=10, elev=30)

    for c in cells:
        if len(c) == 62:
            face = Poly3DCollection(
                [vertices_projected[list(faces[i])] for i in c],
                facecolors=[colors[len(faces[i])] for i in c],
                alpha=0.2, edgecolors='black'
            )
            ax.add_collection(face)

    xmin, ymin, zmin = vertices_projected.min(axis=0)
    xmax, ymax, zmax = vertices_projected.max(axis=0)
    ax.set_xlim((xmin, xmax))
    ax.set_ylim((ymin, ymax))
    ax.set_zlim((zmin, zmax))
    ax.set_aspect('equal')
    ax.set_axis_off()
    plt.savefig(destination, bbox_inches='tight', pad_inches=0, transparent=True)
    image = Image.open(destination)
    image_cropped = image.crop(image.getbbox())
    image_cropped.save(destination)
