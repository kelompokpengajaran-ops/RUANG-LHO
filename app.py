import os, sqlite3, uuid
from pathlib import Path
from datetime import datetime
import requests
import streamlit as st

st.set_page_config(page_title="Ruang LHO", page_icon="📘", layout="wide")

SCHOOL = "SMA PAB 4 Sampali"
YEAR = "2026/2027"
AUTHORS = [
    "Atika Sania Samni Nst", "Wilda Lestari Harahap",
    "Siti Fadillah Hasibuan", "Dea Saputri", "Lawri Aulia Hasibuan",
    "Mela E. Ambarita", "Wanti Br Hombing"
]
TOPICS = [
    "Pengertian Teks Laporan Hasil Observasi",
    "Tujuan Teks Laporan Hasil Observasi",
    "Ciri-ciri Teks Laporan Hasil Observasi",
    "Struktur Teks Laporan Hasil Observasi",
    "Kaidah Kebahasaan Teks Laporan Hasil Observasi",
    "Contoh Teks Laporan Hasil Observasi",
    "Langkah-langkah Menyusun Teks Laporan Hasil Observasi",
    "Penyajian dan Presentasi Hasil Observasi",
]
VIDEO_URL = "https://www.youtube.com/results?search_query=teks+laporan+hasil+observasi+kelas+X+struktur+kaidah+kebahasaan"

MATERIALS = {
TOPICS[0]: """Teks Laporan Hasil Observasi (LHO) menyampaikan informasi tentang suatu objek berdasarkan pengamatan yang sistematis. Objek dapat berupa makhluk hidup, benda, tempat, lingkungan, atau fenomena. Informasinya harus berdasarkan fakta, bukan imajinasi atau pendapat pribadi.""",
TOPICS[1]: """Tujuan teks LHO adalah memberikan informasi faktual dan objektif tentang objek atau fenomena. Laporan membantu pembaca mengenali, memahami, dan mengelompokkan objek berdasarkan ciri-cirinya. Kegiatan ini juga melatih keterampilan mengamati, mencatat data, dan menyampaikan temuan dengan jelas.""",
TOPICS[2]: """Ciri-ciri teks LHO: (1) berdasarkan fakta/data pengamatan; (2) objektif; (3) membahas objek secara umum lalu bagian-bagiannya; (4) sistematis dan runtut; (5) menggunakan bahasa baku dan informatif; (6) dapat mengelompokkan objek berdasarkan ciri-cirinya.""",
TOPICS[3]: """Struktur umum teks LHO:
1. Pernyataan umum/klasifikasi: mengenalkan objek dan menjelaskan definisi atau kelompoknya.
2. Deskripsi bagian: merinci ciri, bagian, sifat, perilaku, atau kondisi objek berdasarkan pengamatan.
3. Deskripsi manfaat atau simpulan (bila diperlukan): menjelaskan manfaat atau merangkum temuan utama.
Sesuaikan istilah struktur dengan buku ajar dan arahan guru yang digunakan di sekolah.""",
TOPICS[4]: """Kaidah kebahasaan yang sering digunakan: kata benda (tanaman, perpustakaan); kata kerja relasional (adalah, merupakan, termasuk); kata kerja material (tumbuh, bergerak, menghasilkan); istilah teknis; kalimat definisi dan deskripsi; serta kata sifat yang dapat dibuktikan melalui pengamatan. Hindari klaim berlebihan tanpa data.""",
TOPICS[5]: """Contoh singkat: Tanaman Lidah Buaya

Pernyataan umum: Lidah buaya merupakan tanaman sukulen yang dapat menyimpan air pada daunnya dan dapat ditanam di pekarangan.

Deskripsi bagian: Daunnya tebal, memanjang, berwarna hijau, dan memiliki tepi bergerigi. Bagian dalam daun mengandung gel. Tanaman membutuhkan cahaya matahari dan air untuk tumbuh.

Deskripsi manfaat: Lidah buaya dimanfaatkan dalam produk perawatan dan sebagai tanaman hias. Untuk tugas sendiri, gunakan fakta dari pengamatan nyata.""",
TOPICS[6]: """Langkah menyusun teks LHO: 1) menentukan objek yang aman untuk diamati; 2) menentukan tujuan dan aspek pengamatan; 3) mengamati dengan teliti; 4) mencatat fakta; 5) mengelompokkan data; 6) membuat kerangka; 7) mengembangkan kerangka menjadi paragraf; 8) memeriksa fakta, ejaan, tanda baca, dan pilihan kata; 9) merevisi berdasarkan masukan.""",
TOPICS[7]: """Hasil observasi dapat disajikan sebagai laporan tertulis, poster, infografik, atau presentasi lisan. Saat presentasi, sampaikan objek dan tujuan, cara pengamatan, temuan utama, lalu simpulan. Gunakan foto, tabel, atau diagram bila membantu. Jawab pertanyaan berdasarkan data dan bedakan fakta dari dugaan."""
}
CP_TEXT = (" peserta didik memahami, mengolah, dan menyampaikan informasi dari berbagai jenis teks; "
           "menggunakan Bahasa Indonesia secara logis, kritis, dan kreatif; serta menyajikan gagasan dan hasil pengamatan "
           "secara runtut sesuai konteks.")
