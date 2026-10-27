# Latihan Mandiri Modul 02

Abdillah Fikri Alpome | 123450062 | RC | 2026-10-27 | seed 62 | float64

## Prediksi sebelum menjalankan

Saya memperkirakan norma gradien W1 mengecil saat ReLU diganti tanh karena turunannya1-tanh(z1)^2 berada di bawah 1 pada z1=(1,5;1). Besar p-y juga berubah, sehingga prediksi harus diuji, bukan hanya melihat turunan aktivasi.

## Turunan manual tanpa autograd

h=[tanh(1,5),tanh(1)], z2=2h1-h2+0,5, d=sigmoid(z2)-1.

dz1=d*[2,-1]*[1-tanh(1,5)^2,1-tanh(1)^2].

dW1=outer(dz1,[2,-1]); db1=dz1; dW2=d*h; db2=d.

## Hasil aktual dan perbandingan

Norma dW1 ReLU 0.379290900, tanh 0.217154934; turun 42.75%. Dz1 tanh adalah [[-0.06334626700390387, 0.07361048530682761]]. BCE tanh 0.192703788 dan probabilitas 0.824726232. Sembilan komponen diperiksa: maksimum relative error 1.769e-10, sesuai ambang1e-5. Autograd digunakan sesudah turunan NumPy untuk memverifikasi, bukan untuk menghasilkan turunan manual.

Prediksi pengecilan norma W1 didukung, tetapi tidak berlaku untuk seluruh gradien: faktor p-y berubah dan dapat membesar. Nilai dW1 lengkap adalah [[-0.12669253400780775, 0.06334626700390387], [0.14722097061365522, -0.07361048530682761]]; semua angka tersedia pada hasil/M02_123450062_gradients.csv. Karena Kasus 1 memakai parameter tetap, hasil bagian ini sama untuk beberapa NIM; loop XOR memakai seed 62 dan dihitung ulang.

Implementasi mengadaptasi kode praktikum Fabio Banyu Cyto dengan izin serta starter DSWorkbench. Seluruh perhitungan dijalankan ulang menggunakan NIM individual. OpenAI Codex digunakan untuk membantu implementasi, pemeriksaan, dan penyusunan draf pembahasan.
