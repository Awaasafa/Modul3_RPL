from unittest.mock import MagicMock
from models.buku_model import BukuModel

def test_create_buku_berhasil():
    # Menginisialisasi Model
    model = BukuModel()
    
    #Memanipulasi (Mock) koneksi database agar tidak mengotori data asli
    model.conn = MagicMock()
    mock_cursor = MagicMock()
    model.conn.cursor.return_value = mock_cursor
    
    #Melakukan eksekusi fungsi
    hasil = model.create_buku("Buku Testing", "Penulis QA", 2026)
    
    #Memverivikasi apakah fungsi mengembalikan nilai true
    assert hasil is True
    #Memverivikasi apakah cursor.execute benar-benar dipanggil dengan query yang benar
    mock_cursor.execute.assert_called_once()
    #Memverivikasi apakah perintah commit (simpan) dipanggil
    model.conn.commit.assert_called_once()
    
def test_get_all_buku_berhasil():
    # Menginisialisasi Model
    model = BukuModel()

    # Memanipulasi (Mock) koneksi database
    model.conn = MagicMock()
    mock_cursor = MagicMock()
    model.conn.cursor.return_value = mock_cursor

    # Menentukan nilai kembalian tiruan dari hasil fetchall database
    mock_cursor.fetchall.return_value = [
        (1, "Belajar Python", "Admin", 2023),
        (2, "Struktur Data", "Dosen", 2024)
    ]

    # Melakukan eksekusi fungsi
    hasil = model.get_all_buku()

    # Memverifikasi apakah hasil mengembalikan data berupa list
    assert isinstance(hasil, list)
    assert len(hasil) == 2

    # Memverifikasi apakah cursor.execute benar-benar dipanggil untuk mengambil data
    mock_cursor.execute.assert_called_once()
#SALWA SHAFA SALSABILA_003