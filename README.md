# Digital Image Filtering

Implementasi praktikum sesuai [PRD V2](PRD-V2.MD), menggunakan Python, OpenCV, NumPy, dan Matplotlib. Program berjalan melalui terminal tanpa framework web.

## Instalasi

Gunakan Python 3.10 atau lebih baru:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Menjalankan

```powershell
python run_all.py
python run_all.py --no-show
python -m filters.low_pass
python -m filters.high_pass
python -m filters.median
python -m filters.gaussian
```

Semua perintah menerima `--image`, `--output-dir`, dan `--no-show`. Contoh:

```powershell
python -m filters.median --image foto/tayama.jpg --output-dir outputs --no-show
```

Input default adalah `images/living.jpg`, salinan gambar `foto/tayama.jpg` yang digunakan proyek sebelum revisi. Nama file mengikuti PRD; gambar ini bukan citra sintetis ruang tamu. Input dibaca sebagai grayscale uint8 dan tidak ditimpa. Path default relatif terhadap source code, sehingga runner dapat dipanggil menggunakan path absolut dari direktori lain. File hilang/rusak menghasilkan pesan error dan exit code 1.

## Metode dan output

Seluruh metode menerima Salt and Pepper Noise identik: generator lokal `default_rng(42)`, mask `< 0.02` menjadi hitam, mask `> 0.98` menjadi putih. Probabilitas total noise 4%; jumlah piksel yang berubah tidak harus tepat 4%.

| Metode | Parameter | Citra hasil (grayscale, ukuran sama dengan input) |
| --- | --- | --- |
| LPF | Tiga kernel 3?3: berbobot, pusat 1/5, rata-rata | `hasil_lpf1.png`, `hasil_lpf2.png`, `hasil_lpf3.png` |
| HPF | 8-neighbor pusat 8, 4-neighbor pusat 5, diagonal | `hasil_hpf1.png`, `hasil_hpf2.png`, `hasil_hpf3.png` |
| Median | Kernel 3?3 | `hasil_mf.png` |
| Gaussian | Kernel 3?3, sigmaX=1.0 | `hasil_gf.png` |

Semua hasil berada di `outputs/`. LPF/HPF menggunakan `CV_32F` dan `BORDER_CONSTANT` (padding nol). LPF dibulatkan dengan `np.rint`, sedangkan HPF dengan `np.floor(response + 0.5)`; keduanya dibatasi ke 0?255 dan dikonversi ke uint8. Respons negatif HPF dipotong ke nol sesuai PRD V2.

Empat PNG tambahan adalah visualisasi perbandingan: `perbandingan_lpf.png`, `perbandingan_hpf.png` (lima panel, 12?4 inci), `perbandingan_median.png`, dan `perbandingan_gaussian.png` (tiga panel, 12?8 inci). Visualisasi disimpan pada 150 dpi. Runner menyimpan seluruh output sebelum membuka empat visualisasi dengan satu `plt.show()`.

## Laporan

- [Tugas 1 - Image Filtering (LPF & HPF)](docs/LAPORAN_TUGAS_1.md)
- [Tugas 2 - Image Filtering (Median dan Gaussian)](docs/LAPORAN_TUGAS_2.md)

## Verifikasi

```powershell
python -m unittest discover -s tests -v
```
