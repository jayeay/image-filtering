# PRD – Digital Image Filtering

**Versi:** 2.0 (Revisi Sesuai Materi Praktikum)  
**Bahasa:** Python 3.x  
**Library:** OpenCV, NumPy, Matplotlib  
**Environment:** Visual Studio Code  
**Metode:** LPF, HPF, Median, Gaussian

## 1. Deskripsi Project

Digital Image Filtering merupakan project praktikum pengolahan citra digital yang mengimplementasikan empat metode filtering, yaitu Low Pass Filter (LPF), High Pass Filter (HPF), Median Filter, dan Gaussian Filter.

Setiap metode dibuat dalam file Python terpisah dengan mengikuti algoritma, matriks kernel, dan tahapan pemrosesan pada materi dosen.

Project dijalankan melalui terminal VS Code dan menampilkan hasil menggunakan Matplotlib.

## 2. Tujuan

1. Mengimplementasikan empat metode image filtering.
2. Memahami penggunaan kernel pada pengolahan citra.
3. Menampilkan perbandingan citra asli, noisy, dan hasil filtering.
4. Menganalisis perbedaan hasil masing-masing metode.
5. Menyimpan citra hasil filtering dalam format PNG.

## 3. Struktur Project

```text
digital-image-filtering/
├── images/
│   └── living.jpg
├── filters/
│   ├── __init__.py
│   ├── low_pass.py
│   ├── high_pass.py
│   ├── median.py
│   └── gaussian.py
├── outputs/
│   ├── hasil_lpf1.png
│   ├── hasil_lpf2.png
│   ├── hasil_lpf3.png
│   ├── hasil_hpf1.png
│   ├── hasil_hpf2.png
│   ├── hasil_hpf3.png
│   ├── hasil_mf.png
│   └── hasil_gf.png
├── run_all.py
├── requirements.txt
└── README.md
```

## 4. Functional Requirements

### FR-01 – Low Pass Filter

**File:** `filters/low_pass.py`

Mengimplementasikan tiga kernel LPF berukuran 3×3 sesuai materi praktikum.

**LPF 1 – Kernel Berbobot**

```python
lpf1 = np.array([
    [1/16, 1/8, 1/16],
    [1/8,  1/4, 1/8],
    [1/16, 1/8, 1/16]
], dtype=np.float32)
```

**LPF 2 – Kernel Pusat 1/5**

```python
lpf2 = np.array([
    [1/10, 1/10, 1/10],
    [1/10, 1/5,  1/10],
    [1/10, 1/10, 1/10]
], dtype=np.float32)
```

**LPF 3 – Kernel Rata-rata**

```python
lpf3 = np.ones((3, 3), dtype=np.float32) / 9
```

Penerapan menggunakan `cv2.filter2D()` dengan `cv2.CV_32F` dan `cv2.BORDER_CONSTANT`.

Hasil dikonversi menjadi `uint8` menggunakan `np.clip()` dan `np.rint()`.

**Visualisasi lima panel:**

1. Citra Asli
2. Citra Noisy
3. Hasil LPF 1
4. Hasil LPF 2
5. Hasil LPF 3

Output: `hasil_lpf1.png`, `hasil_lpf2.png`, `hasil_lpf3.png`.

### FR-02 – High Pass Filter

**File:** `filters/high_pass.py`

Menggunakan tiga kernel HPF sesuai materi praktikum.

**HPF 1 – Delapan Tetangga**

```python
hpf1 = np.array([
    [-1, -1, -1],
    [-1,  8, -1],
    [-1, -1, -1]
], dtype=np.float32)
```

**HPF 2 – Empat Tetangga**

```python
hpf2 = np.array([
    [ 0, -1,  0],
    [-1,  5, -1],
    [ 0, -1,  0]
], dtype=np.float32)
```

**HPF 3 – Bobot Diagonal**

```python
hpf3 = np.array([
    [ 1, -2,  1],
    [-2,  5, -2],
    [ 1, -2,  1]
], dtype=np.float32)
```

Penerapan menggunakan `cv2.filter2D()` dengan `cv2.CV_32F` dan `cv2.BORDER_CONSTANT`.

Konversi hasil:

```python
J1 = np.clip(np.floor(J1_float + 0.5), 0, 255).astype(np.uint8)
```

