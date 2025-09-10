https://rheina-adinda-strikeapparel.pbp.cs.ui.ac.id/

1. Jelaskan bagaimana cara kamu mengimplementasikan checklist di atas secara step-by-step (bukan hanya sekadar mengikuti tutorial).

Membuat sebuah proyek Django baru.
-> siapkan folder proyek dan virtual environment supaya dependensi terisolasi dari sistem, ini mencegah konflik versi library antar proyek dan memudahkan reproducibility. Setelah mengaktifkan venv saya menginstal Django (dan  python-dotenv untuk membaca environment variable) lalu menjalankan django-admin startproject untuk membuat struktur dasar proyek. Sebelum melanjutkan saya menjalankan python manage.py migrate untuk memastikan skema database awal dibuat, dan runserver untuk memverifikasi bahwa proyek bisa dijalankan secara lokal — jika ada error, saya periksa settings.py. Saya juga membuat .gitignore yang memasukkan env/, .env, dan db.sqlite3 agar tidak meng-commit file sensitif lokal.

Membuat aplikasi dengan nama main pada proyek tersebut.
-> Setelah proyek dasar berhasil, saya membuat app main dengan python manage.py startapp main untuk memisahkan modularisasi. Langkah berikutnya adalah mendaftarkan main di INSTALLED_APPS di settings.py sehingga Django mengenali model, view, dan template app ini. Pada tahap ini saya juga menyiapkan struktur folder templates/main/ dan static/main/ karena pemisahan template dan aset mempermudah pengembangan dan testing tampilan. Tujuannya agar setiap fitur (mis. produk) berada dalam satu app yang mudah diuji dan dipindahkan ke proyek lain bila perlu.

Melakukan routing pada proyek agar dapat menjalankan aplikasi main.
-> Saya buat file main/urls.py berisi pemetaan URL lokal aplikasi (mis. path('', views.show_main, name='show_main')) lalu meng-include file itu di level proyek (football_news/urls.py) sehingga root project diarahkan ke app main.  ini menjaga agar routing tingkat aplikasi tetap ringkas dan memudahkan tim untuk menambahkan route baru tanpa mengotori project/urls.py. Setelah include, saya jalankan server lokal dan mengunjungi http://localhost:8000 untuk memastikan view utama tampil. jika tidak, saya cek urutan include dan import error .

Membuat model pada aplikasi main dengan nama Product dan memiliki atribut wajib sebagai berikut.
-> Untuk model produk saya mendesain field berdasarkan kebutuhan fungsional: id bertipe UUIDField sebagai primary key agar unik dan aman saat direplikasi/di-merge; name (CharField) untuk nama, description (TextField) untuk deskripsi panjang; price memakai DecimalField (bukan float) supaya perhitungan uang tetap presisi; stock (PositiveIntegerField) untuk stok; thumbnail (ImageField) bila butuh gambar. Setelah membuat model, saya selalu melakukan makemigrations dan migrate, lalu cek admin Django (daftarkan model di admin.py) untuk memverifikasi data bisa dibuat/diedit lewat UI.

Membuat sebuah fungsi pada views.py untuk dikembalikan ke dalam sebuah template HTML yang menampilkan nama aplikasi serta nama dan kelas kamu.
-> Di views.py saya buat fungsi show_main(request) yang membangun context berisi app_name, name, dan class lalu memanggil render(request, 'main/main.html', context). Alasan menaruh data sederhana ini di context adalah untuk memisahkan logika controller (view) dan tampilan (template) sesuai prinsip MVT—view mempersiapkan data, template hanya menampilkan. Untuk template saya sarankan menggunakan template inheritance (base.html) agar nanti bisa menambah layout konsisten. 

Membuat sebuah routing pada urls.py aplikasi main untuk memetakan fungsi yang telah dibuat pada views.py.
-> Di main/urls.py saya tulis route eksplisit, berikan name pada route (mis. name='show_main') sehingga di template atau test bisa memakai reverse()/url dengan nama route, bukan hardcode URL. Memberi nama route memudahkan refactor URL tanpa mengubah banyak file. Setelah mapping dibuat, saya cek ulang konfigurasi include di level proyek dan jalankan test yang memanggil reverse('show_main') untuk memastikan route sudah benar.

