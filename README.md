# Praktikum Deep Learning - Abdillah Fikri Alpome

NIM **123450062** | Kelas **RC** | 27 Oktober 2026

## Hasil per modul

| Modul | Notebook | Laporan | Metrics | Latihan |
|---|---|---|---|---|
| 01 | [Notebook](notebooks/modul-01/M01_123450062.ipynb) | [PDF](notebooks/modul-01/M01_123450062.pdf), [sumber](notebooks/modul-01/M01_123450062.md) | [CSV](notebooks/modul-01/M01_123450062_metrics.csv) | [Catatan](notebooks/modul-01/latihan-01.md) |
| 02 | [Notebook](notebooks/modul-02/M02_123450062.ipynb) | [PDF](notebooks/modul-02/M02_123450062.pdf), [sumber](notebooks/modul-02/M02_123450062.md) | [CSV](notebooks/modul-02/M02_123450062_metrics.csv) | [Catatan](notebooks/modul-02/latihan-02.md) |
| 03 | [Notebook](notebooks/modul-03/M03_123450062.ipynb) | [PDF](notebooks/modul-03/M03_123450062.pdf), [sumber](notebooks/modul-03/M03_123450062.md) | [CSV](notebooks/modul-03/M03_123450062_metrics.csv) | [Catatan](notebooks/modul-03/latihan-03.md) |
| 04 | [Notebook](notebooks/modul-04/M04_123450062.ipynb) | [PDF](notebooks/modul-04/M04_123450062.pdf), [sumber](notebooks/modul-04/M04_123450062.md) | [CSV](notebooks/modul-04/M04_123450062_metrics.csv) | [Catatan](notebooks/modul-04/latihan-04.md) |

Semua notebook telah dieksekusi dari kernel baru secara berurutan. M01 memakai
seed **1062**; M02-M04 memakai seed **62**, dan pencarian M04 memakai seed **63**.
Dataset Fashion-MNIST tersimpan lokal di `data/raw/` dan tidak ikut Git.
M01 memiliki 8 run; M02 memiliki 59 baris (53 komponen gradient check dan
6 run loop); M03 dan M04 masing-masing 18 run. Semua hasil tetap dicatat.

## Pemeriksaan akhir

Checkpoint resmi **Mode tugas** telah lulus: Modul 01 **10/10**, Modul 02 **11/11**,
Modul 03 **10/10**, dan Modul 04 **10/10**. Log lengkap, termasuk percobaan
sebelum perbaikan format identitas, disimpan di [catatan checkpoint](notebooks/checkpoint-mode-tugas.txt).
Lulus checkpoint tidak berarti tugas sudah dikumpulkan.

## Reproduksi

Jalankan notebook menggunakan lingkungan PyTorch CPU DSWorkbench. Buka berkas
di folder modul dan gunakan **Restart Kernel and Run All**. Setelah itu:

```bash
python -m pip install -r requirements.txt -r requirements-tools.txt
python scripts/export_reports.py
```

Pembuat laporan membaca hasil aktual di `notebooks/modul-XX/hasil/`; tidak
melatih model atau mengevaluasi test lagi. M01/M03/M04 memakai test satu kali
setelah pemilihan validasi; M02 merupakan pemeriksaan algoritme tanpa test.
Laporan M01-M04 tersedia dalam PDF, masing-masing maksimal dua halaman.
Sumber Markdown juga disimpan untuk memudahkan revisi. Kolom metrics mengikuti template; M02 menambahkan kolom
`record_type` yang diwajibkan checkpoint. Template resmi tidak diubah.

## Pengumpulan DSWorkbench

Arsip utama berada dalam folder setiap modul. Salinan aktif notebook, laporan,
metrics, dan latihan disediakan pada akar folder mata kuliah agar dapat dibaca
Local Runner saat checkpoint/pengumpulan. Salinan itu diabaikan Git. Jalur
gambar pada laporan salinan diarahkan ke folder modul.

Lima jawaban analisis setiap modul tersedia pada output/sel pembahasan notebook
dan `hasil/analisis-formulir.json` untuk dipindahkan praktikan ke formulir tugas.
Pengumpulan dilakukan setelah praktikan meninjau kode, hasil, dan laporan.

## Sumber dan bantuan

Kerangka kode diadaptasi dengan izin dari praktikum Fabio Banyu Cyto:
https://github.com/fabiobanyu/deep-learning-123450104 . Seluruh eksperimen di
repo ini dijalankan ulang untuk NIM 123450062; angka lama tidak disalin sebagai
hasil baru. OpenAI Codex membantu implementasi, pemeriksaan, dan draf analisis.
Materi serta starter resmi DSWorkbench dan dokumentasi pustaka dirujuk pada
notebook dan laporan. Praktikan perlu memahami hasil sebelum mengumpulkan.
