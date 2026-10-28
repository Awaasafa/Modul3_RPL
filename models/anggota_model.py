from config.database import Database

class AnggotaModel:
    def __init__(self):
        # Menginisialisasi koneksi ke database dari folder config/database.py
        self.conn = Database().get_connection()
        
    def get_all_anggota(self):
        # Mengambil seluruh data anggota dari database
        if self.conn:
            cursor = self.conn.cursor(dictionary=True)
            query = "SELECT * FROM anggota"
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        return []
        
    def create_anggota(self, nama, alamat):
        # Menambahkan data anggota baru ke database
        if self.conn:
            cursor = self.conn.cursor()
            query = "INSERT INTO anggota (nama, alamat) VALUES (%s, %s)"
            try:
                cursor.execute(query, (nama, alamat))
                self.conn.commit()
                cursor.close()
                return True
            except Exception as e:
                print(f"Error: {e}")
                cursor.close()
                return False
        return False

    def update_anggota(self, id_anggota, nama, alamat):
        # Memperbarui data anggota berdasarkan ID
        if self.conn:
            cursor = self.conn.cursor()
            query = "UPDATE anggota SET nama = %s, alamat = %s WHERE id_anggota = %s"
            try:
                cursor.execute(query, (nama, alamat, id_anggota))
                self.conn.commit()
                cursor.close()
                return True
            except Exception as e:
                print(f"Error: {e}")
                cursor.close()
                return False
        return False

    def delete_anggota(self, id_anggota):
        # Menghapus data anggota berdasarkan ID
        if self.conn:
            cursor = self.conn.cursor()
            query = "DELETE FROM anggota WHERE id_anggota = %s"
            try:
                cursor.execute(query, (id_anggota,))
                self.conn.commit()
                cursor.close()
                return True
            except Exception as e:
                print(f"Error: {e}")
                cursor.close()
                return False
        return False