# salwa shafa salsabila_003
import tkinter.messagebox as messagebox
from models.buku_model import BukuModel
from views.buku_view import BukuView

class BukuController:
    def __init__(self, user_role="anggota"):
        # Menerima parameter user_role dari AuthController
        self.user_role = user_role
        self.model = BukuModel()
        self.view = BukuView()
        
        # Mengatur judul jendela sesuai mode role yang aktif
        self.view.title(f"Sistem Manajemen Perpustakaan - Mode: {self.user_role.upper()}")
        
        # Binding (mengikat) tombol di view dengan fungsi di controller
        self.view.btn_simpan.configure(command=self.simpan_data)
        self.view.btn_delete.configure(command=self.hapus_data)
        self.view.btn_update.configure(command=self.perbarui_data)
        

        # Penerapan Otorisasi Berbasis Peran (RBAC)
        if self.user_role == "anggota":
            self.view.btn_simpan.configure(state="disabled", text="Akses Terkunci (Khusus Admin)")
            self.view.btn_update.configure(state="disabled")
            self.view.btn_delete.configure(state="disabled")
            self.view.entry_judul.configure(state="disabled")
            self.view.entry_penulis.configure(state="disabled")
            self.view.entry_tahun.configure(state="disabled")
        
        # Memuat data ke tabel saat aplikasi pertama kali dibuka
        self.muat_data_tabel()
        
    def muat_data_tabel(self):
        # Mengosongkan isi tabel di view terlebih dahulu
        for item in self.view.tabel.get_children():
            self.view.tabel.delete(item)
            
        # Mengambil data dari model database
        data_buku = self.model.get_all_buku()
        
        # Memasukkan data ke dalam tabel view
        for buku in data_buku:
            self.view.tabel.insert("", "end", values=(buku['id_buku'], buku['judul'], buku['penulis'], buku['tahun_terbit']))
    
    def simpan_data(self):
        # Proteksi tambahan di sisi controller
        if self.user_role == "anggota":
            messagebox.showerror("Akses Ditolak", "Anda tidak memiliki izin untuk menambah data!")
            return

        # Mengambil teks dari kotak input di view
        judul = self.view.entry_judul.get()
        penulis = self.view.entry_penulis.get()
        tahun = self.view.entry_tahun.get()
        
        # Validasi form kosong
        if not judul or not penulis or not tahun:
            messagebox.showwarning("Peringatan", "Semua kolom form harus diisi!")
            return
        
        # Mengirim data ke model untuk disimpan
        berhasil = self.model.create_buku(judul, penulis, tahun)
        
        if berhasil:
            messagebox.showinfo("Sukses", "Data buku berhasil disimpan")
            # Bersihkan form input
            self.view.entry_judul.delete(0, 'end')
            self.view.entry_penulis.delete(0, 'end')
            self.view.entry_tahun.delete(0, 'end')
            # Muat ulang tabel agar data terbaru muncul
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Terjadi kesalahan saat menyimpan data.")
            
    def perbarui_data(self):
        if self.user_role == "anggota":
            messagebox.showerror("Akses Ditolak", "Anda tidak memiliki izin untuk memperbarui data!")
            return

        selected_item = self.view.tabel.focus()
        if not selected_item:
            messagebox.showwarning("Peringatan", "Pilih data buku yang ingin diperbarui di tabel!")
            return

        # Mengambil ID dari baris tabel yang diklik (kolom pertama)
        values = self.view.tabel.item(selected_item, "values")
        id_buku = values[0]

        judul = self.view.entry_judul.get()
        penulis = self.view.entry_penulis.get()
        tahun = self.view.entry_tahun.get()

        if not judul or not penulis or not tahun:
            messagebox.showwarning("Peringatan", "Semua kolom form harus diisi!")
            return

        berhasil = self.model.update_buku(id_buku, judul, penulis, tahun)
        if berhasil:
            messagebox.showinfo("Sukses", "Data buku berhasil diperbarui!")
            # Bersihkan form input
            self.view.entry_judul.delete(0, 'end')
            self.view.entry_penulis.delete(0, 'end')
            self.view.entry_tahun.delete(0, 'end')
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Terjadi kesalahan saat memperbarui data.")
            
    def hapus_data(self):
        if self.user_role == "anggota":
            messagebox.showerror("Akses Ditolak", "Anda tidak memiliki izin untuk menghapus data!")
            return

        selected_item = self.view.tabel.focus()
        if not selected_item:
            messagebox.showwarning("Peringatan", "Pilih data buku yang ingin dihapus di tabel!")
            return
            
        values = self.view.tabel.item(selected_item, "values")
        id_buku = values[0]
        
        konfirmasi = messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus data buku ini?")
        if konfirmasi:
            berhasil = self.model.delete_buku(id_buku)
            if berhasil:
                messagebox.showinfo("Sukses", "Data buku berhasil dihapus!")
                self.muat_data_tabel()
            else:
                messagebox.showerror("Error", "Terjadi kesalahan saat menghapus data.")

    def logout(self):
        self.view.destroy()
        from controllers.auth_controller import AuthController
        app_auth = AuthController()
        app_auth.run()

    # Fungsi untuk menyalakan aplikasi
    def run(self):
        self.view.mainloop()