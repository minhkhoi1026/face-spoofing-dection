from src.utils.registry import Registry

EXTRACTOR_REGISTRY = Registry("EXTRACTOR")

from src.extractor.efficient_net import EfficientNetExtractor
from src.extractor.vit_net import VitNetExtractor
