Install library from https://github.com/fizyr/keras-retinanet in this folder

python ./keras-retinanet/keras_retinanet/bin/train.py --batch-size 1 --steps 1000 \
--epochs=10 --freeze-backkbone  csv ./train_annotations_tuas classes --val-annotations ./test_annotations_tuas

Images_with_bounding_box - folder containing images with bounding-box annotations

train_annotations_tuas - training annotations 

test_annotations_tuas - test annotations
