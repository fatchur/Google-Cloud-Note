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
        idx = list(element.keys())[0]
        img = element[idx]
        a = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        b = {}
        b[idx] = a
        return [b]


class SaveImage(beam.DoFn):
    def process(self, element):
        print (list(element.keys()))
        print ("...................")
        
        idx = list(element.keys())[0]
        img = element[idx]
        img = cv2.imencode('.jpg', img)[1]
        img = img.tobytes()
        
        client = storage.Client()
        bucket = client.bucket("pubsub_notif_result")
        bucket.blob(str(idx) + '.jpg').upload_from_string(img)
        

class GiveIdentity(beam.DoFn):
    def process(self, element):
        frames = []
        for idx, i in enumerate(element):
            tmp = {}
            tmp[idx] = i
            frames.append(tmp)

        return frames


def process_pubsub_data(element):
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
    return frames
    


def run(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--input',
                      dest='input',
                      required=True,
                      help='Input file to process.')
    parser.add_argument('--output',
                      dest='output',
                      required=True,
                      help='Output file to write results to.')
    known_args, pipeline_args = parser.parse_known_args(argv)

    pipeline_options = PipelineOptions(pipeline_args)
    pipeline_options.view_as(SetupOptions).save_main_session = True
    p = beam.Pipeline(options=pipeline_options)
    
    # Read the text file[pattern] into a PCollection.
    data = p | beam.io.ReadFromPubSub(topic='projects/braided-grammar-239803/topics/pubsub_notif')
    
    final = (data | "processing pubsub data" >> beam.Map(process_pubsub_data)
                  | "give identity" >> beam.ParDo(GiveIdentity())
                  | 'grayscaling' >> beam.ParDo(GrayscalingDoFn())
                  | 'save_image' >> beam.ParDo(SaveImage())
           )
    
    #final = (data | "processing pubsub data" >> beam.Map(process_pubsub_data))

    result = p.run()
    result.wait_until_finish()
    print ("=====")


if __name__ == '__main__':
  logging.getLogger().setLevel(logging.INFO)
  run()
  
