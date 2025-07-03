from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Konfigurasi database
engine = create_engine("sqlite:///belanja.db", echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Model tabel
class Belanja(Base):
    __tablename__ = 'belanja'
    
    id = Column(Integer, primary_key=True)
    nama_barang = Column(String)
    jumlah = Column(Integer)

# Buat tabel (jika belum ada)
Base.metadata.create_all(engine)

# Fungsi CRUD
def tambah_barang():
    print("Masukkan barang, Ketik 'selesai' untuk berhenti.\n")
    while True:
        nama = input("Nama barang: ")
        if nama.lower() == "selesai":
            break
        try:
            jumlah = int(input("Jumlah: "))
            barang = Belanja(nama_barang=nama, jumlah=jumlah)
            session.add(barang)
            session.commit()
            print("Barang berhasil ditambahkan!\n")
        except ValueError:
            print("Jumlah harus angka. Coba lagi.\n")

def tampilkan_daftar():
    daftar = session.query(Belanja).all()
    if not daftar:
        print("Daftar belanja kosong.\n")
    else:
        print("\nDaftar Belanja:")
        for i, b in enumerate(daftar, start=1):
            print(f"{i}. {b.nama_barang} - {b.jumlah} (ID: {b.id})")
        print()

def ubah_jumlah():
    tampilkan_daftar()
    print("Ubah jumlah barang. Ketik 'selesai' untuk berhenti.\n")
    while True:
        id_input = input("ID barang yang ingin diubah: ")
        if id_input.lower() == "selesai":
            break
        if not id_input.isdigit():
            print("ID harus berupa angka.")
            continue

        id_barang = int(id_input)
        barang = session.query(Belanja).filter_by(id=id_barang).first()
        if barang:
            try:
                jumlah_baru = int(input(f"Jumlah baru untuk '{barang.nama_barang}': "))
                barang.jumlah = jumlah_baru
                session.commit()
                print("Jumlah barang berhasil diubah!\n")
            except ValueError:
                print("Jumlah harus angka.\n")
        else:
            print("Barang dengan ID tersebut tidak ditemukan.\n")


def hapus_barang():
    tampilkan_daftar()
    print("Masukkan ID barang yang ingin dihapus (pisahkan dengan koma)")
    id_input = input("ID barang yang ingin dihapus: ")

    try:
        id_list = [int(id.strip()) for id in id_input.split(",") if id.strip().isdigit()]
        if not id_list:
            print("Tidak ada ID yang valid.\n")
            return

        for id_barang in id_list:
            barang = session.query(Belanja).filter_by(id=id_barang).first()
            if barang:
                session.delete(barang)
        session.commit()
        print("Barang berhasil dihapus!\n")
    except Exception as e:
        print("Terjadi kesalahan:", e)

# Menu Utama
while True:
    print("====== Catatan Belanja ======")
    print("1. Tambah Barang")
    print("2. Tampilkan Daftar")
    print("3. Ubah Jumlah Barang")
    print("4. Hapus Barang")
    print("5. Keluar")
    
    pilihan = input("Pilih menu (1-5): ")
    
    if pilihan == "1":
        tambah_barang()
    elif pilihan == "2":
        tampilkan_daftar()
    elif pilihan == "3":
        ubah_jumlah()
    elif pilihan == "4":
        hapus_barang()
    elif pilihan == "5":
        print("Terima kasih, sampai jumpa!")
        break
    else:
        print("Pilihan tidak valid.\n")
