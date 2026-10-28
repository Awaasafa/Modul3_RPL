# salwa shafa salsabila_003
import tkinter.messagebox as messagebox
from models.anggota_model import AnggotaModel
from views.anggota_view import AnggotaView

class AnggotaController:
    def __init__(self):
        self.model = AnggotaModel()
        self.view = AnggotaView()

        # Variabel untuk menyimpan ID baris yang sedang dipilih di tabel
        self.selected_id = None

        # Binding tombol di View ke fungsi Controller
        self.view.btn_simpan.configure(command=self.simpan_data)
        self.view.btn_update.configure(command=self.perbarui_data)
        self.view.btn_delete.configure(command=self.hapus_data)

        # Binding event klik pada tabel agar data otomatis masuk ke form saat dipilih
        self.view.tabel.bind("<<TreeviewSelect>>", self.select_item)

        self.muat_data_tabel()

    def muat_data_tabel(self):
        # Mengosongkan tabel terlebih dahulu
        for item in self.view.tabel.get_children():
            self.view.tabel.delete(item)
            
        # Mengambil data dari model anggota
        data_anggota = self.model.get_all_anggota()
        for anggota in data_anggota:
            # Menggunakan 'alamat' sesuai kolom database
            self.view.tabel.insert("", "end", values=(anggota['id_anggota'], anggota['nama'], anggota['alamat']))

    def select_item(self, event):
        # Mengambil data dari baris tabel yang diklik pengguna
        selected_item = self.view.tabel.selection()
        if selected_item:
            item = self.view.tabel.item(selected_item)
            values = item['values']
            if values:
                self.selected_id = values[0] # Menyimpan ID anggota
                self.view.entry_nama.delete(0, 'end')
                self.view.entry_nama.insert(0, values[1])
                self.view.entry_alamat.delete(0, 'end')
                self.view.entry_alamat.insert(0, values[2])

    def simpan_data(self):
        nama = self.view.entry_nama.get()
        alamat = self.view.entry_alamat.get()
        
        if not nama or not alamat:
            messagebox.showwarning("Peringatan", "Semua kolom form harus diisi!")
            return
            
        berhasil = self.model.create_anggota(nama, alamat)
        if berhasil:
            messagebox.showinfo("Sukses", "Data anggota berhasil disimpan!")
            self.clear_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Terjadi kesalahan saat menyimpan data.")

    def perbarui_data(self):
        if not self.selected_id:
            messagebox.showwarning("Peringatan", "Pilih data yang ingin diperbarui dari tabel terlebih dahulu!")
            return

        nama = self.view.entry_nama.get()
        alamat = self.view.entry_alamat.get()

        if not nama or not alamat:
            messagebox.showwarning("Peringatan", "Semua kolom form harus diisi!")
            return

        berhasil = self.model.update_anggota(self.selected_id, nama, alamat)
        if berhasil:
            messagebox.showinfo("Sukses", "Data anggota berhasil diperbarui!")
            self.clear_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Terjadi kesalahan saat memperbarui data.")

    def hapus_data(self):
        if not self.selected_id:
            messagebox.showwarning("Peringatan", "Pilih data yang ingin dihapus dari tabel terlebih dahulu!")
            return

        konfirmasi = messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus data ini?")
        if konfirmasi:
            berhasil = self.model.delete_anggota(self.selected_id)
            if berhasil:
                messagebox.showinfo("Sukses", "Data anggota berhasil dihapus!")
                self.clear_form()
                self.muat_data_tabel()
            else:
                messagebox.showerror("Error", "Terjadi kesalahan saat menghapus data.")

    def clear_form(self):
        self.selected_id = None
        self.view.entry_nama.delete(0, 'end')
        self.view.entry_alamat.delete(0, 'end')

    def run(self):
        self.view.mainloop()