Melakukan deployment ke PWS terhadap aplikasi yang sudah dibuat sehingga nantinya dapat diakses oleh teman-temanmu melalui Internet.
-> Untuk deployment saya ikuti alur pada tutorial: pertama pastikan repository bersih (hapus file sensitif), buat requirements.txt dengan pip freeze, dan pastikan gunicorn ada jika PWS membutuhkan WSGI server. Di settings.py saya ubah supaya membaca SECRET_KEY, DEBUG, dan ALLOWED_HOSTS dari environment variables — ini agar tidak menyimpan rahasia di repo. Selanjutnya push kode ke GitHub dan hubungkan repository ke PWS lewat dashboard SSO UI; di situ saya set environment variables (SECRET_KEY, DEBUG=false, ALLOWED_HOSTS=<host PWS>), dan jalankan prosedur deploy yang disediakan (beberapa PWS menyediakan automatic deploy dari branch main). Setelah deploy, saya cek logs dari panel PWS: jika aplikasi error saya periksa error stack (biasanya terkait SECRET_KEY, missing migrations, atau dependency). Untuk database produksi sebaiknya gunakan Postgres (atau DB yang direkomendasikan PWS) dan atur DATABASE_URL di env; jalankan manage.py migrate pada environment deploy (dri console PWS atau build hook).  pastikan static files di-handle dan media files disimpan di storage yang tersedia. Intinya: deploy = push kode + set env vars + jalankan migrate + verifikasi logs + test akses publik.



2. Buatlah bagan yang berisi request client ke web aplikasi berbasis Django beserta responnya dan jelaskan pada bagan tersebut kaitan antara urls.py, views.py, models.py, dan berkas html.
->  Client (Browser) → URL (urls.py) → View (views.py) → Model (models.py) → Template (HTML) → Response ke Client

urls.py: bertugas memetakan URL yang diminta client ke fungsi tertentu di views.py.

views.py: menjalankan logika bisnis, memproses request, mengambil/mengolah data dari models.py, lalu memilih template untuk ditampilkan.

models.py: berisi representasi data (ORM) yang terhubung ke database. View akan memanggil model ini untuk operasi CRUD.

Template (HTML): menerima data dari view dalam bentuk context, lalu merendernya menjadi halaman web yang siap ditampilkan.

Response: hasil akhir (halaman HTML) dikembalikan ke browser.

3. Jelaskan peran settings.py dalam proyek Django!
Bagaimana cara kerja migrasi database di Django?
-> Peran settings.py berfungsi sebagai pusat konfigurasi proyek django. Di dalamnya terdapat pengaturan database, daftar aplikasi (INSTALLED_APPS), konfigurasi middleware, template, static files, serta variabel lingkungan lainnya. Dengan adanya settings.py, kita bisa mengatur bagaimana seluruh komponen Django beroperasi dalam satu proyek. Cara kerja migrasi database di Django
Proses migrasi dilakukan dalam dua tahap:

makemigrations: membaca perubahan pada models.py dan membuat file migrasi (semacam blueprint skema database).

migrate: menerapkan blueprint tersebut ke database sehingga struktur tabel benar-benar dibuat atau diperbarui.

Alasan keduanya dipisahkan adalah agar developer bisa meninjau dulu perubahan skema sebelum diterapkan. Jika hanya menjalankan makemigrations tanpa migrate, perubahan hanya tercatat di file migrasi tapi tidak dieksekusi ke database

4. Menurut Anda, dari semua framework yang ada, mengapa framework Django dijadikan permulaan pembelajaran pengembangan perangkat lunak?
-> Django dijadikan framework pertama dalam pembelajaran karena memiliki arsitektur MTV (Model–Template–View) yang jelas memisahkan data, logika, dan tampilan sehingga mahasiswa lebih mudah memahami prinsip separation of concern. Selain itu, Django sudah menyediakan banyak fitur bawaan seperti ORM, admin panel, dan autentikasi sehingga pemula dapat langsung membangun aplikasi nyata tanpa harus menyiapkan semuanya dari awal. Ditambah lagi, Django berbasis Python yang relatif mudah dipelajari dan sudah dikenal sebelumnya, serta populer di industri sehingga relevan untuk mahasiswa

5. Apakah ada feedback untuk asisten dosen tutorial 1 yang telah kamu kerjakan sebelumnya?
-> Tutorial 1 sudah cukup membantu memahami alur kerja MTV di Django dan pembuatan tuugas secara keseluruhan.