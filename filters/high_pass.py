"""High Pass Filter: dua Laplacian dan satu sharpening."""

import cv2
import numpy as np

from .common import DEFAULT_IMAGE, DEFAULT_OUTPUT, cli, read_image, save_comparison

KERNELS = (
    np.array([[0, -1, 0], [-1, 4, -1], [0, -1, 0]], dtype=np.float32),
    np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]], dtype=np.float32),
    np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], dtype=np.float32),
)


def apply_filters(image):
    responses = [cv2.filter2D(image, cv2.CV_32F, kernel) for kernel in KERNELS]
    return [np.clip(np.abs(r), 0, 255).astype(np.uint8) for r in responses[:2]] + [
        np.clip(responses[2], 0, 255).astype(np.uint8)
    ]


def main(image_path=DEFAULT_IMAGE, output_dir=DEFAULT_OUTPUT, show=True):
    """Menampilkan magnitudo Laplacian dan intensitas sharpening."""
    image = read_image(image_path)
    return save_comparison(
        [image, image.copy(), *apply_filters(image)],
        ["Citra asli (grayscale)", "Input grayscale", "Laplacian 4-neighbor", "Laplacian 8-neighbor", "Sharpening"],
        "hpf_result.png", output_dir, show,
    )


if __name__ == "__main__":
    cli(main)
