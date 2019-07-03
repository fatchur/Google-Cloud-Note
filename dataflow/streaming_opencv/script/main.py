import logging
import re
import argparse
import cv2
import ast
import numpy as np

from google.cloud import storage

import apache_beam as beam
from apache_beam.io import ReadFromText
from apache_beam.io import WriteToText
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions


class GrayscalingDoFn(beam.DoFn):
    def process(self, element):
        """[summary]
        
        Arguments:
            beam {[type]} -- [description]
            element {[type]} -- beam Pcollection
        
        Returns:
            [type] -- collection of elements
        """
        filename = element['filename']
        #idx = list(element.keys())[1]
        idx = element['idx']
        img = element['img']
        a = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        b = {}
        b['img'] = a
        b['idx'] = idx
        b['filename'] = filename
        return [b]


class SaveImage(beam.DoFn):
    def process(self, element):
        """[summary]
        
        Arguments:
            beam {[type]} -- [description]
            element {[type]} -- beam PCollection
        """
        print (list(element.keys()))
        print ("...................")
        
        filename = element['filename']
        #idx = list(element.keys())[1]
        idx = element['idx']
        img = element['img']
        img = cv2.imencode('.jpg', img)[1]
        img = img.tobytes()
        
        client = storage.Client()
        bucket = client.bucket("pubsub_notif_result")
        bucket.blob(filename + "_" + str(idx) + '.jpg').upload_from_string(img)
        

class GiveIdentity(beam.DoFn):
    def process(self, element):
        """[summary]
        
        Arguments:
            beam {[type]} -- [description]
            element {[type]} -- beam PCollection
        
        Returns:
            [type] -- collection of elements
        """
        frames = []
        filename = element[1]
        for idx, i in enumerate(element[0]):
            tmp = {}
            tmp['img'] = i
            tmp['idx'] = idx
            tmp['filename']=filename
            frames.append(tmp)

        return frames


def process_pubsub_data(element):
    """[summary]
    
    Arguments:
        element {[type]} -- beam PCollection
    
    Returns:
        [type] -- single element
    """
    import ast
    import cv2
    print ("========================>>>", element)
    logging.info("=========================>>")
    logging.info(element)
    element = ast.literal_eval(element.decode('utf-8'))
    filename = element['name']
    print (filename)
    logging.info(filename)
    
    gcs_url = 'http://storage.googleapis.com/pubsub_notif/' + filename
    cap = cv2.VideoCapture(gcs_url)
    
    frames = []
    while(True):
        ret, frame = cap.read()
        if ret == True:
            frames.append(frame)
        else:
            break

    print ("=====>>>>", len(frames))
    logging.info("--------------------:")
    logging.info(len(frames))
    return [frames, filename[:-4]]
    


def run(argv=None):
    parser = argparse.ArgumentParser()
    known_args, pipeline_args = parser.parse_known_args(argv)

    pipeline_options = PipelineOptions(pipeline_args)
    pipeline_options.view_as(SetupOptions).save_main_session = True
    p = beam.Pipeline(options=pipeline_options)
    
    # Read the text file[pattern] into a PCollection.
    data = p | beam.io.ReadFromPubSub(topic='projects/<project id>/topics/<pubsub topic>')
    
    final = (data | "processing pubsub data" >> beam.Map(process_pubsub_data)
                  | "give identity" >> beam.ParDo(GiveIdentity())
                  | 'grayscaling' >> beam.ParDo(GrayscalingDoFn())
                  | 'save_image' >> beam.ParDo(SaveImage())
           )
    
    result = p.run()
    result.wait_until_finish()


if __name__ == '__main__':
  logging.getLogger().setLevel(logging.INFO)
  run()
  
