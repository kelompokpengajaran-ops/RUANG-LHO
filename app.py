import streamlit as st
import sqlite3, os, json
from pathlib import Path
from datetime import datetime

APP_DIR = Path(__file__).parent
DATA_DIR = APP_DIR / "data"
UPLOAD_DIR = DATA_DIR / "tugas_siswa"
DATA_DIR.mkdir(exist_ok=True)
UPLOAD_DIR.mkdir(exist_ok=True)
DB_PATH = DATA_DIR / "ruanglho.db"

st.set_page_config(page_title="Ruang LHO | Bahasa Indonesia X", page_icon="📘", layout="wide")
st.markdown("""
<style>
.block-container{padding-top:1.6rem;max-width:1200px}
.hero{background:linear-gradient(120deg,#172b4d,#315efb);padding:2rem 2.2rem;border-radius:20px;color:white;margin-bottom:1.2rem}
.hero h1{color:white;font-size:2.35rem;margin-bottom:.4rem}.hero p{color:#e0e8ff;font-size:1.05rem}
div[data-testid="stMetric"]{background:#f4f7ff;border:1px solid #e1e8ff;padding:14px;border-radius:14px}
</style>
""", unsafe_allow_html=True)


def connect():
    con = sqlite3.connect(DB_PATH, check_same_thread=False)
    con.row_factory = sqlite3.Row
    return con


def init_db():
    with connect() as con:
        con.execute('''CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT, student_name TEXT NOT NULL,
            class_name TEXT NOT NULL, task_title TEXT NOT NULL, note TEXT,
            file_name TEXT NOT NULL, saved_path TEXT NOT NULL, submitted_at TEXT NOT NULL,
            score INTEGER, feedback TEXT, reviewed_at TEXT)''')
init_db()

st.sidebar.title("📘 Ruang LHO")
st.sidebar.caption("Bahasa Indonesia • Kelas X")
page = st.sidebar.radio("Menu", ["Beranda", "Komponen Inti (Identitas Modul)", "Materi LHO", "LKPD", "Kuis", "Kumpulkan Tugas", "Ruang Guru", "Tanya AI"])
st.sidebar.divider()
st.sidebar.info("Versi aplikasi lokal. Data tugas tersimpan di folder aplikasi pada laptop yang menjalankannya.")

if page == "Beranda":
    st.markdown("<div class='hero'><h1>Selamat Datang di Ruang LHO</h1><p>Ruang belajar Bahasa Indonesia kelas X untuk memahami, menganalisis, dan menyusun teks Laporan Hasil Observasi.</p></div>", unsafe_allow_html=True)
    a,b,c = st.columns(3)
    a.metric("Topik utama", "Teks LHO")
    b.metric("Fitur belajar", "Materi & Kuis")
    c.metric("Tugas", "Unggah & Umpan Balik")
    st.subheader("Mulai belajar")
    cols = st.columns(3)
    with cols[0]:
        st.markdown("### 📖 Materi")
        st.write("Pelajari pengertian, tujuan, ciri, struktur, kaidah kebahasaan, dan langkah menyusun teks LHO.")
    with cols[1]:
        st.markdown("### ✍️ Kuis")
        st.write("Uji pemahamanmu melalui pertanyaan pilihan ganda dan lihat skor secara langsung.")
    with cols[2]:
        st.markdown("### 📤 Tugas")
        st.write("Kirim hasil tugas untuk diperiksa guru. Guru dapat memberi nilai dan umpan balik di menu Ruang Guru.")
    st.info("Siswa dan guru dapat menggunakan menu yang sesuai. Untuk berbagi lewat internet, aplikasi harus dipublikasikan ke hosting; petunjuknya ada di file MULAI_DI_SINI.txt.")

