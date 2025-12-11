"""
A module for handling distance computations between voxel points in medical
images loaded using SimpleITK.

This module provides functionality for transforming voxel indices to world
coordinates and for computing minimum distances between sets of
points extracted from two images. It is specifically useful in medical imaging
applications where accurate spatial measurements are required.
"""

from __future__ import annotations

from functools import cached_property, lru_cache
from typing import TYPE_CHECKING

import SimpleITK as sitk  # type: ignore[import]
import numpy as np  # type: ignore[import]
from scipy.spatial import cKDTree  # type: ignore[import]


if TYPE_CHECKING:
    import numpy.typing as npt  # type: ignore[import]
    from pathlib import Path


def convert_to_world_coordinates(img: sitk.Image) -> npt.NDArray[np.float64]:
    """
    Convert voxel indices from image space to world coordinates, considering the
    image's origin, spacing, and direction.

    This function utilizes the image's metadata to transform voxel indices (where
    mask values are greater than zero) into physical world coordinates. It takes
    into account the image's origin, spacing, and direction matrix to perform the
    necessary transformation from the index space to the physical space.

    :param img: A SimpleITK image object containing the metadata and voxel data
                required for the transformation.
    :type img: sitk.Image
    :return: A numpy array of world coordinates corresponding to the non-zero
             voxel indices of the input image.
    :rtype: npt.NDArray[np.float64]
    """
    origin = np.array(img.GetOrigin())
    spacing = np.array(img.GetSpacing())
    direction = np.array(img.GetDirection()).reshape(3, 3)
    mask = sitk.GetArrayFromImage(img)
    voxel_indices = np.argwhere(mask > 0)[:, ::-1]
    # Apply transformation: physical = origin + direction @ (spacing * index)
    scaled_indices = voxel_indices * spacing
    world_points = origin + (direction @ scaled_indices.T).T
    return world_points


class Distances:
    """
    Handles computation of distances between corresponding points in two images.

    This class is designed to compute distances between two sets of points
    extracted from images. The main purpose is to evaluate minimum
    distances between the points in two given images. The images are read from the
    provided file paths and processed to compute distances efficiently.

    :ivar img_1: The image loaded from path_1, represented as a SimpleITK Image object.
    :type img_1: sitk.Image
    :ivar img_2: The image loaded from path_2, represented as a SimpleITK Image object.
    :type img_2: sitk.Image
    """

    def __init__(self, path_1: str | Path, path_2: str | Path):
        self.img_1 = sitk.ReadImage(path_1)
        self.img_2 = sitk.ReadImage(path_2)

    @lru_cache(maxsize=1)
    def _compute_distances(self) -> npt.NDArray[np.float64]:
        points_1 = convert_to_world_coordinates(self.img_1)
        points_2 = convert_to_world_coordinates(self.img_2)
        tree = cKDTree(points_2)
        distances, _ = tree.query(points_1, workers=-1)
        return distances

    @cached_property
    def minimum(self) -> float:
        """
        The minimum distance between the two images.

        :return: The minimum distance value as a float.
        :rtype: float
        """
        return self._compute_distances().min()


if __name__ == "__main__":
    distances = Distances("laa.segmentation.nii.gz", "pa.segmentation.nii.gz")
    print(f"Minimum distance between segmentations: {distances.minimum}")
