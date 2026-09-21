# Heloo this is git repo shows my portfolio :D

My name is Karen Lim, and you can call me Karen or whatever is comfortable with you!
You can access my portfolio by following this setup:

1. `git clone https://github.com/clarenvc/myportfolio.git`
2. `cd myportfolio`
3. `python -m venv env`
4. **Activate virtual environment:**
   - For macOS: `source env/bin/activate`
   - For Windows: `env\Scripts\activate`
5. `pip install -r requirements.txt`
6. `python manage.py makemigrations`
7. `python manage.py migrate`
8. `python manage.py runserver`

See you there~

Down below is for answering reflective questions to complete for _Platform-Based Programming_ weekly task.

### TUGAS 1

**1.** Iya, untuk sekarang saya baru menggunakan elemen `<section>` untuk membagi halaman saya menjadi beberapa bagian/kelompok, seperti bagian awal "About me" yang berisi nama, bio singkat, npm, dan program (jurusan) saya, lalu kelompok "Education History" yang menjadi bagian khusus untuk pendidikan saya, dan kelompok terakhir di paling bawah untuk menampilkan informasi kontak saya.

**2.** Tantangan utama yang saya alami adalah memastikan kotak-kotak sejajar yang berisi _education history_ saya bisa tertata dengan rapih dan konsisten. Hal ini menjadi tantangan ketika saya sadar bahwa tampilan Education History dan kelompok informasi saya marginnya beda dengan kelompok pertama yang berisi "about me" saya bingung, dan tanyakan kepada AI apa yang sekiranya apa yang dapat menyebabkan hal tersebut terjadi. Setelah saya mengeceknya kembali, saya menemukan beberapa penulisan yang kurang teliti, seperti kurangnya penutup `</div>` dan lupa menambahkan `class="container"` di bagian-bagian tersebut yang menyebabkan bedanya margin. Setelah menyelesaikan masalah itu, saya coba lagi di halaman _mobile_ dimana ternyata tampilan "kotak-kotak sejajar" itu terlihat aneh di _mobile_. Lalu saya menanyakan AI lagi tentang cara membuat kotak-kotak education history dapat menyesuaikan tampilan untuk desktop (horizontal) dan _mobile_ (vertikal). Saya akhirnya menggunakan media query, dengan `@media (max-width: 600px)` sehingga jika media query mendeteksi layar yang lebarnya `<= 600px` maka dia akan menunjukan tampilan _mobile_.

**3.** Untuk sekarang, saya merasa sangat tidak efisien (terbatas) ketika saya harus menambahkan riwayat pendidikan atau mengganti informasi mengenai capaian pada tahun pendidikan tertentu. Dimana pada web statis ini, saya harus membuka editor _code_ dan melakukan perubahan pada file HTML secara manual. Lalu, untuk fungsionalitas yang ingin saya tambahkan adalah integrasi database dan membuat sistemnya (webnya) dapat memanage isi konten pada web, agar saya bisa melakukan operasi _CRUD_ (Create, Read, Update, Delete) secara langsung.

> **P.S.** Tugas 1 ini saya kerjakan dengan bantuan AI, gemini, untuk memodifikasi `style.css`. Khususnya saya gunakan untuk mencari perkiraan sumber error dari _source code_ dimana AI menunjukkan beberapa kekurangan tag (seperti </div>) dan media query. Setelah diberi tau masalahnya apa, saya coba pahami bagian mana yang bermasalah dan dampak/efek samping apa yang disebabkan dari kurangnya tag-tag tertentu. Saya juga melakukan pengecekan sendiri agar saya lihat langsung dan menjadi pelajaran untuk diingat kedepannya.

---

### TUGAS 2

**1.** Ketika _request_ atau permintaan membuka halaman portofolio diterima oleh proyek, permintaan pertama tersebut akan diterima oleh `urls.py` di tingkat proyek (yang ada di folder portfolio) dari `urls.py` proyek ini dia akan mencari `include('main.urls')` yang kemudian nanti akan diarahkan ke aplikasi main. Disinilah `urls.py` aplikasi berperan. Misal user meminta halaman skills, maka `urls.py` akan mencocokan rutenya, dalam hal ini, ke `path("skills/", show_skills, name="show_skills")`. Setelah cocok, _URL dispatcher_ akan memanggil fungsi yang berhubungan ke `views.py`. `views.py` ini kemudian akan memanggil fungsi `show_skills` yang berperan sebagai operator dan menyimpan variabel-variabel yang dibutuhkan oleh model tertentu (dalam hal ini model skills). Setelah view menyiapkan dan memanggil `models.py`, `models.py` akan mengambil data dari tabel database (`db.sqlite3`), dan setelah mendapatkan datanya, `models.py` akan mengembalikan datanya dalam bentuk QuerySet ke `views.py`. Dari sini `views.py` sudah siap mengirimkan data yang sudah dirapihkan dan tinggal dipasang ke template (dalam hal ini `skills.html`).

