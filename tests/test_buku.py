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
#SALWA SHAFA SALSABILA_003