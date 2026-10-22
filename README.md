# Digital Image Filtering

Praktikum pengolahan citra digital menggunakan Python, OpenCV, NumPy, dan Matplotlib. Program berjalan melalui terminal tanpa framework web.

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
python -m filters.median --image images/tayama.jpg --output-dir outputs --no-show
```

Input default adalah `images/tayama.jpg`. Seluruh gambar input disimpan di folder `images/`; `images/chizuru.jpg` tersedia sebagai alternatif melalui `--image`. Input dibaca sebagai grayscale uint8 dan tidak ditimpa. Path default relatif terhadap source code, sehingga runner dapat dipanggil menggunakan path absolut dari direktori lain. File hilang/rusak menghasilkan pesan error dan exit code 1.

## Metode dan output

Seluruh metode menerima Salt and Pepper Noise identik: generator lokal `default_rng(42)`, mask `< 0.02` menjadi hitam, mask `> 0.98` menjadi putih. Probabilitas total noise 4%; jumlah piksel yang berubah tidak harus tepat 4%.

| Metode | Parameter | Citra hasil (grayscale, ukuran sama dengan input) |
| --- | --- | --- |
| LPF | Tiga kernel 3x3: berbobot, pusat 1/5, rata-rata | `hasil_lpf1.png`, `hasil_lpf2.png`, `hasil_lpf3.png` |
| HPF | 8-neighbor pusat 8, 4-neighbor pusat 5, diagonal | `hasil_hpf1.png`, `hasil_hpf2.png`, `hasil_hpf3.png` |
| Median | Kernel 3x3 | `hasil_mf.png` |
| Gaussian | Kernel 3x3, sigmaX=1.0 | `hasil_gf.png` |

Semua hasil berada di `outputs/`. LPF/HPF menggunakan `CV_32F` dan `BORDER_CONSTANT` (padding nol). LPF dibulatkan dengan `np.rint`, sedangkan HPF dengan `np.floor(response + 0.5)`; keduanya dibatasi ke 0-255 dan dikonversi ke uint8. Respons negatif HPF dipotong ke nol.

## Gambar perbandingan

Selain delapan citra hasil filter, program menyimpan empat gambar perbandingan di `outputs/`. Setiap gambar menggabungkan citra asli, citra noisy, dan hasil filtering dalam satu file PNG.

| Metode | File perbandingan | Isi panel |
| --- | --- | --- |
| LPF | [perbandingan_lpf.png](outputs/perbandingan_lpf.png) | Asli, noisy, LPF 1, LPF 2, LPF 3 |
| HPF | [perbandingan_hpf.png](outputs/perbandingan_hpf.png) | Asli, noisy, HPF 1, HPF 2, HPF 3 |
| Median | [perbandingan_median.png](outputs/perbandingan_median.png) | Asli, noisy, Median 3x3 |
| Gaussian | [perbandingan_gaussian.png](outputs/perbandingan_gaussian.png) | Asli, noisy, Gaussian 3x3 |

LPF dan HPF menggunakan figure 12x4 inci (lima panel), sedangkan Median dan Gaussian menggunakan figure 12x8 inci (tiga panel). Semua visualisasi disimpan pada 150 dpi. Perintah `python run_all.py --no-show` tetap menghasilkan seluruh 12 PNG tanpa membuka jendela. Tanpa `--no-show`, runner menyimpan seluruh output sebelum menampilkan empat visualisasi.

### Low Pass Filter

![Perbandingan citra asli, noisy, dan tiga hasil LPF](outputs/perbandingan_lpf.png)

### High Pass Filter

![Perbandingan citra asli, noisy, dan tiga hasil HPF](outputs/perbandingan_hpf.png)

### Median Filter

![Perbandingan citra asli, noisy, dan hasil Median Filter](outputs/perbandingan_median.png)

### Gaussian Filter

![Perbandingan citra asli, noisy, dan hasil Gaussian Filter](outputs/perbandingan_gaussian.png)

## Verifikasi

```powershell
python -m unittest discover -s tests -v
```
