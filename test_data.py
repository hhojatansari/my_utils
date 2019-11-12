from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import pandas as pd
from collections import namedtuple, OrderedDict
import cv2

OCR = False
detection = True
train_percent = 0.90
total_data_path = '/media/gata/data/'
csv_input_list = ['/media/gata/data/img.txt']
images_path_list = ['/media/gata/data/img/']


def split(df, group):
    data = namedtuple('data', ['filename', 'object'])
    gb = df.groupby(group)
    return [data(filename, gb.get_group(x)) for filename, x in zip(gb.groups.keys(), gb.groups)]


def create_tf_detection_example(group, path):
    for index, row in group.object.iterrows():
        print(row['filename'])
        img = cv2.imread("/media/gata/data/img/"+row['filename'])
        cv2.line(img, (row['lt'], row['tl']), (row['rt'], row['tr']), (0, 0, 255), 5)
        cv2.line(img, (row['rt'], row['tr']), (row['rb'], row['br']), (0, 0, 255), 5)
        cv2.line(img, (row['rb'], row['br']), (row['lb'], row['bl']), (0, 0, 255), 5)
        cv2.line(img, (row['lb'], row['bl']), (row['lt'], row['tl']), (0, 0, 255), 5)
        img = cv2.putText(img, str(row['class']), (row['lt']+30, row['tl']+20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3, cv2.LINE_AA)
        cv2.imshow("win", img)
        cv2.waitKey(1000)


def _run():
    c = 0
    try:
        for i in range(len(csv_input_list)):
            images_path = images_path_list[i]
            examples = pd.read_csv(csv_input_list[i])
            grouped = split(examples, 'filename')
            if detection:
                for group in grouped:
                    c += 1
                    print(c)
                    if c % 2 is 0:
                        create_tf_detection_example(group, images_path)
                        cv2.waitKey(500)

    except KeyboardInterrupt:
        print("Except ")


_run()
print("Finished.")
