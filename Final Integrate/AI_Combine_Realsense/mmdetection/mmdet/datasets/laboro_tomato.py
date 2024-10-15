from .coco import CocoDataset
from .builder import DATASETS


@DATASETS.register_module()
class LaboroTomato(CocoDataset):
    CLASSES = ('l_fully_ripened', 'l_half_ripened', 'l_green')