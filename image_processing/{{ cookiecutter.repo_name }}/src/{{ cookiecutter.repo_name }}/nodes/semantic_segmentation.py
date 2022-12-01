import numpy as np
import cv2
from keras_segmentation.pretrained import pspnet_50_ADE_20K
from keras_segmentation.predict import predict

#import pipelinex

def predict_segmentation(model, img):
    resized_img = cv2.resize(img, (473, 473))
    resized_out = predict(model, inp=resized_img)
    out = cv2.resize(resized_out, (512, 512), interpolation=cv2.INTER_NEAREST)
    return out.astype(np.uint8)


def get_semantic_segments(img):
    #img = pipelinex.dict_io(img)
    #print(type(img))
    #print(img)
    
    model = pspnet_50_ADE_20K()

    out = {}
    for image_name in img:
        out[image_name] = predict_segmentation(model, img[image_name])
    
    return out