elif page == "Komponen Inti (Identitas Modul)":
    st.title("Komponen Inti — Identitas Modul")
    st.caption("Modul Ajar Bahasa Indonesia • Fase E / Kelas X")
    st.subheader("A. Identitas Modul")
    st.markdown("""
    | Komponen | Keterangan |
    |---|---|
    | Satuan pendidikan | SMA/MA (sesuaikan dengan satuan pendidikan pengguna) |
    | Mata pelajaran | Bahasa Indonesia |
    | Fase/Kelas | Fase E / Kelas X |
    | Materi pokok | Teks Laporan Hasil Observasi (LHO) |
    | Alokasi waktu | 2 pertemuan (dapat disesuaikan dengan jadwal sekolah) |
    | Penyusun | Guru mata pelajaran (isi nama guru) |
    | Tahun pelajaran | Sesuaikan dengan tahun pelajaran yang berlaku |
    """)
    st.subheader("B. Kompetensi Awal")
    st.write("Peserta didik telah memiliki pengalaman membaca teks informatif dan mampu mengidentifikasi informasi tersurat dalam bacaan sederhana.")
    st.subheader("C. Profil Pelajar Pancasila")
    st.write("Bernalar kritis, mandiri, dan gotong royong melalui kegiatan mengamati objek, memeriksa fakta, berdiskusi, dan menyusun laporan.")
    st.subheader("D. Sarana dan Prasarana")
    st.write("Buku teks, perangkat untuk mengakses Ruang LHO, koneksi internet bila tersedia, objek observasi, dan lembar kerja peserta didik (LKPD).")
    st.subheader("E. Target Peserta Didik")
    st.write("Peserta didik kelas X dengan kebutuhan belajar yang beragam; guru dapat memberikan pendampingan atau pengayaan sesuai hasil asesmen awal.")
    st.subheader("F. Model/Metode Pembelajaran")
    st.write("Pembelajaran berbasis pengamatan dan diskusi, tanya jawab, latihan menganalisis struktur, serta praktik menyusun teks LHO.")
    st.subheader("G. Tujuan Pembelajaran")
    st.markdown("""Setelah pembelajaran, peserta didik mampu:
1. Menjelaskan pengertian, tujuan, dan ciri teks LHO.
2. Mengidentifikasi struktur dan kaidah kebahasaan teks LHO.
3. Membedakan informasi faktual dan opini.
4. Menyusun kerangka dan teks LHO berdasarkan hasil pengamatan secara sistematis.""")
    st.subheader("H. Pemahaman Bermakna")
    st.write("Observasi yang cermat membantu kita menyampaikan informasi faktual tentang objek secara jelas, teratur, dan dapat dipertanggungjawabkan.")
    st.subheader("I. Pertanyaan Pemantik")
    st.markdown("""- Mengapa laporan hasil pengamatan perlu berdasarkan fakta?
- Bagaimana cara membedakan deskripsi objektif dan pendapat pribadi?
- Informasi apa yang perlu dicatat ketika mengamati suatu objek?""")
    st.subheader("J. Asesmen")
    st.write("Asesmen diagnostik melalui tanya jawab, asesmen formatif melalui kuis dan LKPD, serta asesmen produk melalui teks LHO yang dikumpulkan peserta didik.")

