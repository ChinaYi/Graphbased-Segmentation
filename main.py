from PIL import Image
import sys
from graph import build_graph, segment_graph
from smooth_filter import gaussian_grid, filter_image
from random import random
from numpy import sqrt

def diff_rgb(img, x1, y1, x2, y2):
    '''
        return distance among (x1, y1)(x2, y2) for RGB pic
    '''
    r = (img[0][x1, y1] - img[0][x2, y2]) ** 2
    g = (img[1][x1, y1] - img[1][x2, y2]) ** 2
    b = (img[2][x1, y1] - img[2][x2, y2]) ** 2
    return sqrt(r + g + b)

def diff_grey(img, x1, y1, x2, y2):
    '''
        return distance among (x1, y1)(x2, y2) for grey pic
    '''
    v = (img[x1, y1] - img[x2, y2]) ** 2
    return sqrt(v)

def threshold(size, const):
    '''
        rectify function
    '''
    return (const / size)


def generate_image(forest, width, height):
    random_color = lambda: (int(random()*255), int(random()*255), int(random()*255))
    colors = [random_color() for i in range(width*height)]

    img = Image.new('RGB', (width, height))
    im = img.load()
    for y in range(height):
        for x in range(width):
            comp = forest.find(y * width + x)
            im[x, y] = colors[comp]

    return img.transpose(Image.ROTATE_270).transpose(Image.FLIP_LEFT_RIGHT)



if __name__ == '__main__':
    neighbor = 8
       

    image_file = Image.open("test.jpg")
    sigma = 0.8
    #K = 300
    #K = 10
    #K = 50   
    K = 500
    min_size = 5
    size = image_file.size

    grid = gaussian_grid(sigma)

    if image_file.mode == 'RGB':
        image_file.load()
        r, g, b = image_file.split()

        r = filter_image(r, grid)
        g = filter_image(g, grid)
        b = filter_image(b, grid)

        smooth = (r, g, b)
        diff = diff_rgb
    else:
        smooth = filter_image(image_file, grid)
        diff = diff_grey

    graph = build_graph(smooth, size[1], size[0], diff, neighbor == 8)
    forest = segment_graph(graph, size[0]*size[1], K, min_size, threshold)

    image = generate_image(forest, size[1], size[0])
    image.show()