**2.** Ada 2 alasan utama yaitu:

- **Kemudahan pemeliharaan (Maintanability)**
  => Karena akan lebih aman dan lebih mudah ketika ingin menambah, mengedit, atau menghapus data yang tersimpan di model melalui halaman Django Admin atau Django shell (tidak hard-coded). Daripada harus membuka file HTML nya dan mencari data yang ingin diubah dari sekian banyaknya baris yang ada, belum lagi jika tidak sengaja mengubah bagian lain yang tidak berhubungan.
- **Pengembangan aplikasi (Scalability)**
  => Data yang disimpan oleh model bersifat dinamis dan terpusat di SQLite (`db.sqlite3`). Sehingga lebih mudah untuk memanipulasi data misal jika ingin melalukan _sorting_ atau mengurutkan data (misal: _newest to oldest_) atau bisa juga untuk melakukan _filtering_ (untuk kategori tertentu) di berbagai halaman sekaligus, tanpa perlu mengubah 1 per 1 file htmlnya.

**3.** _Makemigrations_ dan _migrate_ keduanya sama-sama digunakan jika ada perubahan di model. Tapi, _makemigrations_ itu lebih berperan sebagai yang meng-"save" ketika ada perubahan di model. Fungsi ini akan membandingkan dengan kondisi sebelumnya, dan menyimpan perubahan jika diperlukan. Sementara _migrate_ itu yang menerapkan atau meng-"execute" perubahan yang disimpan oleh si _makemigrations_. Fungsi _migrate_ tadi akan menerjemahkannya menjadi perintah SQL dan menerapkan perintah tersebut ke dalam database (benar-benar melakukan aksi seperti membuat tabel atau kolom baru di SQLite).

Contoh perubahan pada model yang membutuhkan _makemigrations_ dan _migrate_:
=> Pada model skills yang aku tambahkan kemarin untuk Tugas 2, aku baru sadar bahwa aku belum menambahkan klasifikasi untuk tingkat skill yang aku miliki (mau melakukan sorting tingkat skill dari _beginner, intermediate, proficient_) maka aku harus melakukan perubahan di `models.py` pada class `Skill`. Misal aku menambahkan field baru dengan kode:

`proficiency_level = models.CharField(max_length=50)`

setelah menambahkan baris kode baru itu dan melakukan _makemigrations_, fungsi ini akan meng-"save" perubahan terbaru tersebut. Lalu, ketika memanggil fungsi _migrate_ django akan membuat perintah SQL dan menerapkan perintah tersebut dan segera membuat perubahan (_sorting_) yang diminta oleh aku sebelumnya di database.

> **P.S.** Tugas 2 ini saya kerjakan dengan bantuan Gemini AI, yaitu untuk kembali melakukan modifikasi `style.css`. Misalnya pada Tugas 2 ini saya menambahkan freeze pada _navbar_ dan meminta design untuk kotak-kotak yang saya gunakan di model experience dan skill. Selain itu, saya juga menggunakan gemini untuk membuatkan contoh file `tests.py` yang diperlukan untuk Tugas 2. Selain itu, saya juga meminta gemini untuk menjelaskan lagi perbedaan antara model, view, dan template besertakan contohnya agar lebih terbayang, dan kurang lebih terakhir saya juga gunakan gemini untuk menanyakan soal penggunaan Django Admin (karena tampilan data yang saya sertakan di model experience dan skill hanya muncul ketika aku buka di local dan tidak muncul jika aku buka dari pws), kemungkinan akan saya terapkan setelah Tugas 2.

---

### TUGAS 3

**1.** _ModelForm_ lebih disarankan dibanding membuat form HTML secara manual karena ada beberapa prinsip fundamental dalam pemrograman demi kelancaran pengembangan dan pemeliharan dan pengembangan aplikasi, antara lain:

- **DRY (Don't Repeat Yourself) & Integrasi Otomatis:**
  => _ModelForm_ secara otomatis membuatkan elemen input HTML berdasarkan struktur field yang sudah didefinisikan pada Model Django. Dengan menerapkan prinsip DRY, aplikasi menjadi lebih mudah dirawat, mencegah terjadinya bug atau inkonsistensi ketika ingin menyalin atau menempelkan kode baru, dan kode juga menjadi lebih bersih (ringkas, mudah dibaca, dan lebih rapih).

  **Validasi Data Terintegrasi:**
  => Selain itu, _ModelForm_ juga menangani proses validasi tipe data (seperti tipe angka pada _IntegerField_ atau teks pada _CharField_) dan sanitasi data secara otomatis sebelum disimpan ke basis data.

Terakhir, `{% csrf_token %}` wajib ditambahkan untuk meningkatkan keamanan aplikasi kita dari serangan CSRF _(Cross-site Request Forgery)_ dengan menyisipkan token rahasia unik pada setiap form dengan metode `POST`.

**2.** _JSON_ lebih disukai dalam pengembangan aplikasi modern karena formatnya yang ringan untuk menyimpan dan mentransfer data. Selain itu, sintaks _JSON_ juga identik dengan kode yang sering dipakai untuk membuat objek JavaScript, sehingga lebih familiar bagi para programmer dan lebih mudah bagi program JavaScript untuk mengubah data _JSON_ menjadi objek JavaScript asli. Terakhir, untuk aplikasi AJAX, _JSON_ lebih cepat dan lebih mudah dibanding XML.

**3.** Alur Pengambilan Data JSON pada View:

- a. **Permintaan (Request):** Klien/browser mengirimkan permintaan HTTP GET ke endpoint URL yang dipetakan ke fungsi view (misalnya `/json/`).
- b. **Pengambilan Data (Querying):** Fungsi view memanggil model Django untuk mengambil objek data dari database (menghasilkan QuerySet).
- c. **Deserialisasi/Serialisasi (Serialization):** Objek QuerySet diproses oleh modul serializers bawaan Django untuk diubah dari bentuk objek Python/Django menjadi string format JSON.
- d. **Respons (Response):** Fungsi view mengembalikan data JSON tersebut menggunakan HttpResponse dengan `content_type="application/json"`.

Terakhir, proses _serialization_ sangat dibutuhkan karena objek model/QuerySet pada Django adalah objek Python kompleks yang tersimpan di memori server dan tidak bisa dikirimkan langsung melalui protokol HTTP. Selain itu, proses ini juga diperlukan untuk menerjemahkan objek Python tersebut menjadi format data standar (seperti string _JSON_) yang dapat dipahami, ditransfer, dan diolah oleh aplikasi atau framework lain (misalnya seperti JavaScript di frontend).

> **P.S.** Tugas 3 ini saya kerjakan dengan bantuan Gemini AI, sebagai rekan diskusi saya dan asisten _debugging_.
>
> #### 1. **Strategi Prompting & Tools.**
>
> - Tools yang saya gunakan adalah Gemini 1.5 Pro / Flash.
> - **Strategi Prompting:** Menggunakan _Chain-of-Thought_ (meminta penjelasan step-by-step), konfirmasi berulang terhadap aturan di modul, serta analisis kritis terhadap _error_ dan _best practice_ struktur Django.
>
> #### 2. **Bagian Spesifik yang Dibantu AI**
>
> - **Konsep & Arsitektur:** Memahami alur kerja _Template Inheritance_ (`base.html`), serialisasi data _JSON_, serta mekanisme keamanan `csrf_token`.
> - **Troubleshooting:** Menganalisis perbedaan data antara basis data lokal dan PWS, serta cara penggunaan _data fixture_ (`dumpdata` / `loaddata`).
> - **Dokumentasi:** Memformulasikan jawaban pertanyaan analisis pada README agar tepat secara teknis.
>
> #### 3. **Cuplikan Chat Log AI**
>
> <details>
> <summary> Klik untuk melihat log diskusi dengan AI</summary>
>
> **Prompt 1 (Validasi Urutan Element HTML):**
>
> > _"Di modul tutorial ditulis `<link rel="stylesheet">` ada di atas `{% block meta %}`, tapi secara best practice mana yang lebih disarankan? Apakah ada pengaruh ke rendering browser?"_
>
> **Prompt 2 (Sinkronisasi Database PWS vs Lokal):**
>
> > _"Saya sudah jalankan `loaddata` di terminal lokal, tapi web PWS masih kosong. Apakah file `db.sqlite3` memang tidak di-push ke Git? Bagaimana cara menyinkronkan data dari lokal ke PWS menggunakan fixture?"_
>
> </details>