elif page == "Materi LHO":
    st.title("Materi Pembelajaran: Teks Laporan Hasil Observasi")
    st.write("Teks laporan hasil observasi (LHO) adalah teks yang menyampaikan informasi tentang suatu objek berdasarkan hasil pengamatan secara sistematis. Objek dapat berupa hewan, tumbuhan, lingkungan, benda, atau fenomena sosial.")
    with st.expander("1. Tujuan dan fungsi teks LHO", expanded=True):
        st.write("Teks LHO bertujuan menyajikan informasi faktual agar pembaca memahami objek yang diamati. Laporan yang baik menyampaikan hasil pengamatan secara jelas, objektif, dan teratur, bukan berdasarkan dugaan atau pendapat pribadi semata.")
    with st.expander("2. Ciri-ciri teks LHO"):
        st.markdown("- Berdasarkan fakta hasil observasi.\n- Membahas objek secara umum sebelum rincian bagian.\n- Disusun secara sistematis dan logis.\n- Menggunakan bahasa baku dan istilah yang sesuai.\n- Informasi dapat diperiksa atau dibuktikan.")
    with st.expander("3. Struktur teks LHO"):
        st.markdown("**Pernyataan umum/klasifikasi:** pengenalan objek dan pengelompokan secara umum.\n\n**Deskripsi bagian:** penjelasan ciri, bagian, sifat, perilaku, atau kondisi objek secara lebih rinci.\n\n**Deskripsi manfaat/simpulan:** informasi tentang fungsi atau manfaat objek, jika relevan dengan objek dan tujuan laporan.")
    with st.expander("4. Kaidah kebahasaan"):
        st.markdown("- **Nomina:** kata benda, misalnya tumbuhan, habitat, ekosistem.\n- **Verba relasional:** kata penghubung definisi/klasifikasi, misalnya adalah, merupakan, termasuk.\n- **Verba material:** kata kerja tindakan, misalnya tumbuh, menghasilkan, bergerak.\n- **Istilah teknis:** kosakata khusus sesuai bidang yang diamati.\n- **Kalimat definisi dan deskripsi:** kalimat yang menjelaskan pengertian atau ciri objek.\n- **Kata baku:** gunakan bentuk kata sesuai kaidah bahasa Indonesia.")
    with st.expander("5. Langkah menyusun teks LHO"):
        st.markdown("1. Tentukan objek yang akan diamati.\n2. Tentukan tujuan dan aspek pengamatan.\n3. Lakukan pengamatan langsung atau gunakan sumber tepercaya.\n4. Catat data faktual dengan rinci.\n5. Kelompokkan data berdasarkan aspek yang sama.\n6. Susun kerangka sesuai struktur teks LHO.\n7. Kembangkan kerangka menjadi paragraf yang padu.\n8. Periksa kembali fakta, struktur, ejaan, dan pilihan kata.")
    with st.expander("6. Contoh teks LHO: Tanaman lidah buaya"):
        st.markdown("**Pernyataan umum**\n\nLidah buaya merupakan tanaman sukulen yang mampu menyimpan air pada daunnya. Tanaman ini banyak tumbuh di daerah beriklim hangat dan dapat dibudidayakan di pekarangan maupun pot.\n\n**Deskripsi bagian**\n\nDaun lidah buaya berbentuk memanjang, tebal, dan memiliki tepi bergerigi. Bagian dalam daunnya mengandung gel bening. Akarnya relatif dangkal, sedangkan daunnya tumbuh berkelompok dari pangkal tanaman.\n\n**Deskripsi manfaat**\n\nLidah buaya dimanfaatkan sebagai tanaman hias dan bahan dalam sejumlah produk perawatan tubuh. Pemanfaatannya perlu memperhatikan jenis produk dan cara pengolahan yang aman.")
    with st.expander("7. Cara membedakan fakta dan opini"):
        st.write("Fakta merupakan informasi yang dapat diperiksa kebenarannya melalui pengamatan atau sumber tepercaya. Opini merupakan pendapat atau penilaian seseorang. Dalam teks LHO, utamakan fakta yang relevan dan hindari penilaian subjektif seperti 'tanaman ini paling cantik' jika tidak disertai kriteria yang jelas.")

elif page == "LKPD":
    st.title("Lembar Kerja Peserta Didik (LKPD) — Teks LHO")
    st.write("LKPD tersedia di menu tersendiri agar siswa mudah menemukan dan mengunduhnya.")
    st.subheader("Petunjuk pengerjaan")
    st.markdown("""1. Unduh LKPD Word di bawah.
2. Baca petunjuk pada setiap bagian.
3. Amati objek yang ditentukan guru atau pilih objek di lingkungan sekitar.
4. Catat fakta hasil pengamatan.
5. Lengkapi analisis struktur dan kaidah kebahasaan, lalu susun teks LHO.
6. Simpan hasil kerja, kemudian unggah melalui menu **Kumpulkan Tugas**.""")
    lkpd_path = APP_DIR / "LKPD_LHO_Kelas_X.docx"
    if lkpd_path.exists():
        st.download_button("📄 Unduh LKPD Teks LHO (Word)", data=lkpd_path.read_bytes(), file_name="LKPD_LHO_Kelas_X.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document", type="primary")
    else:
        st.error("File LKPD tidak ditemukan. Pastikan LKPD_LHO_Kelas_X.docx berada satu folder dengan app.py.")
    st.info("Setelah selesai, unggah file LKPD melalui menu Kumpulkan Tugas. Guru dapat memberikan nilai dan umpan balik melalui menu Ruang Guru.")

