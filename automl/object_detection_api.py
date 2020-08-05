import base64
import binascii
import cv2 
from qoaladep.utils.image_utils import encode_image_to_b64


def localize_objects(path):
    """Localize objects in the local image.

    Args:
    path: The path to the local file.
    """
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    #with open(path, 'rb') as image_file:
    #    content = image_file.read()
    content = path
    print (content)
    image = vision.types.Image(content=content)

    objects = client.object_localization(
        image=image).localized_object_annotations

    print('Number of objects found: {}'.format(len(objects)))
    for object_ in objects:
        print('\n{} (confidence: {})'.format(object_.name, object_.score))
        print('Normalized bounding polygon vertices: ')
        for vertex in object_.bounding_poly.normalized_vertices:
            print(' - ({}, {})'.format(vertex.x, vertex.y))


img = cv2.imread('images/phone3.jpg')
img_jpg = cv2.imencode('.jpg', img)[1].tobytes()
localize_objects(img_jpg)
