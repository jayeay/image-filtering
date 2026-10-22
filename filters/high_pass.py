"""High Pass Filter sesuai materi praktikum."""

import cv2
import numpy as np

from .common import DEFAULT_IMAGE, DEFAULT_OUTPUT, add_noise, cli, run_filter

COMPARISON = 'perbandingan_hpf.png'

KERNELS = (
    np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]], dtype=np.float32),
    np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], dtype=np.float32),
    np.array([[1, -2, 1], [-2, 5, -2], [1, -2, 1]], dtype=np.float32),
)


def apply_filters(noisy):
    responses = [cv2.filter2D(noisy, cv2.CV_32F, kernel,
                             borderType=cv2.BORDER_CONSTANT) for kernel in KERNELS]
    return [np.clip(np.floor(result + 0.5), 0, 255).astype(np.uint8) for result in responses]


def main(image_path=DEFAULT_IMAGE, output_dir=DEFAULT_OUTPUT, show=True):
    """High Pass Filter sesuai materi praktikum."""
    return run_filter(image_path, output_dir, show, apply_filters,
                      ['HPF 1: 8-neighbor', 'HPF 2: 4-neighbor', 'HPF 3: Diagonal'],
                      ['hasil_hpf1.png', 'hasil_hpf2.png', 'hasil_hpf3.png'], COMPARISON)


if __name__ == "__main__":
    cli(main)