elif page == "Kuis":
    st.title("Kuis Pemahaman Teks LHO")
    questions = [
        ("Teks LHO disusun terutama berdasarkan …", ["imajinasi penulis", "fakta hasil pengamatan", "perasaan pembaca", "dialog tokoh"], 1, "Teks LHO menyajikan fakta yang diperoleh dari observasi."),
        ("Bagian yang berisi pengenalan atau klasifikasi umum objek disebut …", ["deskripsi bagian", "orientasi", "pernyataan umum", "resolusi"], 2, "Pernyataan umum mengenalkan dan mengklasifikasikan objek."),
        ("Kata 'merupakan' dalam teks LHO umumnya berfungsi sebagai …", ["verba relasional", "kata seru", "kata ganti", "konjungsi temporal"], 0, "'Merupakan' menghubungkan objek dengan definisi atau klasifikasinya."),
        ("Pernyataan yang paling objektif adalah …", ["Bunga itu paling indah di dunia.", "Menurut saya, pohon itu membosankan.", "Daun mangga berbentuk memanjang dengan ujung meruncing.", "Semua orang pasti menyukai kucing."], 2, "Pernyataan tersebut mendeskripsikan ciri yang dapat diamati."),
        ("Langkah awal menyusun teks LHO adalah …", ["memublikasikan laporan", "menentukan objek pengamatan", "menulis kesimpulan", "mengoreksi ejaan"], 1, "Penulis perlu menentukan objek sebelum melakukan pengamatan."),
        ("Deskripsi bagian berisi …", ["rincian ciri atau bagian objek", "daftar pustaka saja", "pendapat pribadi penulis", "judul laporan saja"], 0, "Deskripsi bagian menguraikan karakteristik objek secara rinci."),
        ("Kosakata khusus seperti 'habitat' disebut …", ["istilah teknis", "kata seru", "kata sandang", "majas"], 0, "Istilah teknis digunakan dalam bidang atau topik tertentu."),
        ("Catatan pengamatan yang baik seharusnya …", ["mengandung dugaan tanpa bukti", "berisi fakta yang relevan dan rinci", "mengutamakan humor", "menghilangkan data penting"], 1, "Catatan perlu akurat, relevan, dan cukup rinci untuk mendukung laporan."),
        ("Kalimat yang menggunakan istilah teknis sesuai topik lingkungan adalah …", ["Sungai itu sangat menyenangkan.", "Ekosistem sungai terdiri atas komponen biotik dan abiotik.", "Saya suka melihat air.", "Pemandangan itu paling bagus."], 1, "Istilah ekosistem, biotik, dan abiotik merupakan kosakata khusus bidang lingkungan."),
        ("Setelah data observasi dikelompokkan, langkah yang tepat berikutnya adalah …", ["Menghapus data yang tidak sesuai pendapat", "Menyusun kerangka berdasarkan struktur LHO", "Menambahkan cerita khayalan", "Menentukan tokoh dan konflik"], 1, "Kerangka membantu menata data ke dalam pernyataan umum, deskripsi bagian, dan bagian akhir yang relevan.")
    ]
    with st.form("quiz_form"):
        student = st.text_input("Nama siswa (opsional)")
        answers=[]
        for i,(q,opts,correct,why) in enumerate(questions):
            st.markdown(f"**{i+1}. {q}**")
            answers.append(st.radio("Pilih jawaban:", opts, key=f"q{i}", index=None, label_visibility="collapsed"))
        submitted = st.form_submit_button("Periksa Jawaban", type="primary")
    if submitted:
        if any(x is None for x in answers):
            st.error("Jawab semua pertanyaan terlebih dahulu.")
        else:
            score=sum(1 for ans,(_,opts,correct,_) in zip(answers,questions) if ans==opts[correct])
            st.success(f"{student or 'Siswa'}, skor kamu: {score}/{len(questions)} ({round(score/len(questions)*100)}%).")
            for i,(q,opts,correct,why) in enumerate(questions):
                is_correct=answers[i]==opts[correct]
                st.write(("✅ Benar. " if is_correct else f"❌ Jawaban benar: **{opts[correct]}**. ")+why)

