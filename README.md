# Digital Image Filtering

Praktikum Python untuk Low Pass, High Pass, Median, dan Gaussian Filter menggunakan OpenCV, NumPy, serta Matplotlib. Setiap hasil memuat lima panel grayscale dalam figure 12 × 4 inci.

## Instalasi dan penggunaan

Gunakan Python 3.10 atau lebih baru. Dari folder proyek:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python run_all.py
```

Semua PNG disimpan terlebih dahulu, kemudian empat jendela visualisasi ditampilkan dengan satu pemanggilan `plt.show()`. Tutup jendela untuk menyelesaikan program. Untuk terminal tanpa tampilan grafis:

```powershell
python run_all.py --no-show
```

Jalankan setiap metode secara mandiri:

```powershell
python -m filters.low_pass
python -m filters.high_pass
python -m filters.median
python -m filters.gaussian
```

Semua perintah mendukung `--no-show`, `--image "C:\path\foto.jpg"`, dan `--output-dir "C:\path\hasil"`. Lokasi default ditentukan relatif terhadap source code, sehingga tidak bergantung pada direktori terminal. Dari direktori lain, jalankan `run_all.py` dengan path absolut.

## Input dan hasil

`foto/living.jpg` adalah **citra contoh sintetis ruang tayama**, dibuat dengan bentuk geometris OpenCV, bukan foto asli pengguna. Ganti file tersebut dengan foto Anda atau gunakan `--image`. Input dikonversi ke grayscale; panel citra asli juga grayscale sesuai acceptance criteria. File asli tidak diubah.

| Metode | Variasi | Output |
| --- | --- | --- |
| LPF | Kernel rata-rata 3×3, 5×5, 7×7 | `outputs/lpf_result.png` |
| HPF | Laplacian 4-neighbor, 8-neighbor, sharpening | `outputs/hpf_result.png` |
| Median | Salt and Pepper Noise, median 3×3, 5×5, 7×7 | `outputs/median_result.png` |
| Gaussian | Gaussian Noise, blur 3×3, 5×5, 7×7 | `outputs/gaussian_result.png` |

Laplacian dihitung dalam float untuk mempertahankan respons negatif, lalu ditampilkan sebagai magnitudo yang dibatasi 0–255. Sharpening menggunakan intensitas yang dibatasi 0–255. Salt and Pepper Noise memiliki probabilitas total 5% (masing-masing 2,5% hitam/putih). Gaussian Noise menggunakan mean 0 dan simpangan baku 20. Keduanya memakai generator lokal dengan seed 42 agar hasil dapat diulang tanpa mengubah random state global.

File yang hilang atau tidak dapat dibaca menghasilkan pesan `Error:` dan exit code 1 tanpa traceback. PNG keluaran dengan nama yang sama diperbarui saat program dijalankan kembali.