ATP = [
"Menjelaskan pengertian dan tujuan teks LHO berdasarkan contoh.",
"Mengidentifikasi ciri-ciri dan struktur teks LHO.",
"Menganalisis kaidah kebahasaan teks LHO.",
"Menemukan informasi faktual dalam contoh teks LHO.",
"Menyusun teks LHO berdasarkan hasil pengamatan nyata.",
"Menyunting teks berdasarkan struktur, fakta, dan kaidah bahasa.",
"Menyajikan hasil observasi secara lisan atau visual dengan runtut."
]

ROOT = Path(__file__).parent
DATA = ROOT / "data"
UPLOADS = DATA / "tugas"
LKPD_DIR = ROOT / "lkpd_files"  # Tambahan: lokasi lembar jawaban Word LKPD
DATA.mkdir(exist_ok=True)
UPLOADS.mkdir(exist_ok=True)
LKPD_DIR.mkdir(exist_ok=True)
DB = DATA / "ruang_lho.db"

def secret(name, default=""):
    try:
        return str(st.secrets.get(name, default))
    except Exception:
        return os.getenv(name, default)

def db():
    c = sqlite3.connect(DB, check_same_thread=False)
    c.row_factory = sqlite3.Row
    return c

def init_db():
    with db() as c:
        c.execute("""CREATE TABLE IF NOT EXISTS tasks(
        id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, class_name TEXT DEFAULT '',
        title TEXT NOT NULL, answer TEXT DEFAULT '', file_name TEXT DEFAULT '', stored_file TEXT DEFAULT '',
        submitted TEXT NOT NULL, feedback TEXT DEFAULT '', score TEXT DEFAULT '', reviewed TEXT DEFAULT '')""")
        c.execute("""CREATE TABLE IF NOT EXISTS quizzes(
        id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, score INTEGER, total INTEGER, submitted TEXT)""")
        c.commit()
init_db()

def task_rows(name=None):
    with db() as c:
        if name:
            return c.execute("SELECT * FROM tasks WHERE lower(name)=lower(?) ORDER BY id DESC",(name.strip(),)).fetchall()
        return c.execute("SELECT * FROM tasks ORDER BY id DESC").fetchall()

def submit_task(name, klass, title, answer, upload):
    fname, stored = "", ""
    if upload:
        fname = Path(upload.name).name
        stored = uuid.uuid4().hex + "_" + fname.replace(" ", "_")
        (UPLOADS / stored).write_bytes(upload.getbuffer())
    with db() as c:
        c.execute("""INSERT INTO tasks(name,class_name,title,answer,file_name,stored_file,submitted)
        VALUES(?,?,?,?,?,?,?)""",(name.strip(),klass.strip(),title,answer.strip(),fname,stored,datetime.now().strftime("%Y-%m-%d %H:%M")))
        c.commit()

def save_review(task_id, score, feedback):
    with db() as c:
        c.execute("UPDATE tasks SET score=?,feedback=?,reviewed=? WHERE id=?",
                  (score.strip(),feedback.strip(),datetime.now().strftime("%Y-%m-%d %H:%M"),task_id))
        c.commit()

