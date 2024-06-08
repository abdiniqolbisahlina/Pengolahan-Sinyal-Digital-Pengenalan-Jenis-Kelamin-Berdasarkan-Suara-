import numpy as np
import scipy.io.wavfile as wav
import csv

def find_pitch(filename):
    # Membaca file WAV
    sample_rate, data = wav.read(filename)

    # Mengonversi data menjadi float
    data = data.astype(float)

    # Menerapkan FFT pada data
    fft_data = np.fft.fft(data)

    # Menghitung spektrum frekuensi
    spectrum = np.abs(fft_data)

    # Mencari frekuensi dominan atau pitch
    index = np.argmax(spectrum)
    pitch = index * sample_rate / len(data)

    return pitch

# Inisialisasi variabel untuk pitch terbesar, pitch terkecil, dan total pitch dari gender perempuan
max_pitch_f = float('-inf')
min_pitch_f = float('inf')
total_pitch_f = 0

# Inisialisasi variabel untuk pitch terbesar, pitch terkecil, dan total pitch dari gender laki-laki
max_pitch_m = float('-inf')
min_pitch_m = float('inf')
total_pitch_m = 0

# Inisialisasi variabel untuk pitch terbesar dan pitch terkecil pada kategori female
max_female_pitch = 15837.5
min_female_pitch = 162.30769230769232

num_files = 25

# Membuka file CSV 
with open('data_gender_checker.csv', 'w', newline='') as file:
    writer = csv.writer(file)

    
    writer.writerow(['Nama File', 'Keluaran', 'Kebenaran', 'Pitch'])

    # Loop untuk memeriksa file WAV dari f0001_us_f0001_00001.wav sampai f0001_us_f0001_00025.wav
    for i in range(1, num_files + 1):
        filename = f'f0001_us_f0001_{i:05}.wav'
        pitch = find_pitch(filename)

        # Memperbarui pitch terbesar, pitch terkecil, dan total pitch
        max_pitch_f = max(max_pitch_f, pitch)
        min_pitch_f = min(min_pitch_f, pitch)
        total_pitch_f += pitch

        # Menentukan value keluaran berdasarkan range pitch tertinggi dan terendah dari suara perempuan
        if min_female_pitch <= pitch <= max_female_pitch:
            keluaran = 'Perempuan'
        else:
            keluaran = 'Laki-laki'

        # Menentukan kebenaran suara berdasarkan nama file
        if 'm0001' in filename:
            kebenaran = 'Laki-laki'
        elif 'f0001' in filename:
            kebenaran = 'Perempuan'
        else:
            kebenaran = 'Tidak diketahui'

        # Menulis baris data ke file CSV
        writer.writerow([filename, keluaran, kebenaran, pitch])

        print(filename)
        print('Pitch:', pitch, 'Hz\n')


    # Loop untuk memeriksa file WAV dari m0001_us_m0001_00001.wav sampai m0001_us_m0001_00025.wav
    for i in range(1, num_files + 1):
        filename = f'm0001_us_m0001_{i:05}.wav'
        pitch = find_pitch(filename)

        # Memperbarui pitch terbesar, pitch terkecil, dan total pitch
        max_pitch_m = max(max_pitch_m, pitch)
        min_pitch_m = min(min_pitch_m, pitch)
        total_pitch_m += pitch

        # Menentukan value keluaran berdasarkan range pitch tertinggi dan terendah dari suara perempuan
        if min_female_pitch <= pitch <= max_female_pitch:
            keluaran = 'Perempuan'
        else:
            keluaran = 'Laki-laki'

        # Menentukan kebenaran suara berdasarkan nama file
        if 'm0001' in filename:
            kebenaran = 'Laki-laki'
        elif 'f0001' in filename:
            kebenaran = 'Perempuan'
        else:
            kebenaran = 'Tidak diketahui'

        # Menulis baris data ke file CSV
        writer.writerow([filename, keluaran, kebenaran, pitch])

        print(filename)
        print('Pitch:', pitch, 'Hz\n')

# Menghitung rata-rata pitch berdasarkan gender perempuan
avg_pitch_f = total_pitch_f / num_files

print('Dari Gender Perempuan')
print("Pitch terbesar:", max_pitch_f, "Hz")
print("Pitch terkecil:", min_pitch_f, "Hz")
print("Rata-rata pitch:", avg_pitch_f, "Hz\n")

# Menghitung rata-rata pitch berdasarkan gender laki laki
avg_pitch_m = total_pitch_m / num_files

print('Dari Gender Laki - Laki')
print("Pitch terbesar:", max_pitch_m, "Hz")
print("Pitch terkecil:", min_pitch_m, "Hz")
print("Rata-rata pitch:", avg_pitch_m, "Hz\n")

# Menghitung tingkat akurasi data
def hitung_akurasi(file_csv, kolom_keluaran, kolom_kebenaran):
    total_data = 0
    data_benar = 0

    with open(file_csv, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            keluaran = row[kolom_keluaran]
            kebenaran = row[kolom_kebenaran]

            if keluaran == kebenaran:
                data_benar += 1

            total_data += 1

    akurasi_benar = (data_benar / total_data) * 100
    return akurasi_benar
    
# Contoh penggunaan
nama_file_csv = 'data_gender_checker.csv'
kolom_keluaran = 'Keluaran'
kolom_kebenaran = 'Kebenaran'

akurasi = hitung_akurasi(nama_file_csv, kolom_keluaran, kolom_kebenaran)
print(f'Tingkat akurasi benar : {akurasi}%')
print(f'Tingkat akurasi salah : {100 - akurasi}%')
