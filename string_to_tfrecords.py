"""
Usage:
  # From tensorflow/models/
  # Create train data:
  python generate_tfrecord.py --csv_input=data/train_labels.csv  --output_path=train.record

  # Create test data:
  python generate_tfrecord.py --csv_input=data/test_labels.csv  --output_path=test.record
"""
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
import sys
import os
import io
import pandas as pd
import shutil
import tensorflow as tf
import random
from PIL import Image
import PIL
from object_detection.utils import dataset_util
from collections import namedtuple, OrderedDict
import traceback

OCR = False
detection = True
train_percent = 0.90
total_data_path = '/media/gata/data/'
csv_input_list = ['/media/gata/data/img.txt']
images_path_list = ['/media/gata/data/img/']

output_path_train = total_data_path + 'train.record'
output_path_test = total_data_path + 'test.record'


# TO-DO replace this with label map
def class_text_to_int(row_label):
    if row_label == 'number':
        return 1
    elif row_label == 'cvv2':
        return 2
    elif row_label == 'date':
        return 3
    else:
        return None


def class_int_to_text(row_label):
    if row_label == 1:
        return b'number'
    elif row_label == 2:
        return b'cvv2date'
    elif row_label == 3:
        return b'cvv2date'
    else:
        return None


def class_int_to_int(row_label):
    if row_label == 1:
        return 1
    elif row_label == 2:
        return 2
    elif row_label == 3:
        return 2
    else:
        return None


def split(df, group):
    data = namedtuple('data', ['filename', 'object'])
    gb = df.groupby(group)
    return [data(filename, gb.get_group(x)) for filename, x in zip(gb.groups.keys(), gb.groups)]


def create_tf_detection_example(group, path):
    try:
        with tf.gfile.GFile(os.path.join(path, '{}'.format(group.filename)), 'rb') as fid:
            encoded_jpg = fid.read()
    except:
        traceback.print_exc()
        print('error in opening: ' + os.path.join(path, '{}'.format(group.filename)))
        return None
    filename = group.filename.encode('utf8')
    image_format = b'jpg'
    xmins = []
    xmaxs = []
    ymins = []
    ymaxs = []
    classes_text = []
    classes = []
    # im = Image.open(os.path.join(path, '{}'.format(group.filename)))
    for index, row in group.object.iterrows():
        # if row['class'] == 2:
        #     continue
        if max(int(row['lt']), int(row['lb'])) >= int(row['width']) or max(int(row['tl']), int(row['tr'])) >= int(
                row['height']) or min(int(row['rt']), int(row['rb'])) <= 0 or min(int(row['br']), int(row['bl'])) <= 0:
            continue
        xmin = min(float(row['lt']), float(row['lb']))
        xmax = max(float(row['rt']), float(row['rb']))
        ymin = min(float(row['tl']), float(row['tr']))
        ymax = max(float(row['bl']), float(row['br']))

        xmin += -6  # random.randint(-5, 2)
        xmax += 6  # random.randint(2, 5)
        ymin += -5  # random.randint(-5, 2)
        ymax += 5  # random.randint(2, 5)

        xmin = max(0, xmin)
        xmax = min(xmax, row['width'])
        ymin = max(0, ymin)
        ymax = min(ymax, row['height'])
        # d_im = im.crop((xmin, ymin, xmax, ymax))
        # d_im.show("")
        # return None
        xmins.append(xmin / row['width'])
        xmaxs.append(xmax / row['width'])
        ymins.append(ymin / row['height'])
        ymaxs.append(ymax / row['height'])
        classes_text.append(class_int_to_text(row['class']))
        classes.append(class_int_to_int(row['class']))

    if len(xmins) == 0:
        return None

    tf_example_detection = tf.train.Example(features=tf.train.Features(feature={
        'image/height': dataset_util.int64_feature(row['height']),
        'image/width': dataset_util.int64_feature(row['width']),
        'image/filename': dataset_util.bytes_feature(filename),
        'image/source_id': dataset_util.bytes_feature(filename),
        'image/encoded': dataset_util.bytes_feature(encoded_jpg),
        'image/format': dataset_util.bytes_feature(image_format),
        'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
        'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
        'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
        'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
        'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
        'image/object/class/label': dataset_util.int64_list_feature(classes),
    }))

    return tf_example_detection


def main(_):
    number_of_train_data = 4
    number_of_test_data = 2
    writer_train = tf.python_io.TFRecordWriter(output_path_train)
    if train_percent < 1.00:
        writer_test = tf.python_io.TFRecordWriter(output_path_test)
    try:
        for i in range(len(csv_input_list)):
            print(csv_input_list[i])
            images_path = images_path_list[i]
            examples = pd.read_csv(csv_input_list[i])
            grouped = split(examples, 'filename')
            if detection:
                for group in grouped:
                    print("\n- ", group)
                    tf_example = create_tf_detection_example(group, images_path)
                    if tf_example is not None:
                        if random.random() < train_percent:
                            number_of_train_data += 1
                            writer_train.write(tf_example.SerializeToString())
                            if number_of_train_data % 200 == 0:
                                print("number_of_train_data: " + str(number_of_train_data))
                        else:
                            number_of_test_data += 1
                            writer_test.write(tf_example.SerializeToString())
                            if number_of_train_data % 200 == 0:
                                print("number_of_test_data: " + str(number_of_test_data))

        writer_train.close()
        print("number_of_train_data: " + str(number_of_train_data))
        if train_percent < 1.00:
            writer_test.close()
        print("number_of_test_data: " + str(number_of_test_data))
    except KeyboardInterrupt:
        writer_train.close()
        print("number_of_train_data: " + str(number_of_train_data))
        if train_percent < 1.00:
            writer_test.close()
            print("number_of_test_data: " + str(number_of_test_data))


if __name__ == '__main__':
    tf.app.run()
    print("Finished.")
