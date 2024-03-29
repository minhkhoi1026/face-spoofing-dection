from albumentations import (Compose, Normalize, RandomBrightnessContrast,
                            RandomCrop, Resize, RGBShift, ShiftScaleRotate,
                            SmallestMaxSize, MotionBlur, GaussianBlur,
                            MedianBlur, Blur, RandomRotate90, HorizontalFlip,
                            VerticalFlip, HueSaturationValue, RandomSizedCrop,
                            IAASharpen, ToGray)
import cv2
# https://github.com/albumentations-team/albumentations/issues/1246
cv2.setNumThreads(0)
from albumentations.pytorch.transforms import ToTensorV2

from . import TRANSFORM_REGISTRY

TRANSFORM_REGISTRY.register(RandomCrop, prefix='Alb')
TRANSFORM_REGISTRY.register(RGBShift, prefix='Alb')
TRANSFORM_REGISTRY.register(Normalize, prefix='Alb')
TRANSFORM_REGISTRY.register(Resize, prefix='Alb')
TRANSFORM_REGISTRY.register(Compose, prefix='Alb')
TRANSFORM_REGISTRY.register(RandomBrightnessContrast, prefix='Alb')
TRANSFORM_REGISTRY.register(ShiftScaleRotate, prefix='Alb')
TRANSFORM_REGISTRY.register(SmallestMaxSize, prefix='Alb')
TRANSFORM_REGISTRY.register(MotionBlur, prefix='Alb')
TRANSFORM_REGISTRY.register(GaussianBlur, prefix='Alb')
TRANSFORM_REGISTRY.register(MedianBlur, prefix='Alb')
TRANSFORM_REGISTRY.register(Blur, prefix='Alb')
TRANSFORM_REGISTRY.register(RandomRotate90, prefix='Alb')
TRANSFORM_REGISTRY.register(HorizontalFlip, prefix='Alb')
TRANSFORM_REGISTRY.register(VerticalFlip, prefix='Alb')
TRANSFORM_REGISTRY.register(HueSaturationValue, prefix='Alb')
TRANSFORM_REGISTRY.register(RandomSizedCrop, prefix='Alb')
TRANSFORM_REGISTRY.register(IAASharpen, prefix='Alb')
TRANSFORM_REGISTRY.register(ToTensorV2, prefix='Alb')


@TRANSFORM_REGISTRY.register()
def train_classify_tf(img_size: int):
    return Compose([
        Resize(img_size, img_size),
        HorizontalFlip(p=0.5),
        VerticalFlip(p=0.5),
        RandomRotate90(p=0.5),
        RandomBrightnessContrast(brightness_limit=0.25),
        ToGray(p=0.1),
        ShiftScaleRotate(rotate_limit=[-15,15], shift_limit=[0.15,0.15], scale_limit=[0.75, 1.25]),
    ])


@TRANSFORM_REGISTRY.register()
def test_classify_tf(img_size: int):
    return Resize(img_size, img_size)

@TRANSFORM_REGISTRY.register()
def img_normalize():
    return Compose([
        Normalize([0.49139968, 0.48215841, 0.44653091], [0.24703223, 0.24348513, 0.26158784]),
        ToTensorV2()])
