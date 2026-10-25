#Salwa Shafa salsabila_003
import tkinter.messagebox as messagebox
from models.buku_model import BukuModel
from views.buku_view import BukuView

class BukuController:
    def __init__(self):
        #inisialisasi Model dan View
        self.model = BukuModel()
        self.view = BukuView()
        
        #Binding (mengikat) tombol di view dengan fungsi di controller
        self.view.btn_simpan.configure(command=self.simpan_data)
        
        #memuat data ke tabel saataplikasi pertama kalai dibuka
        self.muat_data_tabel()
        
    def muat_data_tabel (self):
        #mengosongkan isi tabel di view terlebih dahulu
        for item in self.view.tabel.get_children():
            self.view.tabel.delete(item)
            
        #mengambil data dari model database
        data_buku = self.model.get_all_buku()
        
        #memasukkan data baru ke dalam tabel view
        for buku in data_buku:
            self.view.tabel.insert("","end", values=(buku['id_buku'], buku['penulis'], buku['tahun_terbit']))
    
    def simpan_data(self):
        #mengambil teks dari kotak input di view
        judul = self.view.entry_judul.get()
        penulis = self.view.entry_judul.get()
        tahun = self.view.entry_tahun.get()
        
        #validasi form kosong
        if not judul or not penulis or not tahun:
            messagebox.showwarning("peringatan", "Semua kolom form harus diisi!")
            return
        
        #mengirim data ke model untuk disimpan
        berhasil = self.model.create_buku(judul, penulis, tahun)
        
        if berhasil:
            messagebox.showinfo("Sukses", "Data buku berhasil disimpan")
            #Bersihkan form input
            self.view.entry_judul.delete(0,'end')
            self.view.entry_penulis.delete(0,'end')
            self.view.entry_tahun.delete(0,'end')
            #muat ulang tabel agar data terbaru muncul
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Terjadi kesalahan saat menyimpan data.")
    
    
    #Fungsi untuk menyalakan aplikasi
    def run(self):
        self.view.mainloop()
        
        
        
        
        
        
        
        
        
        
        