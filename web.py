from flask import Flask, request, redirect, render_template_string
import json
import os
from datetime import datetime

app = Flask(__name__)

FILE_NAME = "orders.json"

menu = {
    "medium": 30000,
    "large": 45000,
    "party": 80000
}

def load_orders():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as f:
            return json.load(f)
    return []

def save_orders(data):
    with open(FILE_NAME, "w") as f:
        json.dump(data, f, indent=2)

@app.route("/hapus/<int:index>")
def hapus(index):
    orders = load_orders()
    if 0 <= index < len(orders):
        orders.pop(index)
        save_orders(orders)
    return redirect("/")

@app.route("/", methods=["GET", "POST"])
def dashboard():
    orders = load_orders()

    # INPUT
    if request.method == "POST":
        nama = request.form["nama"]
        ukuran = request.form["ukuran"]
        jumlah = int(request.form["jumlah"])

        total = menu[ukuran] * jumlah

        orders.append({
            "nama": nama,
            "ukuran": ukuran,
            "jumlah": jumlah,
            "total": total,
            "waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        save_orders(orders)
        return redirect("/")

    # FILTER
    tanggal = request.args.get("tanggal") or datetime.now().strftime("%Y-%m-%d")
    filtered = [o for o in orders if "waktu" in o and o["waktu"].startswith(tanggal)]

    total = sum(o["total"] for o in filtered)

    produk = {}
    for o in filtered:
        produk[o["ukuran"]] = produk.get(o["ukuran"], 0) + o["jumlah"]

    # GRAFIK
    grafik = {}
    for o in orders:
        if "waktu" not in o:
            continue
        tgl = o["waktu"][:10]
        grafik[tgl] = grafik.get(tgl, 0) + o["total"]

    labels = list(grafik.keys())
    values = list(grafik.values())

    # TABLE
    rows = ""
    for i, o in enumerate(filtered):
        rows += f"<tr><td>{o['waktu']}</td><td>{o['nama']}</td><td>{o['ukuran']}</td><td>{o['jumlah']}</td><td>Rp{o['total']}</td><td><a href='/hapus/{i}' class='btn btn-danger btn-sm'>Hapus</a></td></tr>"

    produk_list = "".join([f"<li>{k}: {v} pcs</li>" for k,v in produk.items()])

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Dashboard</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

        <style>
        body {{ background-color: #121212; color: white; }}

        .card-menu {{
            cursor: pointer;
            transition: 0.2s;
        }}

        .card-menu:hover {{
            transform: scale(1.05);
            border: 2px solid #0d6efd;
        }}

        input[type="radio"]:checked + label {{
            border: 2px solid #0d6efd;
            background-color: #1a1a1a;
        }}
        </style>
    </head>

    <body>
    <div class="container mt-4">

        <h2>📊 Yummykitchen</h2>

        <!-- INPUT -->
        <form method="POST" class="mb-4">

            <input name="nama" class="form-control mb-2" placeholder="Nama pembeli" required>

            <div class="row text-center mb-3">

                <div class="col">
                    <input type="radio" name="ukuran" value="medium" id="medium" hidden checked>
                    <label for="medium" class="card card-menu p-2">
                        <img src="https://via.placeholder.com/80">
                        <h6>Medium</h6>
                        <small>Rp30.000</small>
                    </label>
                </div>

                <div class="col">
                    <input type="radio" name="ukuran" value="large" id="large" hidden>
                    <label for="large" class="card card-menu p-2">
                        <img src="https://via.placeholder.com/80">
                        <h6>Large</h6>
                        <small>Rp45.000</small>
                    </label>
                </div>

                <div class="col">
                    <input type="radio" name="ukuran" value="party" id="party" hidden>
                    <label for="party" class="card card-menu p-2">
                        <img src="https://via.placeholder.com/80">
                        <h6>Party</h6>
                        <small>Rp80.000</small>
                    </label>
                </div>

            </div>

            <input name="jumlah" type="number" class="form-control mb-2" placeholder="Jumlah" required>

            <button class="btn btn-success w-100">Tambah Order</button>
        </form>

        <!-- FILTER -->
        <form method="GET" class="mb-3">
            <input type="date" name="tanggal" value="{tanggal}" class="form-control">
            <button class="btn btn-primary mt-2">Filter</button>
        </form>

        <!-- OMZET -->
        <div class="card bg-success p-3 mb-3">
            <h4>Total Omzet: Rp{total}</h4>
        </div>

        <!-- PRODUK -->
        <div class="card bg-secondary p-3 mb-3">
            <h5>Produk Terjual</h5>
            <ul>{produk_list}</ul>
        </div>

        <!-- TABEL -->
        <table class="table table-dark table-striped">
            <thead>
                <tr>
                    <th>Waktu</th>
                    <th>Nama</th>
                    <th>Ukuran</th>
                    <th>Jumlah</th>
                    <th>Total</th>
                    <th>Aksi</th>
                </tr>
            </thead>
            <tbody>
                {rows}
            </tbody>
        </table>

        <!-- GRAFIK -->
        <canvas id="chart"></canvas>

    </div>

    <script>
        new Chart(document.getElementById('chart'), {{
            type: 'line',
            data: {{
                labels: {labels},
                datasets: [{{
                    label: 'Omzet',
                    data: {values},
                    borderWidth: 2
                }}]
            }}
        }});
    </script>

    </body>
    </html>
    """

    return render_template_string(html)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