def ask_ai(history, prompt):
    key = secret("GEMINI_API_KEY").strip()
    if not key:
        return None, "GEMINI_API_KEY belum diatur di Streamlit Cloud → Settings → Secrets."
    # Model default dapat diganti lewat Secrets; tidak memakai Gemini 2.5 Flash.
    model = secret("GEMINI_MODEL", "gemini-3.5-flash-lite").strip().removeprefix("models/")
    system = ("Kamu adalah Ruang AI, pendamping belajar Bahasa Indonesia untuk siswa SMA. "
              "Bantu siswa memahami teks Laporan Hasil Observasi (LHO) dengan bahasa ramah dan jelas. "
              "Berikan contoh orisinal, dorong siswa berpikir, dan jangan mengarang sumber.")
    contents = []
    for m in history[-10:]:
        txt = m.get("content","").strip()
        if txt:
            contents.append({"role":"model" if m["role"]=="assistant" else "user","parts":[{"text":txt}]})
    contents.append({"role":"user","parts":[{"text":prompt}]})
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    try:
        r = requests.post(url,headers={"Content-Type":"application/json","x-goog-api-key":key},
          json={"systemInstruction":{"parts":[{"text":system}]},"contents":contents,
                "generationConfig":{"temperature":0.6,"maxOutputTokens":1200}},timeout=45)
        if r.status_code != 200:
            try: detail = r.json().get("error",{}).get("message",r.text)
            except Exception: detail = r.text
            if r.status_code == 404:
                return None, f"Model '{model}' tidak tersedia untuk API key ini (404). Periksa daftar model yang didukung key-mu atau ubah GEMINI_MODEL di Secrets. Detail: {detail}"
            if r.status_code in (401,403):
                return None, f"API key ditolak atau tidak punya izin ({r.status_code}). Periksa key Google AI Studio pada Secrets. Detail: {detail}"
            if r.status_code == 429:
                return None, f"Batas penggunaan API tercapai. Coba lagi nanti. Detail: {detail}"
            return None, f"Permintaan AI gagal (HTTP {r.status_code}). Detail: {detail}"
        data = r.json()
        candidates = data.get("candidates",[])
        if not candidates: return None, "AI tidak mengembalikan jawaban. Coba pertanyaan lain."
        answer = "\n".join(p.get("text","") for p in candidates[0].get("content",{}).get("parts",[]) if p.get("text"))
        return (answer,None) if answer else (None,"Respons AI kosong.")
    except requests.Timeout:
        return None,"Permintaan ke AI terlalu lama. Coba lagi."
    except requests.RequestException as e:
        return None,f"Tidak dapat menghubungi layanan AI: {e}"

st.markdown("""<style>.main .block-container{max-width:1150px;padding-top:1.5rem}
.hero{padding:1.5rem;border-radius:16px;background:linear-gradient(120deg,#153b65,#277e91);color:white}
.hero h1{color:white}</style>""",unsafe_allow_html=True)

for k,v in {"role":"","student_name":"","student_class":"","chat":[]}.items():
    if k not in st.session_state: st.session_state[k]=v

with st.sidebar:
    st.markdown("## 📘 Ruang LHO")
    st.caption("Media Pembelajaran Bahasa Indonesia")
    if st.session_state.role:
        st.success("Masuk sebagai "+("Guru" if st.session_state.role=="guru" else "Siswa"))
        if st.session_state.role=="siswa": st.caption(st.session_state.student_name)
        if st.button("Keluar",use_container_width=True):
            for k in ["role","student_name","student_class","chat","page"]: st.session_state.pop(k,None)
            st.rerun()
    st.divider()

if not st.session_state.role:
    st.markdown(f'<div class="hero"><h1>📘 Ruang LHO</h1><p>Media Pembelajaran Teks Laporan Hasil Observasi</p><b>{SCHOOL} · {YEAR}</b></div>',unsafe_allow_html=True)
    tab1,tab2=st.tabs(["👩‍🎓 Masuk Siswa","👩‍🏫 Masuk Guru"])
    with tab1:
        with st.form("login_siswa"):
            nm=st.text_input("Nama lengkap siswa"); cl=st.text_input("Kelas")
            ok=st.form_submit_button("Masuk sebagai Siswa")
        if ok:
            if not nm.strip(): st.warning("Nama lengkap perlu diisi.")
            else:
                st.session_state.role="siswa"; st.session_state.student_name=nm.strip()
                st.session_state.student_class=cl.strip(); st.session_state.page="Beranda"; st.rerun()
    with tab2:
        with st.form("login_guru"):
            pin=st.text_input("PIN guru",type="password"); okg=st.form_submit_button("Masuk sebagai Guru")
        if okg:
            if pin==secret("TEACHER_PIN","1234"):
                st.session_state.role="guru"; st.session_state.page="Ruang Guru"; st.rerun()
            else: st.error("PIN guru salah.")
        st.caption("Ubah PIN default melalui TEACHER_PIN di Streamlit Secrets.")
    st.stop()

