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

> **P.S.** Tugas 1 ini saya kerjakan dengan bantuan AI, gemini, untuk memodifikasi `style.css`. Khususnya saya gunakan untuk mencari perkiraan sumber error dari _source code_ dimana AI menunjukkan beberapa kekurangan tag (seperti `<div>`) dan media query. Setelah diberi tau masalahnya apa, saya coba pahami bagian mana yang bermasalah dan dampak/efek samping apa yang disebabkan dari kurangnya tag-tag tertentu. Saya juga melakukan pengecekan sendiri agar saya lihat langsung dan menjadi pelajaran untuk diingat kedepannya.

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

- **Validasi Data Terintegrasi:**

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

---

### TUGAS 4

> **P.S.** Tugas 4 ini saya kerjakan dengan bantuan Gemini AI, sebagai rekan diskusi saya dan asisten _debugging_ khususnya ketika error muncul.
>
> #### 1. **Strategi Prompting & Tools**
>
> - **Tools yang Digunakan:** Gemini 1.5 Pro / Flash.
> - **Strategi Prompting:**
>   - Menggunakan pendekatan _Chain-of-Thought_ untuk memecah logika implementasi fitur (seperti transisi data dari query set ke deserialisasi JSON).
>   - Melakukan validasi kritis terhadap kecocokan aturan modul dengan struktur kode yang ditulis (misalnya memastikan tipe data `IntegerField` vs `CharField` pada _ModelForm_ sesuai dengan kebutuhan validasi form).
>   - Menguji pemahaman arsitektur keamanan dengan mendiskusikan implementasi pembatasan akses server (_Server-side check_ & penanganan _Forbidden/PermissionDenied_) secara mandiri.
>
> #### 2. **Bagian Spesifik yang Dibantu AI**
>
> - **Deserialisasi JSON & ModelForm:** AI membantu memetakan ulang fungsi `show_education` agar tidak lagi mengambil data langsung dari basis data mentah, melainkan melalui proses deserialisasi objek JSON. Namun, saya melakukan _refactoring_ dan penyesuaian manual pada _mapping field_ di `forms.py` agar atribut penamaan variabel konsisten dengan model yang ada.
> - **Otorisasi & Keamanan Sisi Server:** AI memberikan panduan implementasi pelindung _view_ CRUD. Saya secara aktif memverifikasi kesesuaian proteksi tersebut dengan menguji coba akses ilegal secara manual di peramban untuk memastikan respons _Forbidden_ berjalan semestinya.
> - **Dokumentasi & Analisis:** Membantu menstrukturkan poin-poin penjelasan teknis agar selaras dengan standar dokumentasi _open-source_, yang kemudian saya kurasi ulang agar sesuai dengan konteks implementasi nyata pada proyek saya.
>
> #### 3. **Cuplikan Chat Log AI & Diskusi Saya**
>
> <details>
> <summary>Klik untuk melihat log diskusi saya dengan AI</summary>
>
> **Prompt 1 (Validasi Tipe Data ModelForm):**
>
> > _"Di model Education, aku pakai `end_year` sebagai CharField supaya bisa diisi 'Present' atau angka tahun, tapi field lainnya beda-beda tipe. Apakah ini sudah aman dikategorikan minimal 3 tipe data bervariasi di mata asdos dan Django?"_
>
> **Prompt 2 (Verifikasi Deserialisasi View):**
>
> > _"Fungsi `show_education` sebelumnya masih query langsung ke database. Bagaimana cara mengubahnya agar benar-benar merender data setelah melalui proses deserialisasi JSON dari endpoint view yang sudah dibuat tanpa merusak format template?"_
>
> </details>

---

### TUGAS 5

**1.** **Debouncing** adalah sebuah teknik yang sering diterapkan pada fitur pencarian AJAX untuk menunda eksekusi sebuah fungsi sampai jeda waktu tertentu berlalu sejak pengguna terakhir kali memicunya (misalnya, menunggu hingga pengguna berhenti mengetik selama 300 milidetik).