elif page == "Kumpulkan Tugas":
    st.title("Pengumpulan Tugas Siswa")
    st.write("Isi identitas, pilih tugas, lalu unggah dokumen. Format yang diterima: DOCX, PDF, atau gambar.")
    with st.form("submission_form", clear_on_submit=True):
        name=st.text_input("Nama lengkap", max_chars=100)
        class_name=st.selectbox("Kelas", ["X-A", "X-B", "Kelas lain / belum ditentukan"])
        task=st.selectbox("Jenis tugas", ["LKPD Analisis Teks LHO", "Menulis Teks LHO", "Analisis Struktur dan Kaidah Kebahasaan", "Tugas lainnya"])
        note=st.text_area("Catatan untuk guru (opsional)")
        uploaded=st.file_uploader("Pilih file tugas", type=["docx","pdf","png","jpg","jpeg"])
        ok=st.form_submit_button("Kirim Tugas", type="primary")
    if ok:
        if not name.strip() or uploaded is None:
            st.error("Nama lengkap dan file tugas wajib diisi.")
        else:
            safe_name="".join(ch for ch in name.strip() if ch.isalnum() or ch in "-_ ").strip().replace(" ","_")[:60] or "siswa"
            stamp=datetime.now().strftime("%Y%m%d_%H%M%S")
            saved=UPLOAD_DIR / f"{stamp}_{safe_name}_{Path(uploaded.name).name}"
            saved.write_bytes(uploaded.getbuffer())
            with connect() as con:
                con.execute("INSERT INTO submissions (student_name,class_name,task_title,note,file_name,saved_path,submitted_at) VALUES (?,?,?,?,?,?,?)", (name.strip(),class_name,task,note.strip(),uploaded.name,str(saved),datetime.now().strftime("%d-%m-%Y %H:%M:%S")))
            st.success("Tugas berhasil disimpan. Simpan nama yang kamu gunakan agar mudah menanyakan umpan balik kepada guru.")

elif page == "Ruang Guru":
    st.title("Ruang Guru: Pemeriksaan Tugas")
    st.write("Masukkan PIN guru untuk melihat kiriman, mengunduh file, dan menambahkan nilai serta umpan balik.")
    pin_expected=os.getenv("RUANGLHO_TEACHER_PIN", "1234")
    pin=st.text_input("PIN guru", type="password")
    if pin == pin_expected:
        st.success("Akses guru terbuka.")
        with connect() as con:
            rows=con.execute("SELECT * FROM submissions ORDER BY id DESC").fetchall()
        if not rows:
            st.info("Belum ada tugas yang dikumpulkan.")
        else:
            for row in rows:
                label=f"{row['student_name']} — {row['task_title']} — {row['submitted_at']}"
                with st.expander(label):
                    st.write(f"**Kelas:** {row['class_name']}")
                    st.write(f"**Catatan siswa:** {row['note'] or '-'}")
                    fpath=Path(row['saved_path'])
                    if fpath.exists():
                        st.download_button("Unduh file tugas", data=fpath.read_bytes(), file_name=row['file_name'], key=f"download_{row['id']}")
                    with st.form(f"review_{row['id']}"):
                        score=st.number_input("Nilai (0–100)", min_value=0, max_value=100, value=int(row['score']) if row['score'] is not None else 0, step=1)
                        feedback=st.text_area("Umpan balik guru", value=row['feedback'] or "")
                        save=st.form_submit_button("Simpan umpan balik")
                    if save:
                        with connect() as con:
                            con.execute("UPDATE submissions SET score=?, feedback=?, reviewed_at=? WHERE id=?", (int(score),feedback.strip(),datetime.now().strftime("%d-%m-%Y %H:%M:%S"),row['id']))
                        st.success("Umpan balik tersimpan. Muat ulang halaman bila perlu.")
        st.caption("PIN awal: 1234. Demi keamanan, ubah PIN dengan membuat variabel lingkungan RUANGLHO_TEACHER_PIN sebelum aplikasi dijalankan.")
    elif pin:
        st.error("PIN tidak sesuai.")