if st.session_state.role=="siswa":
    menu=["Beranda","Komponen Inti (Identitas Modul)","Materi LHO","LKPD","Kuis","Kumpulkan Tugas","Umpan Balik Guru","Tanya AI"]
else:
    menu=["Beranda","Komponen Inti (Identitas Modul)","Materi LHO","LKPD","Kuis","Kumpulkan Tugas","Ruang Guru","Tanya AI"]
with st.sidebar: st.radio("Menu",menu,key="page")
page=st.session_state.page

if page=="Beranda":
    st.markdown(f'<div class="hero"><h1>📘 Ruang LHO</h1><p>Media Pembelajaran Teks Laporan Hasil Observasi</p><b>{SCHOOL} · Tahun Ajaran {YEAR}</b></div>',unsafe_allow_html=True)
    st.write("Pelajari konsep LHO, analisis contoh, susun laporan dari pengamatan nyata, lalu sajikan temuan secara runtut.")
    a,b,c=st.columns(3); a.metric("Topik materi","8"); b.metric("Latihan","LKPD + Kuis"); c.metric("Tahun ajaran",YEAR)
    st.subheader("Alur belajar")
    st.markdown("1. Pelajari delapan topik materi.\n2. Kerjakan LKPD dan kuis.\n3. Kumpulkan tugas.\n4. Periksa komentar guru pada menu Umpan Balik Guru.")
    st.subheader("Video pendukung"); st.link_button("▶ Cari video pembelajaran teks LHO di YouTube",VIDEO_URL)
    with st.expander("Tim penyusun"):
        for x in AUTHORS: st.write("• "+x)

elif page=="Komponen Inti (Identitas Modul)":
    st.title("Komponen Inti (Identitas Modul)")
    st.subheader("A. Identitas Modul")
    for k,v in [("Satuan pendidikan",SCHOOL),("Mata pelajaran","Bahasa Indonesia"),("Materi pokok","Teks Laporan Hasil Observasi"),("Fase/Kelas","Fase E / Kelas X (sesuaikan dengan sasaran sekolah)"),("Tahun ajaran",YEAR),("Alokasi waktu","Disesuaikan dengan jadwal guru"),("Penyusun",", ".join(AUTHORS))]:
        st.markdown(f"**{k}:** {v}")
    st.subheader("B. Capaian Pembelajaran (ringkasan kerja)"); st.write(CP_TEXT)
    st.warning("Ini ringkasan kerja, bukan kutipan verbatim CP resmi. Guru perlu mencocokkan dengan dokumen CP yang berlaku di sekolah.")
    st.markdown("[Rujukan CP Bahasa Indonesia Fase E](https://guru.kemendikdasmen.go.id/kurikulum/referensi-penerapan/capaian-pembelajaran/sd-sma/bahasa-indonesia/fase-e/)")
    st.subheader("C. Tujuan Pembelajaran")
    for x in ["Menjelaskan pengertian dan tujuan teks LHO.","Mengidentifikasi ciri-ciri dan struktur teks LHO.","Menganalisis kaidah kebahasaan teks LHO.","Menemukan informasi faktual dalam contoh teks LHO.","Menyusun dan menyunting teks LHO berdasarkan observasi nyata.","Menyajikan hasil observasi secara runtut."]: st.write("• "+x)
    st.subheader("D. Alur Tujuan Pembelajaran (ATP)")
    for i,x in enumerate(ATP,1): st.write(f"{i}. {x}")
    st.subheader("E. Asesmen"); st.write("Asesmen awal melalui tanya jawab; formatif melalui analisis contoh dan LKPD; asesmen akhir melalui teks LHO dan presentasi. Kriteria meliputi ketepatan fakta, struktur, bahasa, keruntutan, dan penyajian.")

elif page=="Materi LHO":
    st.title("Materi Teks Laporan Hasil Observasi")
    for i,t in enumerate(TOPICS,1):
        with st.expander(f"{i}. {t}",expanded=(i==1)): st.markdown(MATERIALS[t])
    st.subheader("Video pendukung"); st.link_button("▶ Cari video pembelajaran di YouTube",VIDEO_URL)