=> Teknik ini sangat penting untuk diterapkan pada fitur pencarian AJAX karena mencegah browser mengirimkan _request_ HTTP ke server pada setiap huruf yang diketik (_keystroke_). Tanpa debouncing, server bisa dibombardir oleh _request_ yang berlebihan atau secara terus menerus, sehingga membebani _bandwidth_, dan berpotensi memicu _race condition_ di mana balasan pencarian dari _request_ lama datang terlambat dan menimpa hasil dari _request_ yang paling baru.

**2.** Penggunaan `await` di fungsi `fetch()` berfungsi untuk menjeda eksekusi baris kode JavaScript selanjutnya secara asinkron sampai proses pengambilan data dari server selesai (mengembalikan _Promise_ yang sudah _resolved_ atau _rejected_).

=> Jika kita tidak menggunakan `await`, JavaScript tidak akan menunggu respons dari server dan langsung melompat mengeksekusi baris kode di bawahnya. Akibatnya, variabel penampung `fetch()` akan diisi objek _Promise_ yang statusnya masih _pending_ (belum selesai), bukan berisi balasan data respons HTTP yang sebenarnya. Hal ini akan menyebabkan program gagal pas ingin mencoba "mem-(_parsing_)" data tersebut jadi JSON.

**3.** **XSS (Cross-Site Scripting)** adalah celah keamanan di mana penyerang berhasil menyuntikkan skrip berbahaya (biasanya kode JavaScript) ke dalam sebuah aplikasi web. Skrip ini kemudian dieksekusi secara otomatis oleh browser pengguna lain yang mengakses halaman tersebut.

=> Data yang ditampilkan menggunakan AJAX lebih rentan terhadap serangan XSS karena pengembang sering kali menyisipkan data JSON mentah langsung ke dalam struktur HTML (DOM) menggunakan properti seperti `innerHTML`. Jika data tersebut mengandung tag `<script>`, browser akan langsung menjalankannya. Sebaliknya, _template_ bawaan Django memiliki fitur _auto-escaping_ yang secara otomatis menerjemahkan karakter berbahaya (seperti `<` menjadi `&lt;`) sebelum dirender ke HTML. Oleh karena itu, pada AJAX, kita harus melakukan sanitasi (seperti memanggil fungsi khusus `escapeHtml()`) secara manual.

---

> **P.S.** Tugas 5 ini saya kerjakan dengan bantuan Gemini AI, sebagai rekan diskusi saya, asisten _debugging_ serta sebagai _buddy scripting_.
>
> #### 1. **Strategi Prompting & Tools.**
>
> - Tools yang saya gunakan adalah Gemini 1.5 Pro / Flash.
> - **Strategi Prompting:** Menggunakan _Iterative Debugging_ (mengirimkan pesan error spesifik beserta potongan kode) serta _Deep Dive_ untuk meminta penjelasan fundamental di balik sebuah _bug_ atau aturan kode.
>
> #### 2. **Bagian Spesifik yang Dibantu AI**
>
> - **Konsep & Arsitektur:** Memahami perbedaan alur kerja dalam merakit JSON secara manual di _backend_ dengan fitur serialisasi bawaan Django, serta cara merancang arsitektur keamanan dengan dekorator Django yang bertumpuk.
> - **Troubleshooting:** Menganalisis mengapa form pengiriman AJAX "bocor" (gagal dicegat) dan memicu _redirect_ ke halaman JSON mentah, serta melacak penyebab munculnya tumpukan _flash messages_ usang pada halaman Login.
> - **Keamanan Frontend:** Menerapkan pengiriman token CSRF melalui _header_ HTTP dan membentengi injeksi DOM dengan fungsi _escaping_ manual di sisi JavaScript.
>
> #### 3. **Cuplikan Chat Log AI**
>
> <details>
> <summary> Klik untuk melihat log diskusi dengan AI</summary>
>
> **Prompt 1 (Analisis Arsitektur Keamanan Django):**
>
> > _"Saya melihat ada penumpukan decorator `@require_POST` dan `@login_required` di atas satu fungsi view yang sama. Secara teknis, apa perbedaan spesifik dari peran kedua decorator ini? Apakah aman dan termasuk best practice jika kita menggabungkannya, terutama untuk endpoint AJAX yang mengekspektasikan balasan JSON alih-alih redirect halaman HTML?"_
>
> **Prompt 2 (Debugging Alur Asinkron & DOM):**
>
> > _"Saat saya menekan tombol submit pada form di dalam modal, browser saya malah berpindah memuat halaman raw JSON yang menampilkan respons dari server (`{"message": "Berhasil...", "pk": "..."}`). Padahal, logika `fetch()` dan modal popover sudah saya siapkan. Mengapa JavaScript gagal mencegat event submit ini, dan di mana letak kesalahan urutan eksekusinya?"_
>
> </details>