Konversi yang sama diterapkan pada J2 dan J3.

**Visualisasi lima panel:**

1. Citra Asli
2. Citra Noisy
3. HPF 1: 8-neighbor
4. HPF 2: 4-neighbor
5. HPF 3: Diagonal

Output: `hasil_hpf1.png`, `hasil_hpf2.png`, `hasil_hpf3.png`.

### FR-03 – Median Filter

**File:** `filters/median.py`

Median Filter digunakan untuk mengurangi Salt and Pepper Noise.

Pembuatan noise:

```python
noisy = img.copy()
rng = np.random.default_rng(42)
noise_mask = rng.random(img.shape[:2])

noisy[noise_mask < 0.02] = 0
noisy[noise_mask > 0.98] = 255
```

Penerapan filter:

```python
hasil_median = cv2.medianBlur(noisy, 3)
```

**Visualisasi tiga panel:**

1. Citra Asli
2. Citra Noisy
3. Hasil Median Filter

Gunakan `plt.figure(figsize=(12, 8))` dan `plt.subplot(1, 3, n)`.

Output: `outputs/hasil_mf.png`.

### FR-04 – Gaussian Filter

**File:** `filters/gaussian.py`

Gaussian Filter digunakan untuk menghaluskan citra menggunakan pembobotan Gaussian.

Pembuatan noise menggunakan Salt and Pepper Noise yang sama seperti pada Median Filter.

Penerapan filter:

```python
hasil_gaussian = cv2.GaussianBlur(
    noisy,
    (3, 3),
    sigmaX=1.0
)
```

**Visualisasi tiga panel:**

1. Citra Asli
2. Citra Noisy
3. Hasil Gaussian Filter

Gunakan `plt.figure(figsize=(12, 8))` dan `plt.subplot(1, 3, n)`.

Output: `outputs/hasil_gf.png`.

## 5. Standar Implementasi

Setiap file Python mengikuti pola:

1. Import library.
2. Membuat folder `outputs`.
3. Membaca gambar `images/living.jpg` menggunakan `cv2.IMREAD_GRAYSCALE`.
4. Memvalidasi gambar input.
5. Menampilkan ukuran dan tipe data citra.
6. Menambahkan noise sesuai kebutuhan praktikum.
7. Membuat kernel atau menentukan ukuran filter.
8. Menerapkan filtering.
9. Menampilkan hasil menggunakan Matplotlib.
10. Menyimpan citra hasil filtering.

Gunakan format grayscale dengan `cmap="gray"`, `vmin=0`, dan `vmax=255`.

Perbaiki kesalahan penamaan variabel atau judul pada materi agar program dapat berjalan dengan benar.

## 6. Menjalankan Program

Install dependency:

```bash
python -m pip install -r requirements.txt
```

Menjalankan masing-masing metode:

```bash
python -m filters.low_pass
python -m filters.high_pass
python -m filters.median
python -m filters.gaussian
```

Menjalankan seluruh metode:

```bash
python run_all.py
```

`run_all.py` menjalankan keempat metode secara berurutan dan menyimpan seluruh output.

## 7. Acceptance Criteria

- [ ] LPF menggunakan tiga matriks kernel sesuai PDF.
- [ ] HPF menggunakan tiga matriks kernel sesuai PDF.
- [ ] Median menggunakan kernel 3×3.
- [ ] Gaussian menggunakan kernel 3×3 dan sigmaX=1.0.
- [ ] Noise mengikuti contoh praktikum.
- [ ] Setiap metode menggunakan file Python terpisah.
- [ ] LPF dan HPF menampilkan lima panel.
- [ ] Median dan Gaussian menampilkan tiga panel.
- [ ] Seluruh hasil tersimpan dalam format PNG.
- [ ] Program dapat dijalankan secara mandiri maupun melalui `run_all.py`.
- [ ] Tidak menggunakan Streamlit, MATLAB, maupun GUI tambahan.

## 8. Deliverables

1. Source code empat metode filtering.
2. File gambar input.
3. Delapan gambar hasil filtering.
4. Script `run_all.py`.
5. `requirements.txt`.
6. `README.md`.

**Batasan:** Implementasi berfokus pada praktikum Image Filtering sesuai dua PDF materi dosen. Tidak diperlukan machine learning, database, atau aplikasi web.
