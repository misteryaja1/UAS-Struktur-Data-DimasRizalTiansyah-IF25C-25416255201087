import csv
import os
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich import print

console = Console()

FILE_CSV = "tamu.csv"
ANTRIAN_CSV = "antrian.csv"

if not os.path.exists(FILE_CSV):
    with open(FILE_CSV, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(["ID", "Nama", "No_HP", "Status"])

if not os.path.exists(ANTRIAN_CSV):
    with open(ANTRIAN_CSV, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(["ID", "Nama"])

# BACA DATA TAMU

def baca_data():
    data = []

    with open(FILE_CSV, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=";")

        for row in reader:
            data.append(row)

    return data

# CREATE
def tambah_tamu():
    data = baca_data()

    id_baru = str(len(data) + 1)

    nama = input("Nama Tamu : ")
    no_hp = input("No HP      : ")

    with open(FILE_CSV, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow([id_baru, nama, no_hp, "Belum Konfirmasi"])

    console.print(
        "[bold green]✓ Tamu berhasil ditambahkan[/bold green]"
        )

    input("\nTekan Enter...")
    

# READ

def tampilkan_tamu():

    data = baca_data()

    if not data:
        console.print("[bold red]Belum ada data tamu[/bold red]")
        input("\nTekan Enter...")
        return

    table = Table(
        title="DAFTAR TAMU UNDANGAN",
        show_lines=True
    )

    table.add_column("ID", justify="center")
    table.add_column("Nama")
    table.add_column("No HP")
    table.add_column("Status")

    for tamu in data:

        if tamu["Status"] == "Hadir":
            status = "[green]Hadir[/green]"
        elif tamu["Status"] == "Tidak Hadir":
            status = "[red]Tidak Hadir[/red]"
        elif tamu["Status"] == "Akan Hadir":
            status = "[yellow]Akan Hadir[/yellow]"
        else:
            status = "[yellow]Belum Konfirmasi[/yellow]"

        table.add_row(
            tamu["ID"],
            tamu["Nama"],
            tamu["No_HP"],
            status
        )

    console.print(table)

    input("\nTekan Enter...")

# UPDATE

def edit_tamu():
    data = baca_data()

    id_cari = input("Masukkan ID Tamu : ")

    ditemukan = False

    for tamu in data:
        if tamu["ID"] == id_cari:
            tamu["Nama"] = input("Nama Baru : ")
            tamu["No_HP"] = input("No HP Baru : ")
            ditemukan = True
            break

    if ditemukan:
        with open(FILE_CSV, "w", newline="", encoding="utf-8") as file:
            fieldnames = ["ID", "Nama", "No_HP", "Status"]

            writer = csv.DictWriter(
                file,
                fieldnames=fieldnames,
                delimiter=";"
            )

            writer.writeheader()
            writer.writerows(data)

        console.print(
            "[bold green]✓ Data berhasil diubah[/bold green]"
        )
        input("\nTekan Enter...")

    else:
        console.print("[bold red]ID tidak ditemukan[/bold red]")
        input("\nTekan Enter...")

# DELETE

def hapus_tamu():
    data = baca_data()

    id_hapus = input("Masukkan ID yang akan dihapus : ")

    data_baru = [
        tamu for tamu in data
        if tamu["ID"] != id_hapus
    ]

    with open(FILE_CSV, "w", newline="", encoding="utf-8") as file:
        fieldnames = ["ID", "Nama", "No_HP", "Status"]

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
            delimiter=";"
        )

        writer.writeheader()
        writer.writerows(data_baru)

    console.print("[bold green]✓ Data berhasil dihapus[/bold green]")
    input("\nTekan Enter...")

# SEARCHING (HASH MAP)

def cari_tamu():
    data = baca_data()

    tamu_dict = {}

    for tamu in data:
        tamu_dict[tamu["ID"]] = tamu

    id_cari = input("Masukkan ID Tamu : ")

    if id_cari in tamu_dict:
        tamu = tamu_dict[id_cari]

        console.print("\n[bold green]DATA DITEMUKAN[/bold green]")
        console.print(f"ID     : {tamu['ID']}")
        console.print(f"Nama   : {tamu['Nama']}")
        console.print(f"No HP  : {tamu['No_HP']}")
        console.print(f"Status : {tamu['Status']}\n")
        input("\nTekan Enter...")

    else:
        console.print("[bold red]Tamu tidak ditemukan[/bold red]")
        input("\nTekan Enter...")

# SORTING

def urutkan_nama():
    data = baca_data()

    data.sort(key=lambda x: x["Nama"].lower())

    console.print("\n[bold green]DAFTAR TAMU (A-Z)[/bold green]")
    console.print("-" * 50)

    for tamu in data:
        console.print(f"{tamu['ID']} - {tamu['Nama']}")

    console.print()
    input("\nTekan Enter...")

# KONFIRMASI TIDAK HADIR
def konfirmasi_tidak_hadir():

    data = baca_data()

    id_tamu = input("Masukkan ID Tamu : ")

    for tamu in data:

        if tamu["ID"] == id_tamu:

            tamu["Status"] = "Tidak Hadir"

            with open(FILE_CSV, "w", newline="", encoding="utf-8") as file:

                fieldnames = [
                    "ID",
                    "Nama",
                    "No_HP",
                    "Status"
                ]

                writer = csv.DictWriter(
                    file,
                    fieldnames=fieldnames,
                    delimiter=";"
                )

                writer.writeheader()
                writer.writerows(data)

            console.print(
                "[bold yellow]✓ RSVP Tidak Hadir berhasil dicatat[/bold yellow]"
            )

            input("\nTekan Enter...")
            return

        console.print(
            "[bold red]ID tidak ditemukan[/bold red]"
        )

        input("\nTekan Enter...")

# RSVP KEHADIRAN

def rsvp_hadir():

    data = baca_data()

    id_tamu = input("Masukkan ID Tamu : ")

    for tamu in data:

        if tamu["ID"] == id_tamu:

            if tamu["Status"] == "Hadir":
                console.print(
                    f"[bold yellow]✓ {tamu['Nama']} sudah hadir[/bold yellow]"
                )
                input("\nTekan Enter...")
                return

            if tamu["Status"] == "Akan Hadir":
                console.print(
                    f"[bold yellow]✓ {tamu['Nama']} sudah melakukan RSVP[/bold yellow]"
                )
                input("\nTekan Enter...")
                return

            if tamu["Status"] == "Tidak Hadir":
                console.print(
                    f"[bold red]✗ {tamu['Nama']} sudah memilih Tidak Hadir[/bold red]"
                )
                input("\nTekan Enter...")
                return

            # Ubah status menjadi Akan Hadir
            tamu["Status"] = "Akan Hadir"

            # Simpan ke tamu.csv
            with open(FILE_CSV, "w", newline="", encoding="utf-8") as file:

                fieldnames = [
                    "ID",
                    "Nama",
                    "No_HP",
                    "Status"
                ]

                writer = csv.DictWriter(
                    file,
                    fieldnames=fieldnames,
                    delimiter=";"
                )

                writer.writeheader()
                writer.writerows(data)

            # Masukkan ke antrian check-in
            with open(
                ANTRIAN_CSV,
                "a",
                newline="",
                encoding="utf-8"
            ) as file:

                writer = csv.writer(
                    file,
                    delimiter=";"
                )

                writer.writerow([
                    tamu["ID"],
                    tamu["Nama"]
                ])

            console.print(
                f"[bold green]✓ {tamu['Nama']} berhasil RSVP Hadir[/bold green]"
            )

            input("\nTekan Enter...")
            return

    console.print("[bold red]ID tidak ditemukan[/bold red]")
    input("\nTekan Enter...")

# LIHAT ANTRIAN

def tampilkan_antrian():

    with open(
        ANTRIAN_CSV,
        "r",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(
            file,
            delimiter=";"
        )

        data = list(reader)

    if not data:
        console.print(
            "[yellow]Belum ada antrian check-in[/yellow]"
        )
        input("\nTekan Enter...")
        return

    table = Table(
        title="ANTRIAN check-in",
        show_lines=True
    )

    table.add_column("No", justify="center")
    table.add_column("Nama Tamu")

    for i, tamu in enumerate(data, start=1):

        table.add_row(
            str(i),
            tamu["Nama"]
        )

    console.print(table)

    input("\nTekan Enter...")

# PROSES CHECK-IN (QUEUE)

def proses_checkin():

    with open(
        ANTRIAN_CSV,
        "r",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(
            file,
            delimiter=";"
        )

        antrian = list(reader)

    if not antrian:
        console.print(
            "[bold red]Tidak ada antrian check-in[/bold red]"
        )
        input("\nTekan Enter...")
        return

    # FIFO (orang pertama dalam antrian)
    tamu_pertama = antrian[0]

    data_tamu = baca_data()

    for tamu in data_tamu:

        if tamu["ID"] == tamu_pertama["ID"]:

            # Sudah benar-benar datang ke acara
            tamu["Status"] = "Hadir"

    # Simpan perubahan status ke tamu.csv
    with open(
        FILE_CSV,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        fieldnames = [
            "ID",
            "Nama",
            "No_HP",
            "Status"
        ]

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
            delimiter=";"
        )

        writer.writeheader()
        writer.writerows(data_tamu)

    # Hapus dari antrian (FIFO)
    antrian.pop(0)

    with open(
        ANTRIAN_CSV,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        fieldnames = [
            "ID",
            "Nama"
        ]

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
            delimiter=";"
        )

        writer.writeheader()
        writer.writerows(antrian)

    console.print(
        f"[bold green]✓ {tamu_pertama['Nama']} berhasil check-in dan tercatat hadir[/bold green]"
    )

    input("\nTekan Enter...")

# MENU
from rich.panel import Panel
from rich.align import Align

while True:

    console.clear()

    data = baca_data()

    # Statistik RSVP
    total = len(data)

    hadir = len([
        x for x in data
        if x["Status"] == "Hadir"
    ])

    akan_hadir = len([
        x for x in data
        if x["Status"] == "Akan Hadir"
    ])

    tidak_hadir = len([
        x for x in data
        if x["Status"] == "Tidak Hadir"
    ])

    belum = len([
        x for x in data
        if x["Status"] == "Belum Konfirmasi"
    ])

    # Progress RSVP
    persentase = (
        ((akan_hadir + hadir + tidak_hadir) / total) * 100
    ) if total > 0 else 0

    panjang_bar = 20

    terisi = int(
        (persentase / 100) * panjang_bar
    )

    progress_bar = (
        "█" * terisi
        + "░" * (panjang_bar - terisi)
    )

    # Layout Rich
    layout = Layout()

    layout.split_row(
        Layout(name="menu", ratio=3),
        Layout(name="info", ratio=1)
    )

    layout["menu"].split_row(
        Layout(name="admin"),
        Layout(name="rsvp"),
        Layout(name="checkin")
    )

    layout["admin"].update(
    Panel(
        """
[green]1.[/green] Tambah Tamu
[green]2.[/green] Lihat Tamu
[green]3.[/green] Edit Tamu
[green]4.[/green] Hapus Tamu
[green]5.[/green] Cari Tamu
[green]6.[/green] Urutkan Nama

[red]0.[/red] Keluar
""",
        title="[bold cyan]ADMIN[/bold cyan]",
        border_style="cyan"
    )
)

    layout["rsvp"].update(
    Panel(
        """
    [green]7.[/green] RSVP Hadir
    [green]8.[/green] RSVP Tidak Hadir
    """,
        title="[bold yellow]RSVP[/bold yellow]",
        border_style="yellow"
    )
)

    layout["checkin"].update(
        Panel(
            """
        [green]9.[/green] Lihat Antrian
        [green]10.[/green] Proses Check-In
        """,
        title="[bold magenta]CHECK-IN[/bold magenta]",
        border_style="magenta"
    )
)

    sudah_rsvp = akan_hadir + hadir + tidak_hadir

    layout["info"].update(
    Panel(
        f"""
👥 Total : {total}
📨 Sudah RSVP : {sudah_rsvp}
🟡 Akan Hadir : {akan_hadir}
✅ Hadir : {hadir}
❌ Tidak Hadir : {tidak_hadir}
⏳ Belum Konfirmasi : {belum}
📊 Progress RSVP
[green]{progress_bar}[/green]

🎉 {persentase:.1f}%
""",
        title="[bold magenta]STATISTIK RSVP[/bold magenta]",
        border_style="bright_magenta"
    )
)

    console.print(
    Panel(
        Align.center(
            "[bold white]💒 SISTEM MANAJEMEN TAMU 💒[/bold white]\n"
            "[bold cyan]      RSVP PERNIKAHAN[/bold cyan]"
        ),
        title="[bold green]UAS STRUKTUR DATA[/bold green]",
        subtitle="[white]Dimas Rizal Tiansyah[/white]",
        border_style="bright_green",
        padding=(1, 2)
    )
)
    

    console.print(layout)

    pilihan = input("\nPilih Menu : ")

    if pilihan == "1":
        tambah_tamu()

    elif pilihan == "2":
        tampilkan_tamu()

    elif pilihan == "3":
        edit_tamu()

    elif pilihan == "4":
        hapus_tamu()

    elif pilihan == "5":
        cari_tamu()

    elif pilihan == "6":
        urutkan_nama()

    elif pilihan == "7":
        rsvp_hadir()

    elif pilihan == "8":
        konfirmasi_tidak_hadir()

    elif pilihan == "9":
        tampilkan_antrian()

    elif pilihan == "10":
        proses_checkin()

    elif pilihan == "0":
        console.print(
        "\n[bold red]Program selesai. Terima kasih.[/bold red]"
        )
        break

    else:
        console.print("[bold red]Pilihan tidak valid.[/bold red]\n")
        input("\nTekan Enter...")