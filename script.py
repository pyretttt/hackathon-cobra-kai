"""OCR script."""

import os
import sys
from functools import reduce

import cv2
from paddleocr import PaddleOCR

ocr = PaddleOCR(use_angle_cls=True, lang='en')

# utils


def read_args():
    try:
        output_path = sys.argv[2]
    except IndexError:
        output_path = os.getcwd()
    return sys.argv[1], output_path


def traverse_path_for_image(path):
    if os.path.isdir(path):
        for file_name in os.listdir(path):
            img_path = os.path.join(path, file_name)
            if os.path.isfile(img_path):
                yield cv2.imread(img_path), img_path
    elif os.path.isfile(path):
        yield cv2.imread(path), path


def preprocess_image(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def get_base_name(path):
    bath_name = os.path.basename(path)
    return bath_name.split('.')


def invoke(path, output_path):
    for img, img_path in traverse_path_for_image(path):
        image_name = get_base_name(img_path)[0]
        preproccessed_img = preprocess_image(img)

        # boxes
        ocr_res = ocr.ocr(preproccessed_img)[0]
        formatted_ocr_result = reduce_ocr_result_to_txt_task(ocr_res)
        write_boxes_result(formatted_ocr_result, os.path.join(
            output_path, image_name + '-1' + '.txt'))

        # entities
        model_input = get_segment_from_ocr_result(ocr_res)
        # TODO - add entities

# boxes


def write_boxes_result(ocr_results_formatted, output_path):
    with open(output_path, mode='w') as f:
        for segment in ocr_results_formatted:
            f.write(segment + '\n')


def reduce_ocr_result_to_txt_task(ocr_result):
    result = []
    for segment_result in ocr_result:
        line = segment_coords_reducer(
            segment_result) + segment_recognition_reducer(segment_result)
        result.append(line)

    return result


def segment_coords_reducer(result):
    return reduce(lambda result, element: result + f'{element[0]},{element[1]},', result[0], '')


def segment_recognition_reducer(result):
    return result[1][0]

# entities


def get_segment_from_ocr_result(ocr_results):
    all_segments = [segment_result[1][0] for segment_result in ocr_results]
    return ' '.join(all_segments)

# main


if __name__ == '__main__':
    try:
        input_path, output_path = read_args()
    except IndexError:
        print('Wrong arguments passed')
        print('Example:')
        print('script_name input_directory [output_directory]')
    else:
        invoke(input_path, output_path)
        print(f'Finished output files in directory `{output_path}`')
