import tensorflow as tf
import cv2
import matplotlib.pyplot as plt

import numpy as np

import asyncio
import functools
import math

import sys
from PIL import Image, ImageColor, ImageDraw, ImageStat



def grayWorld(urlImg,utlSalida):
    def array_to_image(image_array):
        return Image.fromarray(np.uint8(image_array))

    def image_to_array(image):
        image_array = np.asarray(image)
        image_array.flags.writeable = True
        return image_array
    image=Image.open(urlImg)
    image_array = image_to_array(image)
    image_array = image_array.transpose(2, 0, 1).astype(np.uint32)
    average_g = np.average(image_array[1])
    image_array[0] = np.minimum(image_array[0] * (average_g / np.average(image_array[0])), 255)
    image_array[2] = np.minimum(image_array[2] * (average_g / np.average(image_array[2])), 255)
    img= array_to_image(image_array.transpose(1, 2, 0).astype(np.uint8))
    img.save(utlSalida, "JPEG")




def boundingBox(urlImg,utlSalida):
    image = cv2.imread(urlImg)
    original = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    suma = 0
    imagenSelec = None
    seSelecciono = False

    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        if suma < (w + h):
            suma = (w + h)
            imagenSelec = c
            seSelecciono = True

    if seSelecciono:
        x, y, w, h = cv2.boundingRect(imagenSelec)
        # print("utlSalida=",utlSalida)
        cv2.imwrite(utlSalida, original[y:y + h, x:x + w])

def mresize(urlImg,urlSalida,size = None):
    """
    size[#w,#h]
    :param urlImg:
    :param urlSalida:
    :param size:
    :return:
    """
    image = tf.keras.utils.load_img(
        urlImg
    )
    if size is None:
        #size = [35, 35]
        size = [32, 32]
    image = tf.image.resize(
        image, size, method=tf.image.ResizeMethod.BILINEAR, preserve_aspect_ratio=False,
        antialias=False, name=None
    )
    tf.keras.utils.save_img(
        urlSalida, image, data_format=None, file_format=None, scale=True
    )

def cielAB(urlImg,utlSalida):
    img_rgb = cv2.imread(urlImg)
    #img_CIELab = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2LAB)
    img_CIELab = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2LAB)
    #print("utlSalida=",utlSalida)
    #print("img_CIELab=", img_CIELab)
    cv2.imwrite(utlSalida, img_CIELab)