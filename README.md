# Snake Game - Edisi Level Progresif

Sebuah game Snake klasik yang dibangun menggunakan Python dan library Pygame. Game ini tidak hanya sekadar game Snake biasa, tetapi dilengkapi dengan berbagai level, rintangan, dan sistem kecepatan yang meningkat secara progresif untuk memberikan tantangan lebih.

![Gameplay Snake Game](https://user-images.githubusercontent.com/2646532/121356963-df5f6180-c97c-11eb-9c29-399a99787a17.gif)



## Deskripsi

Project ini adalah implementasi dari game Snake yang ikonik dengan sentuhan modern. Pemain dapat memilih tingkat kesulitan yang berbeda, masing-masing dengan rintangan dan kecepatan awal yang unik. Fitur utamanya adalah kecepatan yang akan terus bertambah seiring dengan perolehan skor, membuat permainan semakin sulit dan menantang.


## Fitur Utama

-   🐍 **Sistem Level**: Terdapat 7 level kesulitan, dari "Baby" hingga "Expert", masing-masing dengan layout rintangan yang berbeda.
-   🚀 **Kecepatan Progresif**: Kecepatan ular akan bertambah secara otomatis setiap pemain mendapatkan 5 skor, memberikan tantangan dinamis.
-   🏆 **Skor Tertinggi (High Score)**: Game secara otomatis menyimpan skor tertinggi yang pernah dicapai, bahkan setelah game ditutup.
-   🎵 **Musik dan Suara Dinamis**: Latar belakang musik berubah sesuai dengan tingkat kesulitan level yang dipilih, ditambah dengan efek suara saat ular makan.
-   ⏸️ **Jeda Permainan**: Pemain dapat menjeda dan melanjutkan permainan kapan saja dengan menekan tombol **'P'**.
-   🧱 **Rintangan Bervariasi**: Setiap level memiliki konfigurasi dinding rintangan yang unik.


## Teknologi yang Digunakan

-   **Python 3**
-   **Pygame**


## Instalasi dan Cara Menjalankan

Ikuti langkah-langkah berikut untuk menjalankan game ini di komputer Anda.

### 1. Prasyarat

Pastikan Anda sudah menginstal **Python 3** di sistem Anda.

### 2. Klon Repositori

Buka terminal atau command prompt, lalu klon repositori ini:
```bash
<<<<<<< main
git clone https://github.com/hayyanjpg/game_ular.git
cd game_ular
=======
git clone [https://github.com/hayyanjpg/game_ular.git]
>>>>>>> main
```

### 3. Instalasi Dependensi

Instal library Pygame yang dibutuhkan melalui pip.
```bash
pip install pygame
```

### 4. Struktur Folder

Pastikan semua file suara (.mp3, .wav) berada di dalam folder `assets` agar game dapat memuatnya dengan benar.
```
.
├── nama_game.py
└── assets/
    ├── suara_makan.mp3
    ├── backsound.wav
    └── ...

### 5. Jalankan Game

Eksekusi file Python utama untuk memulai permainan.
```bash
game_ular.py
```
* sesuain aja  disini aku namainnya `game_ular.py` 


## Lisensi

Didistribusikan di bawah Lisensi MIT. Lihat file `LICENSE` untuk informasi lebih lanjut.