elif page=="LKPD":
    st.title("LKPD — Lembar Kerja Peserta Didik")
    st.write("Pilih salah satu LKPD. Baca petunjuk dan soal di halaman ini, lalu unduh lembar jawaban Word. Setelah selesai, unggah dokumen melalui menu **Kumpulkan Tugas**.")

    lkpd_options = {
        "LKPD 1 — Observasi Objek": {
            "file": "LKPD_1_Observasi_Objek.docx",
            "objective": "Mengidentifikasi objek dan mengumpulkan fakta berdasarkan pengamatan langsung.",
            "instructions": [
                "Pilih satu objek yang aman untuk diamati di lingkungan sekolah atau rumah.",
                "Amati objek dengan teliti dan catat fakta yang benar-benar terlihat.",
                "Isi semua bagian berdasarkan hasil pengamatan, bukan dugaan."
            ],
            "questions": [
                "Tuliskan objek yang kamu amati dan tujuan pengamatan.",
                "Catat sekurang-kurangnya lima fakta yang kamu temukan.",
                "Kelompokkan temuan menjadi pernyataan umum dan deskripsi bagian.",
                "Tuliskan simpulan berdasarkan fakta hasil pengamatan."
            ],
            "task": "LKPD 1 — Observasi Objek"
        },
        "LKPD 2 — Menulis Teks LHO": {
            "file": "LKPD_2_Menulis_Teks_LHO.docx",
            "objective": "Menyusun teks LHO yang faktual, objektif, sistematis, dan menggunakan bahasa baku.",
            "instructions": [
                "Gunakan fakta dari hasil pengamatan nyata, termasuk catatan LKPD 1 jika relevan.",
                "Buat kerangka berdasarkan struktur teks LHO.",
                "Kembangkan kerangka menjadi laporan yang runtut dan periksa kembali ejaan."
            ],
            "questions": [
                "Tuliskan objek yang dilaporkan, tujuan, dan fakta utama.",
                "Buat kerangka pernyataan umum/klasifikasi.",
                "Kembangkan deskripsi bagian berdasarkan fakta pengamatan.",
                "Tambahkan deskripsi manfaat atau simpulan jika diperlukan.",
                "Tuliskan teks LHO lengkap dengan bahasa baku dan runtut."
            ],
            "task": "LKPD 2 — Menulis Teks LHO"
        },
        "LKPD 3 — Analisis Struktur dan Kaidah Kebahasaan": {
            "file": "LKPD_3_Analisis_Struktur_Kaidah.docx",
            "objective": "Menganalisis struktur dan unsur kebahasaan dalam contoh teks LHO.",
            "instructions": [
                "Bacalah teks contoh berikut dengan saksama.",
                "Jawab pertanyaan menggunakan bukti berupa kata atau kalimat dari teks.",
                "Gunakan istilah kebahasaan yang tepat dan jelaskan alasanmu."
            ],
            "sample": "Tanaman Lidah Buaya. Lidah buaya merupakan tanaman sukulen yang dapat menyimpan air pada daunnya dan dapat ditanam di pekarangan. Daunnya tebal, memanjang, berwarna hijau, dan memiliki tepi bergerigi. Bagian dalam daun mengandung gel. Tanaman membutuhkan cahaya matahari dan air untuk tumbuh. Lidah buaya dimanfaatkan dalam produk perawatan dan sebagai tanaman hias.",
            "questions": [
                "Tentukan bagian pernyataan umum/klasifikasi dalam teks dan jelaskan alasanmu.",
                "Tentukan bagian deskripsi bagian dalam teks.",
                "Tuliskan bagian deskripsi manfaat/simpulan jika ada.",
                "Temukan contoh kata benda, kata kerja relasional, kata kerja material, kata sifat, dan istilah khusus.",
                "Tuliskan dua fakta dari teks dan jelaskan mengapa teks tersebut termasuk LHO."
            ],
            "task": "LKPD 3 — Analisis Struktur dan Kaidah Kebahasaan"
        }
    }

    selected_lkpd = st.selectbox("Pilih jenis LKPD", list(lkpd_options.keys()))
    lkpd = lkpd_options[selected_lkpd]
    st.subheader("Tujuan")
    st.write(lkpd["objective"])
    st.subheader("Petunjuk Pengerjaan")
    for i, instruction in enumerate(lkpd["instructions"], 1):
        st.write(f"{i}. {instruction}")
    if lkpd.get("sample"):
        st.subheader("Teks Contoh")
        st.write(lkpd["sample"])
    st.subheader("Soal / Tugas")
    for i, question in enumerate(lkpd["questions"], 1):
        st.write(f"{i}. {question}")
    answer_path = LKPD_DIR / lkpd["file"]
    if answer_path.exists():
        st.download_button(
            "⬇️ Unduh Lembar Jawaban Word (.docx)",
            data=answer_path.read_bytes(),
            file_name=lkpd["file"],
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            key=f"download_{lkpd['file']}"
        )
    else:
        st.error(f"File lembar jawaban tidak ditemukan: {lkpd['file']}. Pastikan folder lkpd_files berada di samping app.py.")
    st.info("Setelah selesai mengisi dokumen Word, buka menu **Kumpulkan Tugas**, pilih jenis LKPD yang sama, lalu unggah dokumen jawabanmu.")

