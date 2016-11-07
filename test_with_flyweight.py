import pygame
import sys
from pympler import asizeof
import weakref
from datetime import datetime

screen = pygame.display.set_mode((320, 320), 0, 32)
bg_color = (0, 0, 0)
mainloop = True

size = 20


class FlyWeightMeta(type):

    def __new__(mcs, name, parents, dct):
        dct['pool'] = weakref.WeakValueDictionary()
        return super(FlyWeightMeta, mcs).__new__(mcs, name, parents, dct)

    @staticmethod
    def _serialize_params(cls, *args, **kwargs):

        args_list = map(str, args)
        args_list.extend([str(kwargs), cls.__name__])
        key = ''.join(args_list)
        return key

    def __call__(cls, *args, **kwargs):
        key = FlyWeightMeta._serialize_params(cls, *args, **kwargs)
        pool = getattr(cls, 'pool', {})

        instance = pool.get(key)
        if not instance:
            instance = super(FlyWeightMeta, cls).__call__(*args, **kwargs)
            pool[key] = instance
        return instance


class Pixel:

    __metaclass__ = FlyWeightMeta

    def __init__(self, color='white'):

        if color is 'white':
            self.color = (255, 255, 255)
        elif color is 'black':
            self.color = (0, 0, 0)
        elif color is 'red':
            self.color = (247, 21, 45)


pixel_color_list = [
    Pixel(), Pixel(), Pixel(), Pixel(), Pixel(), Pixel('black'),
    Pixel('black'), Pixel('black'), Pixel('black'), Pixel('black'),
    Pixel('black'), Pixel(), Pixel(), Pixel(), Pixel(), Pixel(),

    Pixel(), Pixel(), Pixel(), Pixel('black'), Pixel('black'),
    Pixel('red'), Pixel('red'), Pixel('red'), Pixel('red'),
    Pixel(), Pixel(), Pixel('black'), Pixel('black'), Pixel(),
    Pixel(), Pixel(),

    Pixel(), Pixel(), Pixel('black'), Pixel(), Pixel(),
    Pixel('red'), Pixel('red'), Pixel('red'), Pixel('red'),
    Pixel(), Pixel(), Pixel(), Pixel(), Pixel('black'), Pixel(),
    Pixel(),

    Pixel(), Pixel('black'), Pixel(), Pixel(), Pixel('red'),
    Pixel('red'), Pixel('red'), Pixel('red'), Pixel('red'), Pixel('red'),
    Pixel(), Pixel(), Pixel(), Pixel(), Pixel('black'), Pixel(),

    Pixel(), Pixel('black'), Pixel(), Pixel('red'), Pixel('red'),
    Pixel(), Pixel(), Pixel(), Pixel(), Pixel('red'),
    Pixel('red'), Pixel(), Pixel(), Pixel(), Pixel('black'), Pixel(),

    Pixel('black'), Pixel('red'), Pixel('red'), Pixel('red'),
    Pixel(), Pixel(), Pixel(), Pixel(), Pixel(), Pixel(),
    Pixel('red'), Pixel('red'), Pixel('red'), Pixel('red'), Pixel('red'),
    Pixel('black'),

    Pixel('black'), Pixel('red'), Pixel('red'), Pixel('red'),
    Pixel(), Pixel(), Pixel(), Pixel(), Pixel(), Pixel(),
    Pixel('red'), Pixel('red'), Pixel(), Pixel(), Pixel('red'),
    Pixel('black'),

    Pixel('black'), Pixel(), Pixel('red'), Pixel('red'),
    Pixel(), Pixel(), Pixel(), Pixel(), Pixel(), Pixel(),
    Pixel('red'), Pixel(), Pixel(), Pixel(), Pixel(),
    Pixel('black'),

    Pixel('black'), Pixel(), Pixel(), Pixel('red'),
    Pixel('red'), Pixel(), Pixel(), Pixel(), Pixel(), Pixel('red'),
    Pixel('red'), Pixel(), Pixel(), Pixel(), Pixel(),
    Pixel('black'),

    Pixel('black'), Pixel(), Pixel(), Pixel('red'),
    Pixel('red'), Pixel('red'), Pixel('red'), Pixel('red'), Pixel('red'),
    Pixel('red'), Pixel('red'), Pixel('red'), Pixel(), Pixel(), Pixel('red'),
    Pixel('black'),

    Pixel('black'), Pixel(), Pixel('red'), Pixel('red'),
    Pixel('black'), Pixel('black'), Pixel('black'), Pixel('black'),
    Pixel('black'), Pixel('black'), Pixel('black'), Pixel('black'),
    Pixel('red'), Pixel('red'), Pixel('red'), Pixel('black'),

    Pixel(), Pixel('black'), Pixel('black'), Pixel('black'),
    Pixel(), Pixel(), Pixel('black'), Pixel(),
    Pixel(), Pixel('black'), Pixel(), Pixel(), Pixel('black'),
    Pixel('black'), Pixel('black'), Pixel(),

    Pixel(), Pixel(), Pixel('black'), Pixel(),
    Pixel(), Pixel(), Pixel('black'), Pixel(),
    Pixel(), Pixel('black'), Pixel(), Pixel(), Pixel(),
    Pixel('black'), Pixel(), Pixel(),

    Pixel(), Pixel(), Pixel('black'), Pixel(),
    Pixel(), Pixel(), Pixel(), Pixel(),
    Pixel(), Pixel(), Pixel(), Pixel(), Pixel(),
    Pixel('black'), Pixel(), Pixel(),

    Pixel(), Pixel(), Pixel(), Pixel('black'),
    Pixel(), Pixel(), Pixel(), Pixel(),
    Pixel(), Pixel(), Pixel(), Pixel(), Pixel('black'),
    Pixel(), Pixel(), Pixel(),

    Pixel(), Pixel(), Pixel(), Pixel(),
    Pixel('black'), Pixel('black'), Pixel('black'), Pixel('black'),
    Pixel('black'), Pixel('black'), Pixel('black'), Pixel('black'), Pixel(),
    Pixel(), Pixel(), Pixel(),

]

startTime = datetime.now()

current_x = 0
current_y = 0

screen.fill(bg_color)

for event in pygame.event.get():
    if event.type == pygame.QUIT:
        sys.exit()

count = 0

for pixel in pixel_color_list:

    if count == 16:
        current_y += size
        current_x = 0
        count = 0

    if count > 0:
        current_x += size

    pygame.draw.rect(screen, pixel.color, (current_x, current_y, size, size))

    count += 1

pygame.display.flip()
pygame.time.delay(1000)

print(asizeof.asizeof(pixel_color_list))
print(datetime.now() - startTime)

instances_pool = getattr(Pixel, 'pool')
print(len(instances_pool))
