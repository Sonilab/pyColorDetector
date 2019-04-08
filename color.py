#time
#real	0m5.561s
#user	0m2.616s
#sys	0m0.793s


import PIL
from PIL import Image
import cv2
import sklearn
from sklearn.cluster import KMeans
import colorsys


#DEFINES

#CLUSTER_NUM
CLUSTER_NUM = 4

#set analyzing size
RESIZE_WIDTH = 32

#For Param Tuning
PARAM_TUNING = False


def run(cv2_img):

    #get original image size
    img_height,img_width,_ = cv2_img.shape

    # CALC HEIGHT PARAM
    RESIZE_HEIGHT = RESIZE_WIDTH / img_width * img_height

    #Resizing for increasing speed
    cv2_img = cv2.resize(cv2_img, (int(RESIZE_WIDTH), int(RESIZE_HEIGHT)))
    #rest because of using numpy array
    #cv2_img = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)


    #analyze main 4 color by sklearn
    cv2_img = cv2_img.reshape(
        (cv2_img.shape[0] * cv2_img.shape[1], 3))


    #Clustring Section
    cluster = KMeans(n_clusters = CLUSTER_NUM)
    cluster.fit(X=cv2_img)


    # cluster.cluster_centers_ returns RGB array of each cluster.
    #rgb(0-255, 0-255, 0-255)
    main_rgb_color = cluster.cluster_centers_


    #hsv(0.0-1.0, 0.0-1.0, 0.0-1.0)
    hsv_color = [[], [], [], []]


    #Convert from RGB to HSV
    for i in range(CLUSTER_NUM):
        hsv_color[i] = colorsys.rgb_to_hsv(main_rgb_color[i][0] / 255.0, main_rgb_color[i][1] / 255.0, main_rgb_color[i][2] / 255.0)
        if PARAM_TUNING:
            print (hsv_color[i])


    # Pick the most impact cluster
    # Rescaled to hsv(0.0-1.0, 0.0-1.0, 0.0-1.0)
    color_result = [0.0, 0.0, 0.0]
    impact = highest = 0.0
    for c in hsv_color:
        impact = c[1]+(c[2]*c[2])
        if impact > highest:
            color_result = c
            highest = impact
    # print('RST' , color_result)
    return color_result




#Method for manual open with this module only
def open_with_file(file_name):
    img = cv2.imread(file_name)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return run(img)