elif page=="Kuis":
    st.title("Kuis Teks Laporan Hasil Observasi")
    qs=[
    ("Teks LHO terutama berdasarkan …",["Imajinasi","Fakta hasil pengamatan","Konflik tokoh","Pendapat tanpa bukti"],1),
    ("Bagian yang mengenalkan objek secara umum disebut …",["Orientasi","Komplikasi","Pernyataan umum/klasifikasi","Resolusi"],2),
    ("Sikap yang perlu dijaga dalam LHO adalah …",["Objektif","Berlebihan","Memihak","Penuh dugaan"],0),
    ("Kata “merupakan” termasuk …",["Kata seru","Kata kerja relasional","Kata ganti","Kata sandang"],1),
    ("Langkah awal menyusun LHO adalah …",["Presentasi","Menentukan objek","Menyunting","Mencetak"],1),
    ("Bagian teks LHO yang menjelaskan ciri atau bagian objek disebut …",["Deskripsi bagian","Orientasi","Komplikasi","Resolusi"],0),
    ("Informasi dalam teks LHO sebaiknya bersifat …",["Rekaan","Objektif dan faktual","Rahasia","Persuasif semata"],1),
    ("Kata “tumbuh” pada laporan tanaman termasuk …",["Kata kerja material","Kata seru","Kata ganti","Kata sandang"],0),
    ("Manakah contoh fakta yang dapat diamati?",["Tanaman itu paling indah","Daunnya berwarna hijau","Semua orang menyukainya","Tanaman itu pasti ajaib"],1),
    ("Sebelum menulis teks LHO, pengamat sebaiknya …",["Mengarang hasil","Menentukan objek dan mencatat data","Menyalin pendapat teman","Membuat simpulan tanpa data"],1)]
    with st.form("quiz_form"):
        answers=[st.radio(f"{i}. {q}",opts,index=None,key=f"q_{i}") for i,(q,opts,correct) in enumerate(qs,1)]
        submitted=st.form_submit_button("Periksa Jawaban")
    if submitted:
        if any(x is None for x in answers): st.warning("Jawab semua soal terlebih dahulu.")
        else:
            score=sum(x==q[1][q[2]] for x,q in zip(answers,qs))
            st.success(f"Nilai: {score}/{len(qs)} ({round(score/len(qs)*100)}%)")
            with db() as c:
                c.execute("INSERT INTO quizzes(name,score,total,submitted) VALUES(?,?,?,?)",(st.session_state.student_name or "Guru",score,len(qs),datetime.now().strftime("%Y-%m-%d %H:%M"))); c.commit()
            with st.expander("Pembahasan"):
                for i,(q,opts,correct) in enumerate(qs,1): st.write(f"{i}. Jawaban: **{opts[correct]}**")

