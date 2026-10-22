"""Jalankan seluruh filter, simpan semua PNG, lalu tampilkan hasil."""

import matplotlib.pyplot as plt

from filters import gaussian, high_pass, low_pass, median
from filters.common import DEFAULT_IMAGE, DEFAULT_OUTPUT, cli


def main(image_path=DEFAULT_IMAGE, output_dir=DEFAULT_OUTPUT, show=True):
    """Menjalankan LPF, HPF, Median, dan Gaussian secara berurutan."""
    paths = []
    for method in (low_pass, high_pass, median, gaussian):
        paths.append(method.main(image_path=image_path, output_dir=output_dir, show=False))
    if show:
        try:
            for path in paths:
                figure, axis = plt.subplots(figsize=(12, 4))
                figure.canvas.manager.set_window_title(path.stem)
                axis.imshow(plt.imread(path))
                axis.axis("off")
                figure.tight_layout(pad=0)
            plt.show()
        finally:
            plt.close("all")
    return paths


if __name__ == "__main__":
    cli(main)
