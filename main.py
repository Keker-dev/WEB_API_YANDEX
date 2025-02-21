import sys
from geocoder import *
from Image_map import *

if __name__ == "__main__":
    toponym_find = " ".join(sys.argv[1:])
    if toponym_find:
        coords, spn = get_coordinates(toponym_find)
        show_map(*coords, spn)
    else:
        print("No data")
