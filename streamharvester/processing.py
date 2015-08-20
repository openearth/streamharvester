import matplotlib.pyplot as plt

from .conventions import generate_filename

def process(img, info):
    filename = generate_filename(info)
    plt.imsave(filename, img)