elif page=="Kumpulkan Tugas":
    st.title("Kumpulkan Tugas")
    with st.form("task_form",clear_on_submit=True):
        name=st.text_input("Nama siswa",value=st.session_state.student_name if st.session_state.role=="siswa" else "")
        klass=st.text_input("Kelas",value=st.session_state.student_class if st.session_state.role=="siswa" else "")
        title=st.selectbox("Jenis tugas",["LKPD 1 — Observasi Objek","LKPD 2 — Menulis Teks LHO","LKPD 3 — Analisis Struktur dan Kaidah Kebahasaan","LKPD: Observasi objek","Menulis teks LHO","Analisis struktur dan kaidah kebahasaan","Presentasi hasil observasi"])
        answer=st.text_area("Jawaban/catatan untuk guru",height=160)
        upload=st.file_uploader("Unggah berkas (opsional)",type=["pdf","doc","docx","txt","jpg","jpeg","png","ppt","pptx"])
        send=st.form_submit_button("Kirim Tugas")
    if send:
        if not name.strip(): st.error("Nama siswa wajib diisi.")
        elif not answer.strip() and upload is None: st.error("Isi jawaban atau unggah berkas.")
        else:
            submit_task(name,klass,title,answer,upload)
            st.success("Tugas tercatat. Periksa menu Umpan Balik Guru setelah guru menilainya.")

elif page=="Umpan Balik Guru":
    st.title("Umpan Balik Guru"); st.write(f"Umpan balik untuk **{st.session_state.student_name}**")
    rows=task_rows(st.session_state.student_name)
    if not rows: st.info("Belum ada tugas atas nama ini. Pastikan nama saat mengumpulkan sama dengan nama login.")
    for r in rows:
        with st.expander(f"{r['title']} · {r['submitted']}"):
            st.write("**Jawaban:**"); st.write(r["answer"] or "Tidak ada jawaban tertulis.")
            if r["file_name"]: st.write("Berkas:",r["file_name"])
            st.write("**Nilai:**",r["score"] or "Belum dinilai")
            st.write("**Komentar guru:**",r["feedback"] or "Belum ada umpan balik")
            if r["reviewed"]: st.caption("Diperiksa: "+r["reviewed"])

elif page=="Ruang Guru":
    if st.session_state.role!="guru": st.error("Menu ini hanya untuk guru."); st.stop()
    st.title("Ruang Guru — Pemeriksaan Tugas"); rows=task_rows(); st.metric("Tugas masuk",len(rows))
    if not rows: st.info("Belum ada tugas masuk.")
    for r in rows:
        with st.expander(f"{r['name']} ({r['class_name'] or 'kelas belum diisi'}) · {r['title']} · {r['submitted']}"):
            st.write("**Jawaban siswa:**"); st.write(r["answer"] or "Tidak ada jawaban tertulis.")
            if r["file_name"]:
                p=UPLOADS/r["stored_file"]
                if p.exists(): st.download_button("Unduh berkas",p.read_bytes(),file_name=r["file_name"],key=f"dl_{r['id']}")
                else: st.warning("Berkas tidak tersedia pada penyimpanan lokal.")
            with st.form(f"review_{r['id']}"):
                score=st.text_input("Nilai",value=r["score"] or "")
                feedback=st.text_area("Komentar/umpan balik",value=r["feedback"] or "",height=120)
                save=st.form_submit_button("Simpan Umpan Balik")
            if save:
                save_review(r["id"],score,feedback); st.success("Umpan balik tersimpan."); st.rerun()
    st.subheader("Hasil kuis")
    with db() as c: qr=c.execute("SELECT * FROM quizzes ORDER BY id DESC").fetchall()
    if qr: st.dataframe([{"Nama":r["name"],"Skor":f"{r['score']}/{r['total']}","Waktu":r["submitted"]} for r in qr],use_container_width=True,hide_index=True)
    else: st.info("Belum ada hasil kuis.")

elif page=="Tanya AI":
    st.title("Tanya AI — Teman Belajar Teks LHO")
    st.caption("Model bawaan: Gemini 3.8 Flash. Model dapat diubah melalui GEMINI_MODEL pada Streamlit Secrets.")
    if st.button("Hapus riwayat percakapan"): st.session_state.chat=[]; st.rerun()
    for m in st.session_state.chat:
        with st.chat_message(m["role"]): st.markdown(m["content"])
    prompt=st.chat_input("Tulis pertanyaan tentang teks LHO…")
    if prompt:
        with st.chat_message("user"): st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Ruang AI sedang menjawab…"):
                answer,error=ask_ai(st.session_state.chat,prompt)
                if error: st.error(error)
                else:
                    st.markdown(answer)
                    st.session_state.chat.extend([{"role":"user","content":prompt},{"role":"assistant","content":answer}])

st.divider()
st.caption(f"Ruang LHO · {SCHOOL} · Tahun Ajaran {YEAR}")
