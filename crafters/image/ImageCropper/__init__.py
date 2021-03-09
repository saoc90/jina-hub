__copyright__ = "Copyright (c) 2020 Jina AI Limited. All rights reserved."
__license__ = "Apache-2.0"

from typing import Dict

import numpy as np

from jina.executors.decorators import single
from jina.executors.crafters import BaseCrafter

from .helper import _crop_image, _move_channel_axis, _load_image


class ImageCropper(BaseCrafter):
    """
    Crop the image with the specific crop box.

    The coordinate is the same coordinate-system in
        the :py:mode:`PIL.Image`.

    :param top: the vertical coordinate of the top left
        corner of the crop box.
    :param left: the horizontal coordinate of the top
        left corner of the crop box.
    :param height: the height of the crop box.
    :param width: the width of the crop box.
    :param channel_axis: the axis referring to the channels
    :param args:  Additional positional arguments
    :param kwargs: Additional keyword arguments
    """

    def __init__(self, top: int = 0, left: int = 0, height: int = 224, width: int = 224, channel_axis: int = -1, *args, **kwargs):
        """Set Constructor."""
        super().__init__(*args, **kwargs)
        self.top = top
        self.left = left
        self.height = height
        self.width = width
        self.channel_axis = channel_axis

    @single
    def craft(self, blob: 'np.ndarray', *args, **kwargs) -> Dict:
        """
        Crop the input image array.

        :param blob: The ndarray of the image
        :return: A dict with the cropped image
        """
        raw_img = _load_image(blob, self.channel_axis)
        _img, top, left = _crop_image(raw_img, target_size=(self.height, self.width), top=self.top, left=self.left)
        img = _move_channel_axis(np.asarray(_img), -1, self.channel_axis)
        return dict(offset=0, blob=img.astype('float32'), location=(top, left))

