import random as rdm

def create_Map(length, level):
    # create first block
    Map = [[100,50,0,0]]
    x = 0
    y = 0
    width = 100
    while (x + width) < length:
        d = level * 14 + int(80 * rdm.random())
        width = 200 - 35 * level + int((100 - level * 5) * rdm.random())
        height = 40+ int(20*rdm.random())
        x = Map[len(Map)-1][2] + d + Map[len(Map)-1][0]
        block = [width, height, x, y]
        Map.append(block)

    return Map