---

### TUGAS 6

**1.** **REST (Representational State Transfer)** adalah salah 1 bentuk API yang memiliki batasan-batasan jelas, seperti _resource_ yg memiliki URL sendiri (misal `/api/v1/education/<id>/`), operasinya didefinisikan lewat _method_ HTTP (GET untuk membaca, POST membuat, PUT/PATCH mengubah, DELETE menghapus), bersifat _stateless_, dan menggunakan status HTTP yang bermakna.

=> Mengembalikan format data JSON saja tidak cukup untuk menyebut sebuah API RESTful. Sebuah _endpoint_ seperti `/delete-education/<id>/` yang membalas status 200 berisi JSON tetap melanggar prinsip REST karena aksinya (delete) diletakkan pada URL, bukan pada _method_ HTTP. Terkait _update_, **PUT** mengganti keseluruhan _resource_ sehingga semua _field_ wajib dikirim, sedangkan **PATCH** hanya untuk pembaruan parsial (misalnya digunkaan ketika Editor yang hanya mengubah _description_ tanpa menyentuh _school_name_).

**2.** **Serializer** dalam Django REST Framework (DRF) berfungsi sebagai penerjemah yang mengubah objek model ke JSON (serialisasi) dan memproses input JSON menjadi data yang tervalidasi (deserialisasi), sekaligus menjalankan aturan validasi khusus seperti `validate_<field>`.

=> Dibandingkan merakit _dictionary_ secara manual menggunakan `JsonResponse`, _serializer_ sangat menguntungkan karena semua aturan _field_, validasi, dan _field_ perhitungan (`star_count`, `is_starred`) terpusat di satu tempat. Ini memungkinkan _serializer_ dipakai berulang untuk berbagai aksi seperti list, detail, create, update, melindungi _field read-only_ dari input klien, serta otomatis memformat error validasi menjadi respons HTTP 400 tanpa mengulang-ulang kode (DRY principle).

**3.** **Autentikasi dan Otorisasi** adalah teknik verifikasi yg berbeda. Autentikasi mendeteksi "Siapa kamu?" (ditangani `SessionAuthentication` yang mengenali _user_ dari _cookie session_), sedangkan Otorisasi mengecek "Apa yang boleh kamu lakukan?" (ditangani _permission class_ seperti `IsPortfolioOwnerOrEditorOrReadOnly`).

=> Pengecekan hak akses ini mutlak harus dilakukan di sisi _backend_ (server). Menyembunyikan tombol Edit/Delete di _template_ (frontend) hanya memanipulasi tampilan; tanpa validasi di server, siapa pun bisa mengirim _request_ langsung melalui `curl`, Postman, atau _console_ browser ke _endpoint_ yang sama. Hanya pemeriksaan di server yang benar-benar bisa menolak _request_ tak berizin.

**4.** **SessionAuthentication** membuat browser otomatis menyertakan _cookie session_ pada setiap _request_ ke domain kita. Tanpa pengamanan ekstra, situs jahat bisa memicu browser korban untuk mengirim POST/PATCH/DELETE (serangan CSRF). Oleh karena itu, DRF mewajibkan token CSRF (header `X-CSRFToken`) untuk setiap _method_ yang memutasi data.

