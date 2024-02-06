import os
import json

def labelme_to_yolo_directory(input_directory, output_directory, class_mapping=None):
    for filename in os.listdir(input_directory):
        if filename.endswith('.json'):
            labelme_json_path = os.path.join(input_directory, filename)
            output_yolo_path = os.path.join(output_directory, f"{os.path.splitext(filename)[0]}.txt")
            output_classes_path = os.path.join(output_directory, "yolo_classes.txt")

            labelme_to_yolo(labelme_json_path, output_yolo_path, output_classes_path, class_mapping)

def labelme_to_yolo(labelme_json_path, output_yolo_path, output_classes_path, class_mapping=None):
    with open(labelme_json_path, 'r') as file:
        labelme_data = json.load(file)

    yolo_lines = []
    yolo_classes = []

    for shape in labelme_data['shapes']:
        label = shape['label']

        if class_mapping and label in class_mapping:
            yolo_label = class_mapping[label]
        else:
            yolo_label = label

        if yolo_label not in yolo_classes:
            yolo_classes.append(yolo_label)

        points = shape['points']
        x_min = min(point[0] for point in points)
        y_min = min(point[1] for point in points)
        x_max = max(point[0] for point in points)
        y_max = max(point[1] for point in points)

        width = x_max - x_min
        height = y_max - y_min

        # Convert coordinates to YOLO format (normalized between 0 and 1)
        x_center = (x_min + x_max) / 2.0
        y_center = (y_min + y_max) / 2.0
        normalized_x_center = x_center / labelme_data['imageWidth']
        normalized_y_center = y_center / labelme_data['imageHeight']
        normalized_width = width / labelme_data['imageWidth']
        normalized_height = height / labelme_data['imageHeight']

        yolo_line = f"{yolo_classes.index(yolo_label)} {normalized_x_center} {normalized_y_center} {normalized_width} {normalized_height}"
        yolo_lines.append(yolo_line)

    with open(output_yolo_path, 'w') as yolo_file:
        yolo_file.write('\n'.join(yolo_lines))

    with open(output_classes_path, 'w') as classes_file:
        classes_file.write('\n'.join(yolo_classes))

if __name__ == "__main__":
    input_directory = "C:\\Users\\DELL\\Downloads\\image 2\\image"
    output_directory = "C:\\Users\\DELL\\Downloads\\image 2"
    class_mapping = {
        # Add your class mapping if necessary
        # 'labelme_class': 'yolo_class',
    }

    labelme_to_yolo_directory(input_directory, output_directory, class_mapping)
