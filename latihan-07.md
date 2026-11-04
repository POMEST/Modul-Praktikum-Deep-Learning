# Latihan Mandiri di Lab - Modul 07

**Nama:** Abdillah Fikri Alpome  
**NIM:** 123450062  
**Kelas:** RC  

---

### Hasil dan perbandingan dengan prediksi

**Prediksi:**
Pemotongan menjadi 30 token kemungkinan mempercepat waktu per epoch, tetapi dapat menurunkan akurasi karena sebagian ringkasan teks terbuang. Dampak terbesar diperkirakan pada teks yang panjangnya >30 token, terutama golongan >40.

**Hasil:**
* **Waktu per Epoch:** Seperti yang diprediksi, pemotongan menjadi 30 token (MAKS=30) berhasil mempercepat waktu komputasi. Waktu per epoch turun dari 6,85 detik (MAKS=60) menjadi 4,56 detik (MAKS=30).
* **Akurasi Keseluruhan:** Penurunan akurasi juga terjadi sesuai dengan prediksi. Akurasi turun dari 0,7527 (MAKS=60) menjadi 0,7370 (MAKS=30), menghasilkan selisih penurunan sebesar -0,0157.
* **Dampak per Golongan Teks:**
    * **Golongan <20:** Mengalami penurunan akurasi dari 0,6744 menjadi 0,6279.
    * **Golongan 20-40:** Mengalami sedikit penurunan akurasi dari 0,7593 menjadi 0,7475.
    * **Golongan >40:** Sesuai dengan prediksi awal, golongan ini yang seharusnya terkena dampak pemotongan (karena teksnya dipangkas di atas token ke-30), mengalami penurunan akurasi dari 0,7464 menjadi 0,7266. 
    
Hal ini mengonfirmasi bahwa hilangnya informasi akibat pemotongan berimbas pada kemampuan model dalam memprediksi teks yang lebih panjang