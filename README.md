A little bit about me :D

Name  : Karen Lim  
NPM   : 2506623982  
Class : PBP C  

i like sightseeing~

### TUGAS 1
1. Iya, untuk sekarang saya baru menggunakan elemen <section> untuk membagi halaman saya menjadi beberapa bagian/kelompok, seperti bagian awal "About me" yang berisi nama, bio singkat, npm, dan program (jurusan) saya, lalu kelompok "Education History" yang menjadi bagian khusus untuk pendidikan saya, dan kelompok terakhir di paling bawah untuk menampilkan informasi kontak saya.

2. Tantangan utama yang saya alami adalah memastikan kotak-kotak sejajar yang berisi education history saya bisa tertata dengan rapih dan konsisten. Hal ini menjadi tantangan ketika saya sadar bahwa tampilan Education History dan kelompok informasi saya marginnya beda dengan kelompok pertama yang berisi "about me" saya bingung, dan tanyakan kepada AI apa yang sekiranya apa yang dapat menyebabkan hal tersebut terjadi. Setelah saya mengeceknya kembali, saya menemukan beberapa penulisan yang kurang teliti, seperti kurangnya penutup </div> dan lupa menambahkan <class="container> di bagian-bagian tersebut yang menyebabkan bedanya margin. Setelah menyelesaikan masalah itu, saya coba lagi di halaman _mobile_ dimana ternyata tampilan "kotak-kotak sejajar" itu terlihat aneh di _mobile_. Lalu saya menanyakan AI lagi tentang cara membuat kotak-kotak education history dapat menyesuaikan tampilan untuk desktop (horizontal) dan _mobile_ (vertikal). Saya akhirnya menggunakan media query, dengan @media (max-width: 600px) sehingga jika media query mendeteksi layar yang lebarnya <= 600px maka dia akan menunjukan tampilan _mobile_.

3. Untuk sekarang, saya merasa sangat tidak efisien (terbatas) ketika saya harus menambahkan riwayat pendidikan atau mengganti informasi mengenai capaian pada tahun pendidikan tertentu. Dimana pada web statis ini, saya harus membuka editor _code_ dan melakukan perubahan pada file HTML secara manual. Lalu, untuk fungsionalitas yang ingin saya tambahkan adalah integrasi database dan membuat sistemnya (webnya) dapat memanage isi konten pada web, agar saya bisa melakukan operasi _CRUD_ (Creade, Read, Update, Delete) secara langsung.

P.S. Tugas 1 ini saya kerjakan dengan bantuan AI, yaitu untuk memodifikasi style.css. Khususnya saya gunakan untuk mencari perkiraan sumber error dari _source code_ dimana masih saya lakukan pengecekan sendiri agar saya lihat langsung dan menjadi pelajaran untuk diingat kedepannya