elif page == "Tanya AI":
    st.title("Tanya Jawab AI tentang Teks LHO")
    st.write("Ajukan pertanyaan tentang materi LHO. Jawaban AI otomatis menggunakan Gemini jika guru telah mengatur GEMINI_API_KEY pada pengaturan aplikasi. Untuk uji coba lokal, kunci juga dapat dimasukkan sementara di bawah.")
    question=st.text_area("Pertanyaanmu", placeholder="Contoh: Apa perbedaan pernyataan umum dan deskripsi bagian?")
    configured_key = os.getenv("GEMINI_API_KEY", "")
    try:
        configured_key = configured_key or st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        pass
    api_key = configured_key or st.text_input("Gemini API key (opsional untuk uji coba lokal)", type="password", help="Kunci tidak disimpan oleh aplikasi. Jika aplikasi dipublikasikan, lebih aman atur melalui Secrets hosting.")
    if st.button("Kirim pertanyaan", type="primary"):
        if not question.strip():
            st.error("Tuliskan pertanyaan terlebih dahulu.")
        elif api_key.strip():
            try:
                import requests
                url=f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key.strip()}"
                payload={"system_instruction":{"parts":[{"text":"Kamu adalah tutor Bahasa Indonesia kelas X yang membantu siswa memahami teks Laporan Hasil Observasi (LHO). Jawab dalam bahasa Indonesia yang jelas, ramah, dan sesuai tingkat SMA. Berikan penjelasan yang akurat, contoh jika relevan, dan umpan balik pembelajaran yang membangun."}]},"contents":[{"parts":[{"text":question.strip()}]}],"generationConfig":{"temperature":0.5}}
                resp=requests.post(url,json=payload,timeout=45)
                if resp.ok:
                    data=resp.json(); answer=data["candidates"][0]["content"]["parts"][0]["text"]
                    st.session_state["last_ai_question"] = question.strip()
                    st.session_state["last_ai_answer"] = answer
                    st.session_state["last_ai_source"] = "gemini"
                else:
                    st.error(f"Layanan AI memberi respons {resp.status_code}. Periksa kunci API atau koneksi internet.")
            except Exception:
                st.error("Tidak dapat menghubungi layanan AI. Periksa koneksi internet dan kunci API.")
        else:
            q=question.lower()
            if "struktur" in q:
                ans="Struktur teks LHO umumnya meliputi pernyataan umum/klasifikasi, deskripsi bagian, dan deskripsi manfaat atau simpulan bila sesuai. Pernyataan umum mengenalkan objek; deskripsi bagian merinci cirinya; bagian akhir menjelaskan manfaat atau merangkum informasi relevan."
            elif "objektif" in q or "fakta" in q or "opini" in q:
                ans="Informasi objektif didasarkan pada fakta yang dapat diperiksa, bukan penilaian pribadi. Contoh fakta: 'Daun mangga berbentuk memanjang.' Contoh opini: 'Daun mangga sangat cantik.' Dalam teks LHO, utamakan hasil pengamatan yang bisa dibuktikan."
            elif "kaidah" in q or "kebahasaan" in q:
                ans="Kaidah kebahasaan LHO antara lain penggunaan nomina, verba relasional seperti 'adalah' dan 'merupakan', istilah teknis, kalimat definisi, kalimat deskripsi, dan kata baku."
            elif "tujuan" in q or "pengertian" in q or "ciri" in q:
                ans="Teks Laporan Hasil Observasi menyampaikan informasi faktual tentang objek berdasarkan pengamatan sistematis. Tujuannya agar pembaca memahami objek secara jelas dan objektif. Ciri umumnya: faktual, sistematis, informatif, dan menggunakan bahasa baku."
            else:
                ans="Aku bisa membantu menjelaskan pengertian, tujuan, ciri, struktur, kaidah kebahasaan, fakta dan opini, serta langkah menyusun teks LHO. Untuk jawaban generatif yang menanggapi pertanyaan secara khusus, guru perlu mengatur Gemini API key pada aplikasi."
            st.session_state["last_ai_question"] = question.strip()
            st.session_state["last_ai_answer"] = ans
            st.session_state["last_ai_source"] = "panduan"
    if st.session_state.get("last_ai_answer"):
        st.markdown("### Jawaban")
        st.write(st.session_state["last_ai_answer"])
        st.caption("Sumber jawaban: " + ("AI generatif Gemini" if st.session_state.get("last_ai_source") == "gemini" else "panduan materi lokal"))
        st.markdown("**Apakah jawaban ini membantu?**")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("👍 Membantu", key="ai_helpful"):
                st.session_state["ai_feedback"] = "Membantu"
        with c2:
            if st.button("👎 Belum membantu", key="ai_not_helpful"):
                st.session_state["ai_feedback"] = "Belum membantu"
        if st.session_state.get("ai_feedback"):
            st.success("Terima kasih atas umpan balikmu: " + st.session_state["ai_feedback"] + ".")
            extra = st.text_area("Saran atau pertanyaan lanjutan (opsional)", key="ai_feedback_detail")
            if st.button("Kirim umpan balik", key="send_ai_feedback"):
                st.session_state["saved_ai_feedback"] = {"question": st.session_state.get("last_ai_question", ""), "rating": st.session_state["ai_feedback"], "detail": extra.strip(), "time": datetime.now().strftime("%d-%m-%Y %H:%M:%S")}
                st.success("Umpan balik tersimpan untuk sesi ini. Terima kasih!")