=> Saat melakukan _testing_, fungsi `force_authenticate` akan melewati proses autentikasi _session_ sepenuhnya, sehingga pemeriksaan token CSRF tidak pernah dijalankan (tes terlihat sukses pdahal di _production_ gagal). Maka, tes harus menggunakan `APIClient(enforce_csrf_checks=True)` dan fungsi `.login()` untuk menggunakan alur _session_ sungguhan, untuk membuktikan bahwa _request_ tanpa token akan ditolak (403).

---

> **P.S.** Tugas 6 ini saya kerjakan dengan bantuan Gemini AI, sebagai rekan diskusi saya, asisten _debugging_ serta sebagai _buddy scripting_.
>
> #### 1. **Strategi Prompting & Tools**
>
> - **Tools:** Gemini (berperan sebagai _buddy scripting_ dan asisten _debugging_).
> - **Strategi Prompting:** Saya memberik konteks dari berdasarkan tutorial 7, dan meminta ai untuk menuntun implementasi yang sama ke modul aku lainnya agar sintaks AI tetap selaras dengan struktur proyek saya. Saya juga menggunakan _Deep Dive Prompting_ yang berfokus pada diskusi fundamental (seperti siklus hidup _request-response_ di DRF) alih-alih sekadar meminta _generate_ kode.
>
> #### 2. **Bagian Spesifik yang Dibantu AI & Pengerjaan Manual**
>
> - **Bagian yang Dibantu AI (Kerangka & Konseptual):** Melakukan _brainstorming_ terkait _best practice_ pemisahan _business logic_ ke dalam `ModelSerializer` (termasuk penanganan _computed fields_), merumuskan rancangan hierarki _permission class_, serta mendiskusikan kerangka asinkron `fetch` API untuk fungsionalitas _modal_ PATCH dan _toast_. AI juga membantu membuat draf struktur skenario _edge-case_ untuk `APITestCase`.
> - **Integrasi & Pemecahan Masalah Manual:** Saya secara mandiri mengorkestrasi penggabungan _permission class_ agar sesuai dengan _role-based access_ spesifik di proyek saya. Selain itu, saya harus memetakan ulang _payload_ dari _form_ HTML agar sinkron dengan _fields_ yang diekspektasikan oleh _serializer_, serta memburu dan menyelesaikan _bug_ otentikasi saat melakukan _testing_ integrasi secara manual.
> - **Tinjauan Kritis terhadap Keterbatasan AI:** AI sering kali mengalami "halusinasi struktural" terkait manipulasi DOM karena tidak memiliki visibilitas spasial terhadap hierarki elemen di `education.html`. Resolusi yang diberikan oleh AI untuk JavaScript kerap keliru dalam menargetkan ID/Class. Oleh karena itu, saya harus menganalisis ulang alur DOM dan menulis ulang logika _query selector_ secara manual agar eksekusi AJAX berjalan presisi.
>
> #### 3. **Cuplikan Chat Log AI**
>
> <details>
> <summary> Klik untuk melihat tinjauan analitis bersama AI</summary>
>
> **Prompt 1 (Analisis Komparatif Arsitektur DRF):**
>
> > _"Berdasarkan kode Tutorial 07, apa kelebihan arsitektural yang didapat dengan memindahkan proses perakitan JSON dari metode manual `JsonResponse` menjadi terpusat pada `ModelSerializer` di DRF? Tolong bedah signifikansinya dalam konteks enkapsulasi validasi, penanganan computed fields, dan penerapan DRY principle."_
>
> **Prompt 2 (Debugging Celah Keamanan Sesi & Testing):**
>
> > _"Saat saya menjalankan `APITestCase` untuk menguji endpoint PATCH, penggunaan `force_authenticate` membuat tes saya lolos (passed) meskipun payload tidak menyertakan token CSRF. Namun, ketika saya mereplikasinya langsung via browser, request tersebut justru diblokir (403 Forbidden). Apa yang terlewat dari siklus SessionAuthentication saat testing, dan bagaimana cara memodifikasi konfigurasi `APIClient` agar mensimulasikan injeksi CSRF secara otentik layaknya di production?"_
>
>
> </details>