import json
import os
from datetime import datetime

FILE_NAME = "orders.json"

menu = {
    "ori":15000,
    "medium": 30000,
    "large": 45000,
    "party": 80000
}

# Load data
if os.path.exists(FILE_NAME):
    with open(FILE_NAME, "r") as f:
        orders = json.load(f)
else:
    orders = []

def simpan():
    with open(FILE_NAME, "w") as f:
        json.dump(orders, f, indent=2)

def tambah_order():
    nama = input("Nama pembeli: ")
    ukuran = input("Ukuran (ori/medium/large/party): ").lower()

    if ukuran not in menu:
        print("❌ Ukuran tidak valid")
        return

    try:
        jumlah = int(input("Jumlah: "))
    except:
        print("❌ Input harus angka")
        return

    total = menu[ukuran] * jumlah

    order = {
        "nama": nama,
        "ukuran": ukuran,
        "jumlah": jumlah,
        "total": total,
        "waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    orders.append(order)
    simpan()

    print(f"✅ Order masuk | Rp{total}")

def tampilkan_order(filter_tanggal=None):
    hasil = []
    for i, o in enumerate(orders):
        if "waktu" not in o:
            continue

        if filter_tanggal:
            if not o["waktu"].startswith(filter_tanggal):
                continue

        print(f"[{i}] {o['waktu']} | {o['nama']} | {o['ukuran']} x{o['jumlah']} = Rp{o['total']}")
        hasil.append(o)

    return hasil

def laporan():
    today = datetime.now().strftime("%Y-%m-%d")

    print(f"\n=== LAPORAN HARI INI ({today}) ===")
    tampilkan_order(today)

    analisa(today)

def laporan_tanggal():
    tanggal = input("Masukkan tanggal (YYYY-MM-DD): ")
    print(f"\n=== LAPORAN {tanggal} ===")
    tampilkan_order(tanggal)
    analisa(tanggal)

def analisa(tanggal):
    total = 0
    produk = {}
    jam = {}

    for o in orders:
        if "waktu" not in o:
            continue

        if not o["waktu"].startswith(tanggal):
            continue

        total += o["total"]

        # produk
        produk[o["ukuran"]] = produk.get(o["ukuran"], 0) + o["jumlah"]

        # jam
        jam_key = o["waktu"][11:13]
        jam[jam_key] = jam.get(jam_key, 0) + o["jumlah"]

    print("\n=== ANALISA ===")
    print(f"Total omzet: Rp{total}")

    if produk:
        best = max(produk, key=produk.get)
        print(f"Produk terlaris: {best} ({produk[best]} pcs)")

    if jam:
        best_jam = max(jam, key=jam.get)
        print(f"Jam paling rame: {best_jam}:00")

def hapus_order():
    tampilkan_order()

    try:
        index = int(input("\nIndex yang mau dihapus: "))
        deleted = orders.pop(index)
        simpan()
        print(f"🗑️ {deleted['nama']} dihapus")
    except:
        print("❌ Gagal hapus")

def edit_order():
    tampilkan_order()

    try:
        index = int(input("\nIndex yang mau diedit: "))
        o = orders[index]
    except:
        print("❌ Index salah")
        return

    print("Kosongkan jika tidak ingin mengubah")

    nama = input(f"Nama ({o['nama']}): ") or o["nama"]
    ukuran = input(f"Ukuran ({o['ukuran']}): ") or o["ukuran"]

    if ukuran not in menu:
        print("❌ Ukuran tidak valid")
        return

    jumlah_input = input(f"Jumlah ({o['jumlah']}): ")
    jumlah = int(jumlah_input) if jumlah_input else o["jumlah"]

    total = menu[ukuran] * jumlah

    orders[index] = {
        "nama": nama,
        "ukuran": ukuran,
        "jumlah": jumlah,
        "total": total,
        "waktu": o["waktu"]
    }

    simpan()
    print("✅ Order diupdate")

def menu_utama():
    while True:
        print("\n=== MENU ===")
        print("1. Tambah Order")
        print("2. Laporan Hari Ini")
        print("3. Laporan by Tanggal")
        print("4. Hapus Order")
        print("5. Edit Order")
        print("6. Keluar")

        pilih = input("Pilih: ")

        if pilih == "1":
            tambah_order()
        elif pilih == "2":
            laporan()
        elif pilih == "3":
            laporan_tanggal()
        elif pilih == "4":
            hapus_order()
        elif pilih == "5":
            edit_order()
        elif pilih == "6":
            break
        else:
            print("❌ Pilihan salah")

menu_utama()
