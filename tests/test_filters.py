"""Verifikasi kontrak PRD V2 dan eksekusi terminal."""

import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import cv2
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from filters import gaussian, high_pass, low_pass, median
from filters.common import DEFAULT_IMAGE, ROOT, add_noise, save_comparison


class FilteringTests(unittest.TestCase):
    def test_noise_matches_practicum_and_preserves_input(self):
        image = np.full((200, 200), 128, np.uint8)
        mask = np.random.default_rng(42).random(image.shape)
        expected = image.copy()
        expected[mask < 0.02] = 0
        expected[mask > 0.98] = 255
        for module in (low_pass, high_pass, median, gaussian):
            np.testing.assert_array_equal(module.add_noise(image), expected)
        np.testing.assert_array_equal(image, 128)

    def test_kernel_coefficients_and_conversion(self):
        expected_lpf = [np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]]) / 16,
                        np.array([[1, 1, 1], [1, 2, 1], [1, 1, 1]]) / 10,
                        np.ones((3, 3)) / 9]
        expected_hpf = [np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]]),
                        np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]]),
                        np.array([[1, -2, 1], [-2, 5, -2], [1, -2, 1]])]
        image = np.random.default_rng(7).integers(0, 256, (17, 19), dtype=np.uint8)
        for module, kernels in ((low_pass, expected_lpf), (high_pass, expected_hpf)):
            actual = module.apply_filters(image)
            for kernel, declared, result in zip(kernels, module.KERNELS, actual):
                np.testing.assert_allclose(declared, kernel)
                # Scalar reference includes zero padding and checks boundary pixels.
                padded = np.pad(image.astype(np.float32), 1)
                response = np.empty_like(image, dtype=np.float32)
                for y, x in np.ndindex(image.shape):
                    response[y, x] = np.sum(padded[y:y+3, x:x+3] * kernel.astype(np.float32))
                opencv_response = cv2.filter2D(image, cv2.CV_32F, declared,
                                               borderType=cv2.BORDER_CONSTANT)
                np.testing.assert_allclose(opencv_response, response, atol=5e-5, rtol=0)
                # Use the actual CV_32F response for rounding: float summation
                # order can move an exact half to either side by a few ulps.
                rounded = (np.rint(opencv_response) if module is low_pass
                           else np.floor(opencv_response + 0.5))
                expected = np.clip(rounded, 0, 255).astype(np.uint8)
                np.testing.assert_array_equal(result, expected)

    def test_median_and_gaussian_parameters(self):
        image = np.full((31, 31), 100, np.uint8)
        image[15, 15] = 255
        np.testing.assert_array_equal(median.apply_filters(image)[0], cv2.medianBlur(image, 3))
        np.testing.assert_array_equal(gaussian.apply_filters(image)[0],
                                      cv2.GaussianBlur(image, (3, 3), sigmaX=1.0))
        self.assertEqual(len(median.apply_filters(image)), 1)
        self.assertEqual(len(gaussian.apply_filters(image)), 1)

    def test_panel_count_and_figure_size(self):
        with tempfile.TemporaryDirectory() as directory:
            for count, size in ((3, (12, 8)), (5, (12, 4))):
                def inspect(*args, **kwargs):
                    self.assertEqual(len(plt.gcf().axes), count)
                    np.testing.assert_array_equal(plt.gcf().get_size_inches(), size)
                with patch("filters.common.plt.savefig", side_effect=inspect):
                    save_comparison([np.zeros((9, 9))] * count, ["test"] * count,
                                    "comparison.png", directory, False)

    def test_cli_and_raw_outputs(self):
        env = dict(os.environ, MPLBACKEND="Agg")
        image = cv2.imread(str(DEFAULT_IMAGE), cv2.IMREAD_GRAYSCALE)
        noisy = add_noise(image)
        with tempfile.TemporaryDirectory() as directory:
            for name in ("low_pass", "high_pass", "median", "gaussian"):
                result = subprocess.run([sys.executable, "-m", f"filters.{name}",
                                         "--no-show", "--output-dir", directory],
                                        cwd=ROOT, env=env, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
            result = subprocess.run([sys.executable, str(ROOT / "run_all.py"),
                                     "--no-show", "--output-dir", directory], cwd=directory,
                                    env=env, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            expected = {}
            for prefix, module in (("lpf", low_pass), ("hpf", high_pass)):
                expected.update({f"hasil_{prefix}{n}.png": array
                                 for n, array in enumerate(module.apply_filters(noisy), 1)})
            expected["hasil_mf.png"] = median.apply_filters(noisy)[0]
            expected["hasil_gf.png"] = gaussian.apply_filters(noisy)[0]
            for filename, array in expected.items():
                np.testing.assert_array_equal(cv2.imread(str(Path(directory) / filename), 0), array)
            self.assertEqual(len(list(Path(directory).glob("*.png"))), 12)
            for module in (low_pass, high_pass, median, gaussian):
                saved = cv2.imread(str(Path(directory) / module.COMPARISON))
                self.assertEqual(saved.shape[:2], (1200, 1800) if module in (median, gaussian)
                                 else (600, 1800))
            bad = Path(directory) / "bad.jpg"
            bad.write_text("invalid")
            for path in (bad, Path(directory) / "missing.jpg"):
                result = subprocess.run([sys.executable, str(ROOT / "run_all.py"), "--no-show",
                                         "--image", str(path)], env=env, capture_output=True, text=True)
                self.assertEqual(result.returncode, 1)
                self.assertIn("Error:", result.stderr)
                self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
