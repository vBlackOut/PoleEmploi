#!/usr/bin/python
import numpy as np
import cv2

# size 700*700
number_detect_phantomjs = { 0:   [[21, 28], [22, 29], 
                                  [25, 29], [26, 28],
                                  [25, 29], [22, 29],
                                  [27, 26], [20, 26],
                                  [27, 21], [20, 21],
                                  [22, 18], [21, 19],
                                  [22, 18], [25, 18],
                                  [26, 19], [25, 18]],

                            1:   [24, 18],

                            2:   [[20, 29], [21, 29],
                                  [26, 24], [24, 26],
                                  [25, 18], [27, 20],
                                  [27, 22], [27, 20],
                                  [22, 18]],

                            3:   [[24, 29], [21, 29],
                                  [22, 29], [26, 28],
                                  [26, 23], [24, 22],
                                  [26, 18]],

                            4:   [[26, 27],
                                  [27, 27],[20, 26],
                                  [24, 21],[22, 23],
                                  [26, 18],[26, 19]],

                            5:   [[24, 29], [21, 29],
                                  [22, 29], [26, 28],
                                  [26, 23], [21, 22],
                                  [24, 22], [21, 18]],

                            6:   [[26, 23], [27, 24],
                                  [27, 27], [25, 29],
                                  [27, 27], [27, 24],
                                  [23, 22], [24, 22],
                                  [20, 22], [20, 27],
                                  [22, 29], [20, 27],
                                  [20, 24], [21, 23],
                                  [23, 18], [21, 20],
                                  [23, 18], [24, 18]],

                            7:   [[22, 29], [23, 27],
                                  [24, 24], [24, 25],
                                  [25, 22], [26, 20],
                                  [26, 18]],

                            8:   [[27, 25], [27, 27],
                                  [25, 29], [27, 27],
                                  [20, 25], [20, 27],
                                  [22, 29], [20, 27],
                                  [22, 21], [22, 22],
                                  [21, 23], [22, 22],
                                  [25, 22], [26, 23],
                                  [25, 22], [25, 21],
                                  [24, 22], [23, 22],
                                  [25, 18], [22, 18]],

                            9:   [[26, 27], [24, 29],
                                  [23, 29], [24, 29],
                                  [23, 25], [24, 25],
                                  [25, 18], [27, 20],
                                  [27, 23], [26, 24],
                                  [27, 25], [27, 20],
                                  [22, 18], [20, 20],
                                  [20, 23], [21, 24],
                                  [20, 23], [20, 20]]
                          }

# size 1600*900
number_detect_firefox = { 0:   [[26, 28], [25, 29],
                                [21, 28], [22, 29],
                                [27, 25], [27, 26],
                                [20, 25], [20, 26],
                                [27, 21], [27, 22],
                                [20, 21], [20, 22],
                                [25, 18], [26, 19],
                                [22, 18], [21, 19]],


                          1:   [[24, 18], [23, 19],
                                [24, 18], [25, 19],
                                [25, 29], [25, 18]],

                          2:   [[20, 29], [21, 29],
                                [26, 24], [24, 26],
                                [27, 21], [27, 22],
                                [25, 18], [26, 19],
                                [22, 18]],


                           3:   [[21, 29], [24, 29],
                                 [26, 28], [26, 23],
                                 [24, 22], [26, 18]],


                           4:   [[20, 26], [20, 27],
                                 [27, 27], [21, 27],
                                 [24, 21], [22, 23],
                                 [26, 18], [26, 19]],

                           5:   [[24, 29], [21, 29],
                                 [22, 29], [26, 28],
                                 [26, 23], [21, 22],
                                 [24, 22], [21, 18]],

                           6:   [[26, 23], [27, 24],
                                 [27, 27], [25, 29],
                                 [27, 27], [27, 24],
                                 [23, 22], [24, 22],
                                 [20, 22], [20, 27],
                                 [22, 29], [20, 27],
                                 [20, 24], [21, 23],
                                 [23, 18], [21, 20],
                                 [23, 18], [24, 18]],

                           7:   [[22, 29], [23, 27],
                                 [24, 24], [24, 25],
                                 [25, 22], [26, 20]],

                           8:   [[27, 25], [27, 27],
                                 [25, 29], [27, 27],
                                 [20, 25], [20, 27],
                                 [22, 29], [20, 27],
                                 [22, 21], [22, 22],
                                 [21, 23], [22, 22],
                                 [25, 22], [26, 23],
                                 [25, 22], [25, 21],
                                 [24, 22], [23, 22],
                                 [25, 18], [22, 18]],


                           9:   [[26, 27], [24, 29],
                                 [23, 29], [24, 29],
                                 [23, 25], [24, 25],
                                 [25, 18], [27, 20],
                                 [27, 23], [26, 24],
                                 [27, 25], [27, 20],
                                 [22, 18], [20, 20],
                                 [20, 23], [21, 24],
                                 [20, 23], [20, 20]]
                        }
                        
def calcule_image(images_input, number_check, listes):
    img = cv2.imread('images/Downloads/{}'.format(images_input))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, thresh = cv2.threshold(gray,127,255,1)

    _, contours, h = cv2.findContours(thresh,1,2)
    contours = np.vstack(contours).squeeze()
    b = contours.tolist()
    #print(b)
    a = listes[number_check]
    try:
        accuracy = len([a[i] for i in range(0, len(a)) if a[i] == b[i]]) / len(a)
        if accuracy >= 0.79:
            return True
    except:
        return False
    return False
    #accuracy = correct.sum() / correct.size

def calcule_image_new(images_input, number_check, listes=number_detect):
    img = cv2.imread('images/{}.png'.format(images_input))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    scale_percent = 1000 # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)

    resized = cv2.resize(gray, dim, interpolation = cv2.INTER_AREA)
    cv2.imwrite("test.png", resized)

    gray = cv2.bilateralFilter(resized, 11, 17, 17)
    edged = cv2.Canny(gray, 30, 200)

    contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(resized, contours, -1, (0, 255, 0), 3)

    contours = np.vstack(contours).squeeze()

    b = contours.tolist()
    a = number_detect[str(number_check)]

    try:
        accuracy = len([a[i] for i in range(0, len(a)) if a[i] == b[i]]) / len(a)
        if accuracy >= 0.79:
            return True
    except:
        return False
    return False

#listes = [(x, y) for x in range(0, 10) for y in range(0, 10)]
#for i, a in listes:
#    calcl = calcule_image("cel_{}.png".format(i), a)
#    if calcl:
#        print(calcl, i, a)

#normalize_image("cel_0.png")
#print(calcule_image("cel_{}.png".format(9), 7))
