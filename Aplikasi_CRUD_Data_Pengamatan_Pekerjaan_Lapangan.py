# ===================================================================================================================================================
# ==================================================================== DATA AWAL ====================================================================
# Import tabulate untuk penyajian data dalam tabel
from tabulate import tabulate
import math

# Data header untuk tabulate
headerMain = ['KODE', 'PEKERJAAN', 'SATUAN', 'JUMLAH\nPEKERJA', 'MATERIAL TERPAKAI', 'WAKTU\nSIKLUS', 'VOLUME\nTERCAPAI', 'PRODUKTIVITAS\nPEKERJA\n(OUTPUT)']
headerMaterial = ['KODE\nMATERIAL', 'MATERIAL', 'SATUAN']
headerPekerjaan = ['KODE\nPEKERJAAN', 'PEKERJAAN','SATUAN\nPEKERJAAN', 'MATERIAL']
headerSimulasi = ['STATUS\nDATA','PRODUKTIVITAS\nDATA', 'JUMLAH\nPEKERJA', 'VOLUME\nPEKERJAAN', 'WAKTU', 'STATUS']
helperUpdPengamatan = [['','','','id Col. = 1','id Col. = 2','id Col. = 3','id Col. = 4','']]

# Data material (penunjang)
material = {
    'M001':['Portland Cement (PC)', 'kg'],
    'M002':['Pasir Cor', 'm3'],
    'M003':['Batu pecah mesin 2/3', 'm3'],
    'M004':['Air Bersih', 'ltr'],
    'M005':['Batu Kali', 'm3'],
    'M006':['Pasir Pasang', 'm3'],
    'M007':['Pasir Urug', 'm3'],
    'M008':['Lantai Granitile', 'bh'],
    'M009':['Portland Cement (PC) Warna', 'bh'],
    'M010':['Bata Merah','bh']
    }

# Data pekerjaan (penunjang)
pekerjaan = {
    'P001':['Rabat beton', 'm3', ['M001', 'M002', 'M003', 'M004']],
    'P002':['Pasang pondasi\nbatu kali,\n1 Pc : 6 Ps', 'm3',['M005', 'M001', 'M006']],
    'P003':['Pasang pondasi\nbatu kosong', 'm3',['M005', 'M007']],
    'P004':['Pasang Lantai\nGranitile', 'm2',['M008', 'M001', 'M006', 'M009']],
    'P005':['Pasangan bata\nmerah tebal\n1 bata, 1 Pc : 6 Ps', 'm2', ['M010', 'M001', 'M006']]
}

# Data pengamatan (utama)
pengamatan = {
    'P001/001':[3, [42, 0.15, 0.14, 39.2], '40m 21d', 0.182],
    'P001/002':[3, [63.8, 0.18, 0.2, 59.7], '45m 17d', 0.278],
    'P001/003':[3, [40.3, 0.1, 0.13, 37.6], '42m 57d', 0.175],
    'P001/004':[3, [44, 0.12, 0.15, 41.2], '36m 2d', 0.192],
    'P001/005':[4, [52.8, 0.15, 0.18, 49.4], '37m 22d', 0.23],
    'P002/001':[11, [2, 195.3, 0.9], '1j 50m 12d', 1.669],
    'P002/002':[11, [1.9, 191.6, 0.9], '2j 2m', 1.638],
    'P002/003':[11, [1.7, 164.2, 0.8], '1j 55m 19d', 1.404],
    'P002/004':[11, [0.2, 16.3, 0.1], '1j 13m', 0.139],
    'P002/005':[10, [1.93, 189.1, 0.9], '1j 48m 37d', 1.616],
    'P003/001':[4, [0.52, 0.19], '41m 2d', 0.429],
    'P003/002':[4, [0.73, 0.26], '50m', 0.61],
    'P003/003':[4, [0.74, 0.27], '44m 12d', 0.429],
    'P003/004':[4, [0.6, 0.2], '47m 53d', 0.507],
    'P003/005':[4, [0.88, 0.3], '51m 29d', 0.729],
    'P004/001':[5, [2.8, 8.76, 0.04, 1.4], '20m 14d', 0.911],
    'P004/002':[5, [3.25, 10, 0.05, 1.6], '24m 36d', 1.048],
    'P004/003':[5, [3.3, 10.2, 0.05, 1.5], '21m 44d', 1.058],
    'P004/004':[6, [3.4, 10.4, 0.05, 1.6], '24m 32d', 1.089],
    'P004/005':[5, [3.3, 10.4, 0.04, 1.7], '25m 48d', 1.131],
    'P005/001':[5, [375, 49.5, 0.3], '21m 5d', 2.679],
    'P005/002':[4, [310, 41, 0.2], '18m 12d', 2.217],
    'P005/003':[5, [444, 58.5, 0.4], '24m 36d', 3.172],
    'P005/004':[5, [371, 49, 0.3], '20m 24d', 2.65],
    'P005/005':[4, [280, 39, 0.2], '20m 2d', 2.017]
}

# ==================================================================================================================================================
# ==================================================================== FUNCTION ====================================================================
# Fungsi konversi format waktu siklus
def waktuKeJam (waktu):
    '''
    Melakukan konversi format waktu siklus yang diinput user (dalam kombinasi keseluruhan jam, menit, detik atau sebagian) menjadi format jam
    Args:
        Waktu (str): format awal waktu dengan 'j' penanda jam, 'm' penanda menit, 'd' penanda detik
    Return:
        hasilJam (float): format akhir waktu dalam satuan jam
    '''
    hasilJam = 0
    for i in waktu.split():
        if i[-1] == 'j':
            hasilJam += int(i[:-1])
        elif i[-1] == 'm':
            hasilJam += int(i[:-1])/60
        elif i[-1] == 'd':
            hasilJam += int(i[:-1])/3600
    return hasilJam

# Fungsi perhitungan produktivitas pekerja
def hitungProd (siklus, pekerja, volume):
    '''
    Melakukan perhitungan produktivitas pekerja
    Args:
        siklus (float): waktu siklus. didapat dari fungsi waktuKeJam
        pekerja (int): jumlah pekerja pada suatu pengamatan pekerjaan
        volume (float): volume yang tercapai pada suatu pengamatan pekerjaan
    Return:
        prod (float): produktivitas pekerja dengan satuan per org per hari (1 hari diasumsikan 8 jam kerja)
    '''
    prod = round((((volume/waktuKeJam(siklus)) * 8)/pekerja), 3)
    return prod

# ================================================================= FUNCTION FITUR =================================================================
# 1. FITUR READ
# 1.1 Read seluruh data
def readFull():
    '''
    Menampilkan seluruh data pengamatan dengan format yang telah ditentukan. Selain menggunakan data pengamatan (data utama) digunakan juga data 
    material dan pekerjaan sebagai data penunjang.
    Args:
        None
    Return:
        None
    '''
    headerMain = ['KODE', 'PEKERJAAN', 'SATUAN', 'JUMLAH\nPEKERJA', 'MATERIAL TERPAKAI', 'WAKTU\nSIKLUS', 'VOLUME\nTERCAPAI', 'PRODUKTIVITAS\nPEKERJA\n(OUTPUT)']
    listKecil = []
    listBesar = []
    materialRapi = ''
    for kode1, isi1 in pengamatan.items():
        listKecil.append(kode1)
        for kode0, isi0 in pekerjaan.items():
            if kode1[:4] == kode0:
                listKecil.append(isi0[0])
                listKecil.append(isi0[1])
                satuan = isi0[1]
                materialList = [[i, j] for i, j in zip(isi0[2], isi1[1])]
                for items in materialList:
                    kodeM = items[0]
                    if kodeM in material:
                        items.append(material[kodeM][0])
                        items.append(material[kodeM][1])
        listKecil.append(isi1[0])
        pekerja = isi1[0]
        for isi2 in materialList:
            materialRapi += f'{isi2[2]}: {isi2[1]} {isi2[3]}\n'
        materialRapi2 = materialRapi[:-1]
        listKecil.append(materialRapi2)
        materialRapi2 = ''
        materialRapi = ''
        materialList = []
        listKecil.append(isi1[2])
        siklus = isi1[2]
        listKecil.append(f'{isi1[3]} {satuan}')
        volume = isi1[3]
        listKecil.append(f'{hitungProd(siklus, pekerja, volume)}\n{satuan}/(org/hari)')
        listBesar.append(listKecil)
        listKecil = []
    print(f'Menampilkan seluruh data pengamatan:\n{tabulate(listBesar, headerMain, tablefmt="grid")}')
    return

# 1.2 Read data dengan primary key yang ditentukan user
def readSpesifik(iptKey):
    '''
    Menyimpan hanya 1 buah data sesuai input user (primary key). primary key terdapat pada data pengamatan yaitu kode pengamatan
    Args:
        iptKey (str): primary key hasil inputan user
    Return:
        listBesar (list): data pengamatan yang bersesuaian dengan iptKey untuk nantinya dijadikan output berupa tabel
    '''
    listKecil = []
    listBesar = []
    materialRapi = ''
    for kode1, isi1 in pengamatan.items():
        if iptKey.lower() == kode1.lower():
            listKecil.append(kode1)
            for kode0, isi0 in pekerjaan.items():
                if kode1[:4] == kode0:
                    listKecil.append(isi0[0])
                    listKecil.append(isi0[1])
                    satuan = isi0[1]
                    materialList = [[i, j] for i, j in zip(isi0[2], isi1[1])]
                    for items in materialList:
                        kodeM = items[0]
                        if kodeM in material:
                            items.append(material[kodeM][0])
                            items.append(material[kodeM][1])
            listKecil.append(isi1[0])
            pekerja = isi1[0]
            for isi2 in materialList:
                materialRapi += f'{isi2[2]}: {isi2[1]} {isi2[3]}\n'
            materialRapi2 = materialRapi[:-1]
            listKecil.append(materialRapi2)
            materialRapi2 = ''
            materialRapi = ''
            materialList = []
            listKecil.append(isi1[2])
            siklus = isi1[2]
            listKecil.append(f'{isi1[3]} {satuan}')
            volume = isi1[3]
            listKecil.append(f'{hitungProd(siklus, pekerja, volume)}\n{satuan}/(org/hari)')
            listBesar.append(listKecil)
            listKecil = []
    return listBesar

# 1.3 Read data dengan keyword(s) yang ditentukan oleh user
def readSpesifik2 (spesifik):
    '''
    Menyimpan data yang bersesuaian dengan kata kunci(keyword(s)) yang diinput oleh user. keyword(s) tidak harus berupa kode pengamatan (primary key)
    namun dapat berupa nama pekerjaan atau kode pekerjaan
    Args:
        spesifik(str): kata kunci yang diinput user
    Return:
        listAkhir(list): data pengamatan yang bersesuaian dengan spesifik untuk nantinya dijadikan output berupa tabel 
    '''
    listKecil = []
    listAkhir = []
    materialRapi = ''
    for kode1, isi1 in pengamatan.items():
        if spesifik.upper() in kode1.upper():
            listKecil.append(kode1)
            for kode0, isi0 in pekerjaan.items():
                if kode1[:4] == kode0:
                    listKecil.append(isi0[0])
                    listKecil.append(isi0[1])
                    satuan = isi0[1]
                    materialList = [[i, j] for i, j in zip(isi0[2], isi1[1])]
                    for items in materialList:
                        kodeM = items[0]
                        if kodeM in material:
                            items.append(material[kodeM][0])
                            items.append(material[kodeM][1])
            listKecil.append(isi1[0])
            pekerja = isi1[0]
            for isi2 in materialList:
                materialRapi += f'{isi2[2]}: {isi2[1]} {isi2[3]}\n'
            materialRapi2 = materialRapi[:-1]
            listKecil.append(materialRapi2)
            materialRapi2 = ''
            materialRapi = ''
            materialList = []
            listKecil.append(isi1[2])
            siklus = isi1[2]
            listKecil.append(f'{isi1[3]} {satuan}')
            volume = isi1[3]
            listKecil.append(f'{hitungProd(siklus, pekerja, volume)}\n{satuan}/(org/hari)')
            listAkhir.append(listKecil)
            listKecil = []
        elif spesifik.upper() in pekerjaan[kode1[:4]][0].upper():
            listKecil.append(kode1)
            for kode0, isi0 in pekerjaan.items():
                if kode1[:4] == kode0:
                    listKecil.append(isi0[0])
                    listKecil.append(isi0[1])
                    satuan = isi0[1]
                    materialList = [[i, j] for i, j in zip(isi0[2], isi1[1])]
                    for items in materialList:
                        kodeM = items[0]
                        if kodeM in material:
                            items.append(material[kodeM][0])
                            items.append(material[kodeM][1])
            listKecil.append(isi1[0])
            pekerja = isi1[0]
            for isi2 in materialList:
                materialRapi += f'{isi2[2]}: {isi2[1]} {isi2[3]}\n'
            materialRapi2 = materialRapi[:-1]
            listKecil.append(materialRapi2)
            materialRapi2 = ''
            materialRapi = ''
            materialList = []
            listKecil.append(isi1[2])
            siklus = isi1[2]
            listKecil.append(f'{isi1[3]} {satuan}')
            volume = isi1[3]
            listKecil.append(f'{hitungProd(siklus, pekerja, volume)}\n{satuan}/(org/hari)')
            listAkhir.append(listKecil)
            listKecil = []
    return listAkhir

# 1.4 Read data material (data penunjang)
def readMaterial():
    '''
    Menampilkan seluruh data material dalam tabel
    Args:
        None
    Return:
        None
    '''
    isiTabel = [[i, j[0], j[1]] for i, j in material.items()]
    print(f'Menampilkan seluruh data material:\n{tabulate(isiTabel, headerMaterial, tablefmt="psql")}')
    return

# 1.5 Read data pekerjaan (data penunjang)
def readPekerjaan():
    '''
    Menampilkan seluruh data pekerjaan dalam tabel
    Args:
        None
    Return:
        None
    '''
    listKecil = []
    listPekerjaan = []
    for i, j in pekerjaan.items():
        listKecil.append(i)
        listKecil.append(j[0])
        listKecil.append(j[1])
        materialRapi = ''
        for k in j[2]:
            if k in material:
                materialRapi += f'{material[k][0]}\n'
        listKecil.append(materialRapi[:-1])
        materialRapi = ''
        listPekerjaan.append(listKecil)
        listKecil = []
    print(f'Menampilkan seluruh data pekerjaan:\n{tabulate(listPekerjaan, headerPekerjaan, tablefmt="grid")}')
    return 

# 2. FITUR CREATE
# 2.1 Create 1 data pengamatan
def createPengamatan(iptKode, iptPekerja, crMaterial, iptSiklus, iptVolume):
    '''
    Menyimpan 1 data pengamatan baru yang nantinya dapat ditambahkan pada database pengamatan. untuk bagian kode, user hanya perlu menginput kode pekerjaan 
    dan kode pengamatan akan di-generate secara otomatis.
    Args:
        iptKode(str): kode pekerjaan
        iptPekerja(int): jumlah pekerja
        crMaterial(list): jumlah material yang digunakan dalam bentuk list 
        iptSiklus(str): waktu siklus pekerjaan
        iptVolume(int): volume yang dicapai
    Return:
        crHasil(list): data pengamatan pekerjaan yang dikelompokkan dalam list (yang akan di-append pada database utama apabila user memilih untuk menambahkan data)
    '''
    cariIndeks = []

    # Indeks pengamatan
    for i in pengamatan.keys():
        if iptKode in i:
            cariIndeks.append(int(i[5:]))
    
    idks = max(cariIndeks)
    if len(str(idks)) == 1:
        crIndeks = f'{iptKode}/00{idks+1}'
    elif len(str(idks)) == 2:
        crIndeks = f'{iptKode}/0{idks+1}'
    elif len(str(idks)) == 3:
        crIndeks = f'{iptKode}/{idks+1}'

    crHasil = {crIndeks: [iptPekerja, crMaterial, iptSiklus, iptVolume]}
    return crHasil

# 2.2 Create lebih dari satu data pengamatan 
def createPengamatan2(iptBerapa, iptKode, iptPekerja, iptMaterial, iptSiklus, iptVolume):
    '''
    Menyimpan beberapa data pengamatan (hanya untuk 1 jenis pekerjaan) sekaligus yang nantinya dapat ditambahkan pada database pengamatan.
    Args:
        iptBerapa(int): berapa banyak data yang ingin ditambahkan oleh user
        iptKode(str): kode pekerjaan
        iptPekerja(list): jumlah pekerja dalam bentuk list (HARUS BERURUTAN)
        iptMaterial(list): material yang digunakan dalam bentuk list (HARUS BERURUTAN)
        iptSiklus(list): waktu siklus pengamatan pekerjaan dalam bentuk list (HARUS BERURUTAN)
        iptVolume(list): volume yang tercapai dalam bentuk list (HARUS BERURUTAN)
    Return:
        crHasil(dict): dictionary berisi data pengamatan yang telah diinput user (yang akan di-update pada database utama apabila user memilih untuk menambahkan data)
    '''
    cariIndeks = []
    crHasil = {}

    for i in range(iptBerapa):
        for j in pengamatan.keys():
            if iptKode in j:
                cariIndeks.append(int(j[5:]))
        
        idks = max(cariIndeks)
        if len(str(idks)) == 1:
            crIndeks = f'{iptKode}/00{idks+1}'
        elif len(str(idks)) == 2:
            crIndeks = f'{iptKode}/0{idks+1}'
        elif len(str(idks)) == 3:
            crIndeks = f'{iptKode}/{idks+1}'

        crHasil[crIndeks] = [iptPekerja[i], iptMaterial[i], iptSiklus[i], iptVolume[i]]
        cariIndeks.append(int(crIndeks[5:]))
        crIndeks = []
    return crHasil

# 2.3 Create data material
def createMaterial(iptKode, iptNama, iptSatuan):
    '''
    Menyimpan 1 data material sesuai dengan iputan user
    Args:
        iptKode(str): kode material yang akan diinput (HARUS UNIK)
        iptNama(str): nama material
        iptSatuan(str): satuan material
    Return:
        crHasil(dict): dictionary berisi data material yang telah diinput user (yang akan di-update pada database apabila user memilih untuk menambahkan data)
    '''
    iptKode = 'M011'
    iptNama = 'Kolplin Kaca Gelap t: 8 cm'
    iptSatuan = 'm'
    crHasil = {iptKode: [iptNama, iptSatuan]}  
    return crHasil

# 2.4 Create data pekerjaan
def createPekerjaan(iptKode, iptNama, iptSatuan, iptMaterial):
    '''
    Menyimpan 1 data pekerjaan sesuai dengan iputan user
    Args:
        iptKode(str): kode pekerjaan yang akan diinput (HARUS UNIK)
        iptNama(str): nama pekerjaan
        iptSatuan(str): satuan pekerjaan
        iptMaterial(list): list material yang digunakan untuk pekerjaan
    Return:
        crHasil(dict): dictionary berisi data pekerjaan yang telah diinput user (yang akan di-update pada database apabila user memilih untuk menambahkan data)
    '''
    iptKode = 'P006'
    iptNama = 'Pasang Kolplint\nLantai T : 8 cm\n( Kaca Gelap )'
    iptSatuan = 'm'
    iptMaterial = ['M001', 'M002']
    crHasil = {iptKode: [iptNama, iptSatuan, iptMaterial]}
    return crHasil

# 3. FITUR UPDATE
# 3.1 Update data pengamatan (jumlah pekerja, waktu siklus, dan volume tercapai)
def updatePengamatan1(kodeSp, upIdks, upBaru):
    '''
    Melakukan update nilai pada data pengamatan HANYA UNTUK jumlah pekerja, waktu siklus, dan volume tercapai
    Args:
        kodeSp(str): kode pengamatan
        upIdks(str): penomoran kolom data yang dapat diganti
        upBaru(int, str, float): nilai baru dari nilai
    Return:
        None
    '''
    if upIdks == '1':
        while True:
            yakinU1 = input(f'Apakah Anda yakin mengganti jumlah pekerja dari {pengamatan[kodeSp][0]} org menjadi {upBaru} org?: (y / n): ')
            if yakinU1 == 'y':
                pengamatan[kodeSp][0] = upBaru
                print(f'-------------------------- DATA PENGAMATAN "{kodeSp}" BERHASIL DIUBAH --------------------------' )
                break
            elif yakinU1 == 'n':
                print(f'-------------------------- DATA PENGAMATAN "{kodeSp}" TIDAK DIUBAH --------------------------' )
                break
            else:
                print('*** INPUTAN TIDAK VALID ***')
    
    elif upIdks == '3':
        while True:
            yakinU1 = input(f'Apakah Anda yakin mengganti waktu siklus dari {pengamatan[kodeSp][2]} menjadi {upBaru} ?: (y / n): ')
            if yakinU1 == 'y':
                pengamatan[kodeSp][2] = upBaru
                print(f'-------------------------- DATA PENGAMATAN "{kodeSp}" BERHASIL DIUBAH --------------------------' )
                break
            elif yakinU1 == 'n':
                print(f'-------------------------- DATA PENGAMATAN "{kodeSp}" TIDAK DIUBAH --------------------------' )
                break
            else:
                print('*** INPUTAN TIDAK VALID ***')
    
    elif upIdks == '4':
        while True:
            yakinU1 = input(f'Apakah Anda yakin mengganti volume pengamatan dari {pengamatan[kodeSp][2]} {pekerjaan[kodeSp][1]} menjadi {upBaru} {pekerjaan[kodeSp][1]} ?: (y / n): ')
            if yakinU1 == 'y':
                pengamatan[kodeSp][3] = upBaru
                print(f'-------------------------- DATA PENGAMATAN "{kodeSp}" BERHASIL DIUBAH --------------------------' )
                break
            elif yakinU1 == 'n':
                print(f'-------------------------- DATA PENGAMATAN "{kodeSp}" TIDAK DIUBAH --------------------------' )
                break
            else:
                print('*** INPUTAN TIDAK VALID ***')
    return

def updatePengamatan2(kodeSp, upBaru, idMat):
    '''
    Melakukan update nilai pada data pengamatan HANYA UNTUK material terpakai
    Args:
        kodeSp(str): kode pengamatan
        upBaru(float): nilai baru dari nilai
        idMat(int): penomoran material
    Return:
        None
    '''
    while True:
        yakinU1 = input(f'Apakah Anda yakin mengganti volume material?: (y / n): ')
        if yakinU1 == 'y':
            pengamatan[kodeSp][1][idMat-1] = upBaru
            print(f'-------------------------- DATA PENGAMATAN "{kodeSp}" BERHASIL DIUBAH --------------------------' )
            break
        elif yakinU1 == 'n':
            print(f'-------------------------- DATA PENGAMATAN "{kodeSp}" TIDAK DIUBAH --------------------------' )
            break
        else:
            print('*** INPUTAN TIDAK VALID ***')
    return


# 4. FITUR DELETE
# 4.1 Hapus 1 data pengamatan
def deletePengamatan(iptKodePnDel):
    '''
    Melakukan penghapusan 1 data pengamatan
    Args:
        iptKodePnDel(str): Kode pengamatan
    Return:
        None
    '''
    while True:
        yakinDl1 = input(f'Apakah Anda yakin menghapus data pengamatan {iptKodePnDel}?: (y / n): ')
        if yakinDl1 == 'y':
            del pengamatan[iptKodePnDel]
            print(f'-------------------------- DATA PENGAMATAN "{iptKodePnDel}" BERHASIL DIHAPUS --------------------------' )
            break
        elif yakinDl1 == 'n':
            print(f'-------------------------- DATA PENGAMATAN "{iptKodePnDel}" TIDAK DIHAPUS --------------------------' )
            break
        else:
            print('*** INPUTAN TIDAK VALID ***')
    return

# 4.2 Hapus data pekerjaan pada data pengamatan
def deletePengamatan2(iptKodePkDel):
    '''
    Melakukan penghapusan beberapa data pengamatan (sesuai dengan pekerjaan)
    Args:
        iptKodePkDel(str): Kode pekerjaan
    Return:
        None
    '''
    while True:
        yakinDl2 = input(f'Apakah Anda yakin menghapus data pengamatan {iptKodePkDel}?: (y / n): ')
        if yakinDl2 == 'y':
            listHapus =[]
            for i in pengamatan.keys():
                if iptKodePkDel == i[:4]:
                    listHapus.append(i)
            
            for j in listHapus:
                del pengamatan[j] 
            
            print(f'-------------------------- DATA PENGAMATAN "{iptKodePkDel}" BERHASIL DIHAPUS --------------------------' )
            break
        elif yakinDl2 == 'n':
            print(f'-------------------------- DATA PENGAMATAN "{iptKodePkDel}" TIDAK DIHAPUS --------------------------' )
            break
        else:
            print('*** INPUTAN TIDAK VALID ***')
    return


# 4.3 Hapus seluruh data pengamatan
def deleteSemua():
    '''
    Melakukan penghapusan SELURUH data pengamatan
    Args:
        None
    Return:
        None
    '''
    while True:
        yakinDl1 = input(f'Apakah Anda yakin menghapus SELURUH data pengamatan?: (y / n): ')
        if yakinDl1 == 'y':
            pengamatan.clear()
            print(f'-------------------------- SELURUH DATA PENGAMATAN BERHASIL DIHAPUS --------------------------' )
            break
        elif yakinDl1 == 'n':
            print(f'-------------------------- SELURUH DATA PENGAMATAN TIDAK DIHAPUS --------------------------' )
            break
        else:
            print('*** INPUTAN TIDAK VALID ***')
    return

# 5. FITUR SIMULASI
# 5.1 Simulasi pekerjaan
def simulasi(iptSubS, iptKodePek):
    '''
    Melakukan simulasi dengan parameter jumlah pekerja, waktu pekerjaan, volume pekerjaan DENGAN BASIS rata-rata produktivitas data pengamatan
    Args:
        iptSubS(str): pilihan menu untuk menentukan parameter mana yang dijadikan missing variable
        iptKodePek(str): kode pekerjaan
    Return:
        None
    '''
    listProd = []
    cariProd = readSpesifik2(iptKodePek)
    for i in cariProd:
        listProd.append(float(i[-1][:5]))
    
    aveProd = sum(listProd) / len(listProd)
    listHasil = ['AVE', f'{aveProd}\n{pekerjaan[iptKodePek][1]}/(org/hari)']

    if iptSubS == '1':
        # CARI JUMLAH PEKERJA
        helperSimulasi = [['','','OUTPUT', 'INPUT', 'INPUT', 'OUTPUT']]
        while True:
            try:
                iptVolumeS = float(input(f'Masukkan volume pekerjaan yang ingin dicapai ({pekerjaan[iptKodePek][1]}): '))
                if iptVolumeS <=0:
                    print('*** VOLUME PEKERJAAN HARUS BERNILAI BILANGAN POSITIF ***')
                else:
                    break
            except:
                print('*** VOLUME PEKERJAAN HARUS BERNILAI BILANGAN POSITIF ***')
        
        while True:
            try:
                iptHariS = int(input(f'Masukkan rencana waktu pengerjaan (DALAM BENTUK HARI, 1 HARI = 8 JAM KERJA): '))
                if iptHariS <=0:
                    print('*** RENCANA WAKTU PENGERJAAN HARUS BERNILAI BILANGAN BULAT POSITIF ***')
                else:
                    break
            except:
                print('*** RENCANA WAKTU PENGERJAAN HARUS BERNILAI BILANGAN BULAT POSITIF ***')
        
        pekerjaAwal = math.ceil(iptVolumeS/(aveProd * iptHariS))

        listHasil.append(f'{pekerjaAwal} orang')
        listHasil.append(f'{iptVolumeS} {pekerjaan[iptKodePek][1]}')
        listHasil.append(f'{iptHariS} Hari')
        listHasil.append(f'SIMULASI BERHASIL')
        print(f'---------------- HASIL SIMULASI UNTUK PEKERJAAN "{pekerjaan[iptKodePek][0]}" ---------------- ')
        print(tabulate(helperSimulasi + [listHasil], headerSimulasi, tablefmt="grid"))

    elif iptSubS == '2':
        # CARI VOLUME PEKERJAAN
        helperSimulasi = [['','','INPUT', 'OUTPUT', 'INPUT', 'OUTPUT']]
        while True:
            try:
                iptPekerjaS = int(input(f'Masukkan rencana jumlah pekerja: '))
                if iptPekerjaS <=0:
                    print('*** JUMLAH PEKERJA HARUS BERNILAI BILANGAN BULAT POSITIF ***')
                else:
                    break
            except:
                print('*** JUMLAH PEKERJA HARUS BERNILAI BILANGAN BULAT POSITIF ***')
        
        while True:
            try:
                iptHariS = int(input(f'Masukkan rencana waktu pengerjaan (DALAM BENTUK HARI, 1 HARI = 8 JAM KERJA): '))
                if iptHariS <=0:
                    print('*** RENCANA WAKTU PENGERJAAN HARUS BERNILAI BILANGAN BULAT POSITIF ***')
                else:
                    break
            except:
                print('*** RENCANA WAKTU PENGERJAAN HARUS BERNILAI BILANGAN BULAT POSITIF ***')
        
        volAwal = round(aveProd * iptPekerjaS * iptHariS,3)

        listHasil.append(f'{iptPekerjaS} orang')
        listHasil.append(f'{volAwal} {pekerjaan[iptKodePek][1]}')
        listHasil.append(f'{iptHariS} Hari')
        listHasil.append(f'SIMULASI BERHASIL')
        print(f'---------------- HASIL SIMULASI UNTUK PEKERJAAN "{pekerjaan[iptKodePek][0]}" ---------------- ')
        print(tabulate(helperSimulasi + [listHasil], headerSimulasi, tablefmt="grid"))

    elif iptSubS == '3':
        # CARI WAKTU PEKERJAAN
        helperSimulasi = [['','','INPUT', 'INPUT', 'OUTPUT', 'OUTPUT']]
        while True:
            try:
                iptPekerjaS = int(input(f'Masukkan rencana jumlah pekerja: '))
                if iptPekerjaS <=0:
                    print('*** JUMLAH PEKERJA HARUS BERNILAI BILANGAN BULAT POSITIF ***')
                else:
                    break
            except:
                print('*** JUMLAH PEKERJA HARUS BERNILAI BILANGAN BULAT POSITIF ***')

        while True:
            try:
                iptVolumeS = float(input(f'Masukkan volume pekerjaan yang ingin dicapai ({pekerjaan[iptKodePek][1]}): '))
                if iptVolumeS <=0:
                    print('*** VOLUME PEKERJAAN HARUS BERNILAI BILANGAN POSITIF ***')
                else:
                    break
            except:
                print('*** VOLUME PEKERJAAN HARUS BERNILAI BILANGAN POSITIF ***')
        
        waktuAwal = math.ceil(iptVolumeS/(aveProd * iptPekerjaS))

        listHasil.append(f'{iptPekerjaS} orang')
        listHasil.append(f'{iptVolumeS} {pekerjaan[iptKodePek][1]}')
        listHasil.append(f'{waktuAwal} Hari')
        listHasil.append(f'SIMULASI BERHASIL')
        print(f'---------------- HASIL SIMULASI UNTUK PEKERJAAN "{pekerjaan[iptKodePek][0]}" ---------------- ')
        print(tabulate(helperSimulasi + [listHasil], headerSimulasi, tablefmt="grid"))

    elif iptSubS == '4':
        # SIMULASI STATUS
        helperSimulasi = [['','','INPUT', 'INPUT', 'INPUT', 'OUTPUT']]
        while True:
            try:
                iptPekerjaS = int(input(f'Masukkan rencana jumlah pekerja: '))
                if iptPekerjaS <=0:
                    print('*** JUMLAH PEKERJA HARUS BERNILAI BILANGAN BULAT POSITIF ***')
                else:
                    break
            except:
                print('*** JUMLAH PEKERJA HARUS BERNILAI BILANGAN BULAT POSITIF ***')
        
        while True:
            try:
                iptVolumeS = float(input(f'Masukkan volume pekerjaan yang ingin dicapai ({pekerjaan[iptKodePek][1]}): '))
                if iptVolumeS <=0:
                    print('*** VOLUME PEKERJAAN HARUS BERNILAI BILANGAN POSITIF ***')
                else:
                    break
            except:
                print('*** VOLUME PEKERJAAN HARUS BERNILAI BILANGAN POSITIF ***')
        
        while True:
            try:
                iptHariS = int(input(f'Masukkan rencana waktu pengerjaan (DALAM BENTUK HARI, 1 HARI = 8 JAM KERJA): '))
                if iptHariS <=0:
                    print('*** RENCANA WAKTU PENGERJAAN HARUS BERNILAI BILANGAN BULAT POSITIF ***')
                else:
                    break
            except:
                print('*** RENCANA WAKTU PENGERJAAN HARUS BERNILAI BILANGAN BULAT POSITIF ***')
        
        # DARI SEGI PEKERJA
        pekerjaHarusnya = math.ceil(iptVolumeS/(aveProd * iptHariS))

        # DARI SEGI WAKTU
        waktuHarusnya = math.ceil(iptVolumeS/iptPekerjaS/aveProd)

        listHasil.append(f'{iptPekerjaS} orang')
        listHasil.append(f'{iptVolumeS} {pekerjaan[iptKodePek][1]}')
        listHasil.append(f'{iptHariS} Hari')
        if pekerjaHarusnya < iptPekerjaS or waktuHarusnya > iptHariS:
            status = f'SIMULASI GAGAL. Lakukan:\n1. Tambah pekerja menjadi {pekerjaHarusnya} org ATAU \n   tambah waktu pekerjaan menjadi {waktuHarusnya} hari\n2. Iterasi jumlah pekerja dan waktu ulang \n   pada sub-menu ini hingga simulasi berhasil'
        else:
            status = f'SIMULASI BERHASIL.'
        listHasil.append(status)
        print(f'---------------- HASIL SIMULASI UNTUK PEKERJAAN "{pekerjaan[iptKodePek][0]}" ---------------- ')
        print(tabulate(helperSimulasi + [listHasil], headerSimulasi, tablefmt="grid"))
    return

# =========================================================================== PROGRAM ===========================================================================
keluarProgram = False
keluarSubC = False


print('Selamat datang di aplikasi Database Hasil Pengamatan Lapangan Pekerjaan.') 
ketMenuUtama = '\nPilihan menu: \n1. Lihat data \n2. Tambahkan data \n3. Ubah data \n4. Hapus data \n5. Simulasi pekerjaan \n6. Keluar dari program'
print(ketMenuUtama)

# VARIABEL PILIHAN SUB-MENU UNTUK TIAP MENU
ketSubMenuR = '\nPilihan sub-menu Read: \n1. Lihat semua data pengamatan \n2. Lihat hanya 1 data pengamatan \n3. Lihat beberapa data pengamatan \n4. Lihat data penunjang data pekerjaan \n5. Lihat data penunjang data material \n6. Kembali ke menu utama \n7. Keluar dari program'
ketSubMenuC = '\nPilihan sub-menu Create: \n1. Tambah 1 data pengamatan \n2. Tambah beberapa data pengamatan \n3. Tambah data penunjang data pekerjaan \n4. Tambah data penunjang data material \n5. Kembali ke menu utama \n6. Keluar dari program'
ketSubMenuU = '\nPilihan sub-menu Update: \n1. Update data pengamatan \n2. Kembali ke menu utama \n3. Keluar dari program'
ketSubMenuD = '\nPilihan sub-menu Delete: \n1. Hapus 1 data pengamatan \n2. Hapus data pekerjaan pada data pengamatan \n3. Hapus seluruh data pengamatan \n4. Kembali ke menu utama \n5. Keluar dari program'
ketSubMenuS = '\nPilihan sub-menu Delete: \n1. Simulasi penentuan jumlah pekerja \n2. Simulasi penentuan volume pekerjaan \n3. Simulasi penentuan waktu pekerjaan \n4. Simulasi penentuan status pekerjaan \n5. Kembali ke menu utama \n6. Keluar dari program'

# LOOPINGAN TERLUAR
while True:
    inputMenu = input('Silakan masukkan pilihan menu: ')
    if inputMenu == '1':
        print('=============================================================== MENU READ ===============================================================')
        print('\nPilihan sub-menu Read: \n1. Lihat semua data pengamatan \n2. Lihat hanya 1 data pengamatan \n3. Lihat beberapa data pengamatan \n4. Lihat data penunjang data pekerjaan \n5. Lihat data penunjang data material \n6. Kembali ke menu utama \n7. Keluar dari program')
        while True:
            inputSubMenuR = input('Silakan masukkan pilihan sub-menu: ')
            if inputSubMenuR == '1':
                print('=============================================================== MENU READ ===============================================================')
                print('******************************************************** Seluruh Data Pengamatan ********************************************************')
                readFull()
                print(ketSubMenuR)
            elif inputSubMenuR == '2':
                print('=============================================================== MENU READ ===============================================================')
                print('********************************************************** Satu Data Pengamatan *********************************************************')
                r2 = True
                while r2 == True:
                    kodePengR = input('Silakan masukkan kode pengamatan: ')
                    subMenuR2 = readSpesifik(kodePengR)
                    if subMenuR2 == []:
                        print(f'------- TIDAK TERDAPAT DATA DENGAN KODE PENGAMATAN "{kodePengR}" -------')
                        while True:
                            r2ipt= input('Lakukan pencarian ulang? (y / n): ')
                            if r2ipt == 'n':
                                r2 = False
                                print('=============================================================== MENU READ ===============================================================')
                                print(ketSubMenuR)
                                break
                            elif r2ipt == 'y':
                                break
                            else:
                                print('Hanya menerima input (y / n)')
                    else:
                        print(f'Menampilkan data pengamatan dengan kode "{kodePengR}":\n{tabulate(subMenuR2, headerMain, tablefmt="grid")}')
                        while True:
                            r2ipt= input('Lakukan pencarian ulang? (y / n): ')
                            if r2ipt == 'n':
                                r2 = False
                                print('=============================================================== MENU READ ===============================================================')
                                print(ketSubMenuR)
                                break
                            elif r2ipt == 'y':
                                break
                            else:
                                print('Hanya menerima input (y / n)')
            elif inputSubMenuR == '3':
                print('=============================================================== MENU READ ===============================================================')
                print('******************************************************** Beberapa Data Pengamatan *******************************************************')
                r3 = True
                while r3 == True:
                    keywordsR = input('Silakan masukan keyword(s): ')
                    subMenuR3 = readSpesifik2(keywordsR)
                    if subMenuR3 == []:
                        print(f'------- TIDAK TERDAPAT DATA PENGAMATAN DENGAN KEYWORD(S) "{keywordsR}" -------')
                        while True:
                            r3ipt= input('Lakukan pencarian ulang? (y / n): ')
                            if r3ipt == 'n':
                                r3 = False
                                print('=============================================================== MENU READ ===============================================================')
                                print(ketSubMenuR)
                                break
                            elif r3ipt == 'y':
                                break
                            else:
                                print('Hanya menerima input (y / n)')
                    else:
                        print(f'Menampilkan data pengamatan dengan Keyword(s) "{keywordsR}":\n{tabulate(subMenuR3, headerMain, tablefmt="grid")}')
                        while True:
                            r3ipt= input('Lakukan pencarian ulang? (y / n): ')
                            if r3ipt == 'n':
                                r3 = False
                                print('=============================================================== MENU READ ===============================================================')
                                print(ketSubMenuR)
                                break
                            elif r3ipt == 'y':
                                break
                            else:
                                print('Hanya menerima input (y / n)')
            elif inputSubMenuR == '4':
                print('=============================================================== MENU READ ===============================================================')
                print('***************************************************** Data Penunjang Data Pekerjaan *****************************************************')
                readPekerjaan()
                print('=============================================================== MENU READ ===============================================================')
                print(ketSubMenuR)
            elif inputSubMenuR == '5':
                print('=============================================================== MENU READ ===============================================================')
                print('****************************************************** Data Penunjang Data Material *****************************************************')
                readMaterial()
                print('=============================================================== MENU READ ===============================================================')
                print(ketSubMenuR)
            elif inputSubMenuR == '6':
                print(ketMenuUtama)
                break
            elif inputSubMenuR == '7':
                print('********* TERIMA KASIH TELAH MENGGUNAKAN PROGRAM DATABASE PENGAMATAN PEKERJAAN *********')
                keluarProgram = True
                break
            else:
                print('*** PILIHAN SUB-MENU TIDAK TERSEDIA ***')

        if keluarProgram == True:
            break

    elif inputMenu == '2':
        print('=============================================================== MENU CREATE ===============================================================')
        print(ketSubMenuC)
        while True:
            inputSubMenuC = input('Silakan masukkan pilihan sub-menu: ')
            if inputSubMenuC == '1':
                print('=============================================================== MENU CREATE ===============================================================')
                print('******************************************************** Tambah 1 Data Pengamatan *********************************************************')
                print('----------------------- DATA PENUNJANG DATA PEKERJAAN -----------------------')
                readPekerjaan()
                iptKodePn = input('Masukkan kode pekerjaan: ').upper()
                while iptKodePn not in pekerjaan:
                    print(f'*** TIDAK TERDAPAT PEKERJAAN DENGAN KODE "{iptKodePn}" ***')
                    iptKodePn = input('Masukkan kode pekerjaan: ').upper()
                
                while True:
                    try:
                        iptPekerja = int(input('Masukkan jumlah pekerja: '))
                        if iptPekerja > 0:
                            break
                        else:
                            print('*** JUMLAH PEKERJA HARUS BILANGAN BULAT POSITIF ***')
                    except:
                        print('*** JUMLAH PEKERJA HARUS BILANGAN BULAT POSITIF ***')
                
                listMaterialCr = []
                print('Masukkan kuantitas material yang terpakai: ')
                for i in pekerjaan[iptKodePn][2]:
                    while True:
                        try:
                            materialCr = float(input(f'{material[i][0]} ({material[i][1]}): '))
                            if materialCr > 0:
                                break
                            else:
                                print('*** JUMLAH MATERIAL HARUS BILANGAN POSITIF ***')
                        except:
                            print('*** JUMLAH MATERIAL HARUS BILANGAN POSITIF ***')
                    
                    listMaterialCr.append(materialCr)
                    materialCr = 0
                
                while True:
                    print('CATATAN: untuk input waktu siklus pengamatan, pastikan penulisan: \n1. Format xxj xxm xxd (j untuk jam, m untuk menit, dan d untuk detik) \n2. Pastikan antar penanda waktu diberi pemisah BERUPA SPASI')
                    iptSiklus = input('Masukkan waktu siklus pengamatan: ')
                    c13 = True

                    listWaktu = iptSiklus.split()
                    for i in listWaktu:
                        if len(i) < 2 or i[:-1].isdigit() == False or i[-1] not in 'jmd':
                            c13 = False
                            break
                    if c13 == True:
                        try:
                            crSiklus = waktuKeJam(iptSiklus)
                            break
                        except:
                            print('*** FORMAT TIDAK SESUAI KAIDAH ***')
                    else:
                        print('*** FORMAT TIDAK SESUAI KAIDAH ***')
                
                while True:
                    try:
                        iptVolume = float(input('Masukkan volume pengamatan: '))
                        if iptVolume > 0:
                            break
                        else:
                            print('*** VOLUME PENGAMATAN HARUS BILANGAN POSITIF ***')
                    except:
                        print('*** VOLUME PENGAMATAN HARUS BILANGAN POSITIF ***')
                
                tambahSatu = createPengamatan(iptKodePn, iptPekerja, listMaterialCr, iptSiklus, iptVolume)

                while True:
                    yakinCr1 = input('Apakah Anda yakin untuk menambahkan data pengamatan diatas? (y / n): ')
                    if yakinCr1 == 'y':
                        pengamatan.update(tambahSatu)
                        print('-------------------- DATA PENGAMATAN BERHASIL DITAMBAHKAN --------------------')
                        readFull()
                        print(ketSubMenuC)
                        break
                    elif yakinCr1 == 'n':
                        print('-------------------- DATA PENGAMATAN TIDAK DITAMBAHKAN --------------------')
                        readFull()
                        print(ketSubMenuC)
                        break
                    else:
                        print('*** INPUTAN TIDAK VALID ***')
                
            elif inputSubMenuC == '2':
                print('=============================================================== MENU CREATE ===============================================================')
                print('*********************************************** Tambah Beberapa Data Pengamatan Sekaligus *************************************************')
                print('----------------------- DATA PENUNJANG DATA PEKERJAAN -----------------------')
                readPekerjaan()

                iptKodePn2 = input('Masukkan kode pekerjaan: ').upper()
                while iptKodePn2 not in pekerjaan:
                    print(f'*** TIDAK TERDAPAT PEKERJAAN DENGAN KODE "{iptKodePn2}" ***')
                    iptKodePn2 = input('Masukkan kode pekerjaan: ').upper()
                
                while True:
                    try:
                        iptBerapa2 = int(input('Berapa banyak data pengamatan yang ingin ditambahkan?: '))
                        if iptBerapa2 > 0:
                            break
                        else:
                            print('*** BANYAKNYA DATA HARUS BILANGAN BULAT POSITIF ***')
                    except:
                        print('*** BANYAKNYA DATA HARUS BILANGAN BULAT POSITIF ***')
                
                listPekerja2 = []
                for i in range(iptBerapa2):
                    while True:
                        try:
                            pekerja2 = int(input(f'Masukkan jumlah pekerja untuk pengamatan ke-{i+1}: '))
                            if pekerja2 > 0:
                                break
                            else:
                                print('*** JUMLAH PEKERJA HARUS BILANGAN BULAT POSITIF ***')
                        except:
                            print('*** JUMLAH PEKERJA HARUS BILANGAN BULAT POSITIF ***')
                    listPekerja2.append(pekerja2)
                    pekerja2 = 0
                
                listUrutKMat = pekerjaan[iptKodePn2][2]
                listUrutMat = []
                for i in listUrutKMat:
                    listUrutMat.append(f'{material[i][0]} ({material[i][1]})')
                
                strUrutMat = ', '.join(listUrutMat)

                print(f'URUTAN INPUT: {strUrutMat} \n')
                listMaterial2 = []
                for i in range(iptBerapa2):
                    while True:
                        materialList2 = input(f'Secara berurutan, masukkan material yang terpakai untuk pengamatan ke-{i+1}: ')
                        try:
                            materialList2Float = [float(i) for i in materialList2.split(', ')]
                            if len(materialList2Float) != len(listUrutKMat):
                                print(f'*** JUMLAH MATERIAL TIDAK SESUAI. DIBUTUHKAN {len(listUrutKMat)} DATA MATERIAL. ANDA MEMASUKKAN {len(materialList2Float)} DATA')
                            else:
                                listMaterial2.append(materialList2Float)
                                break
                        except:
                            print('*** JUMLAH MATERIAL HARUS BILANGAN POSITIF ***')
                    

                print('CATATAN: untuk input waktu siklus pengamatan, pastikan penulisan: \n1. Format xxj xxm xxd (j untuk jam, m untuk menit, dan d untuk detik) \n2. Pastikan antar penanda waktu diberi pemisah BERUPA SPASI')
                listSiklus = []
                for j in range(iptBerapa2):
                    while True:
                        iptSiklus = input(f'Masukkan waktu siklus pengamatan ke-{j+1}: ')
                        c22 = True

                        listWaktu = iptSiklus.split()
                        for i in listWaktu:
                            if len(i) < 2 or i[:-1].isdigit() == False or i[-1] not in 'jmd':
                                c22 = False
                                break
                        if c22 == True:
                            try:
                                crSiklus = waktuKeJam(iptSiklus)
                                break
                            except:
                                print('*** FORMAT TIDAK SESUAI KAIDAH ***')
                        else:
                            print('*** FORMAT TIDAK SESUAI KAIDAH ***')
                    listSiklus.append(iptSiklus)
                
                listVolume = []
                for i in range(iptBerapa2):
                    while True:
                        try:
                            iptVolume = float(input(f'Masukkan volume pengamatan ke-{i+1}: '))
                            if iptVolume > 0:
                                break
                            else:
                                print('*** VOLUME PENGAMATAN HARUS BILANGAN POSITIF ***')
                        except:
                            print('*** VOLUME PENGAMATAN HARUS BILANGAN POSITIF ***')
                    listVolume.append(iptVolume)
                
                tambahBanyak = createPengamatan2(iptBerapa2, iptKodePn2, listPekerja2, listMaterial2, listSiklus, listVolume)

                while True:
                    yakinCr2 = input('Apakah Anda yakin untuk menambahkan data pengamatan diatas? (y / n): ')
                    if yakinCr2 == 'y':
                        pengamatan.update(tambahBanyak)
                        print('-------------------- DATA PENGAMATAN BERHASIL DITAMBAHKAN --------------------')
                        readFull()
                        print(ketSubMenuC)
                        break
                    elif yakinCr2 == 'n':
                        print('-------------------- DATA PENGAMATAN TIDAK DITAMBAHKAN --------------------')
                        readFull()
                        print(ketSubMenuC)
                        break
                    else:
                        print('*** INPUTAN TIDAK VALID ***')

            elif inputSubMenuC == '3':
                print('=============================================================== MENU CREATE ===============================================================')
                print('************************************************** Tambah Data Penunjang Data Pekerjaan ***************************************************')
                print('----------------------- DATA PENUNJANG DATA PEKERJAAN -----------------------')
                readPekerjaan()
                print('KAIDAH PENAMAAN KODE PEKERJAAN:\n1. Harus unik (tidak boleh sama dengan kode pekerjaan lain) \n2. Diawali dengan SATU karakter alfabet dan diikuti dengan TIGA angka')
                while True:
                    iptKodePk = input('Masukkan kode pekerjaan yang ingin ditambahkan: ').upper()
                    if len(iptKodePk) != 4 or iptKodePk[0].isalpha == False or iptKodePk[1:].isnumeric == False:
                        print('*** PENAMAAN KODE PEKERJAAN TIDAK SESUAI KAIDAH ***')
                    elif iptKodePk in pekerjaan:
                        print('*** KODE PEKERJAAN YANG ANDA INPUT SUDAH DIGUNAKAN UNTUK PEKERJAAN LAIN ***')
                    else:
                        break
                
                iptNamaPk = input('Masukkan nama pekerjaan: ')
                iptSatuanPk = input('Masukkan satuan pekerjaan: ')

                listMaterialPk = []
                print('----------------------- DATA PENUNJANG DATA MATERIAL -----------------------')
                readMaterial()
                while True:
                    try:
                        brpMaterialPk = int(input('Berapa banyak jenis material yang dibutuhkan?: '))
                        break
                    except:
                        print('*** MASUKKAN BILANGAN BULAT POSITIF ***')
                for i in range(brpMaterialPk):
                    while True:
                        kodeMatPk = input(f'Masukkan kode material ke-{i+1}: ').upper()
                        if kodeMatPk not in material:
                            print(f'*** MATERIAL DENGAN KODE {kodeMatPk} TIDAK TERDAFTAR ***')
                        else:
                            listMaterialPk.append(kodeMatPk)
                            break
                
                tambahPk = createPekerjaan(iptKodePk, iptNamaPk, iptSatuanPk, listMaterialPk)

                while True:
                    yakinCr3 = input('Apakah Anda yakin untuk menambahkan data pekerjaan diatas? (y / n): ')
                    if yakinCr3 == 'y':
                        pekerjaan.update(tambahPk)
                        print('-------------------- DATA PEKERJAAN BERHASIL DITAMBAHKAN --------------------')
                        readPekerjaan()
                        print(ketSubMenuC)
                        break
                    elif yakinCr3 == 'n':
                        print('-------------------- DATA PEKERJAAN TIDAK DITAMBAHKAN --------------------')
                        readPekerjaan()
                        print(ketSubMenuC)
                        break
                    else:
                        print('*** INPUTAN TIDAK VALID ***')

            elif inputSubMenuC == '4':
                print('=============================================================== MENU CREATE ===============================================================')
                print('*************************************************** Tambah Data Penunjang Data Material ***************************************************')
                print('----------------------- DATA PENUNJANG DATA MATERIAL -----------------------')
                readMaterial()
                print('KAIDAH PENAMAAN KODE MATERIAL:\n1. Harus unik (tidak boleh sama dengan kode material lain) \n2. Diawali dengan SATU karakter alfabet dan diikuti dengan TIGA angka')
                while True:
                    iptKodeMat = input('Masukkan kode material yang ingin ditambahkan: ').upper()
                    if len(iptKodeMat) != 4 or iptKodeMat[0].isalpha == False or iptKodeMat[1:].isnumeric == False:
                        print('*** PENAMAAN KODE MATERIAL TIDAK SESUAI KAIDAH ***')
                    elif iptKodeMat in material:
                        print('*** KODE MATERIAL YANG ANDA INPUT SUDAH DIGUNAKAN UNTUK MATERIAL LAIN ***')
                    else:
                        break
                
                iptNamaMat = input('Masukkan nama material: ')
                iptSatuanMat = input('Masukkan satuan Material: ')

                while True:
                    yakinCr4 = input('Apakah Anda yakin untuk menambahkan data material diatas? (y / n): ')
                    if yakinCr4 == 'y':
                        material.update(tambahPk)
                        print('-------------------- DATA MATERIAL BERHASIL DITAMBAHKAN --------------------')
                        readMaterial()
                        print(ketSubMenuC)
                        break
                    elif yakinCr4 == 'n':
                        print('-------------------- DATA MATERIAL TIDAK DITAMBAHKAN --------------------')
                        readMaterial()
                        print(ketSubMenuC)
                        break
                    else:
                        print('*** INPUTAN TIDAK VALID ***')

            elif inputSubMenuC == '5':
                print(ketMenuUtama)
                break

            elif inputSubMenuC == '6':
                print('********* TERIMA KASIH TELAH MENGGUNAKAN PROGRAM DATABASE PENGAMATAN PEKERJAAN *********')
                keluarProgram = True
                break

            else:
                print('*** PILIHAN SUB-MENU TIDAK TERSEDIA ***')

        if keluarProgram == True:
            break
    
    elif inputMenu == '3':
        print('=============================================================== MENU UPDATE ===============================================================')
        print(ketSubMenuU)
        while True:
            inputSubMenuU = input('Masukkan pilihan sub-menu: ')
            if inputSubMenuU == '1':
                print('=============================================================== MENU UPDATE ===============================================================')
                print('********************************************************** Update Data Pengamatan *********************************************************')
                readFull()           
                while True:
                    iptKodeUp = input('Silakan masukkan kode pengamatan yang ingin di-update: ').upper()
                    if iptKodeUp not in pengamatan:
                        print(f'*** TIDAK DITEMUKAN PENGAMATAN DENGAN KODE {iptKodeUp} ***')
                    else:
                        break
                
                updPeng = readSpesifik(iptKodeUp)
                print(tabulate(helperUpdPengamatan + updPeng, headerMain, tablefmt="grid"))

                while True:
                    idCol = input('Masukkan id kolom yang ingin diubah: ')
                    if idCol not in '1234':
                        print('*** PILIHAN ID KOLOM HANYA 1, 2, 3, DAN 4 ***')
                    else:
                        break

                if idCol == '1':
                    while True:
                        try:
                            upBaru = int(input('Masukkan jumlah pekerja baru: '))
                            if upBaru > 0:
                                break
                            else:
                                print('*** JUMLAH PEKERJA HARUS BILANGAN BULAT POSITIF ***')
                        except:
                            print('*** JUMLAH PEKERJA HARUS BILANGAN BULAT POSITIF ***')
                    
                    updatePengamatan1(iptKodeUp, idCol, upBaru)
                    hasilUpdate31 = readSpesifik(iptKodeUp)
                    print(f'Menampilkan data pengamatan dengan kode "{iptKodeUp}":\n{tabulate(hasilUpdate31, headerMain, tablefmt="grid")}')
                    print(ketSubMenuU)

                elif idCol == '2':
                    for i, j, k in zip(range(len(pekerjaan[iptKodeUp[:4]][2])),pekerjaan[iptKodeUp[:4]][2], pengamatan[iptKodeUp][1]):
                        print(f'id = {i+1} --> {material[j][0]} (data awal = {k} {material[j][1]})')
                    
                    while True:
                        try:
                            idMat = int(input('Masukkan id. material yang ingin diubah: '))
                            if idMat > len(pekerjaan[iptKodeUp[:4]][2]) or idMat <= 0:
                                print('*** ID MATERIAL TIDAK ADA ***')
                            else:
                                break
                        except:
                            print('*** ID MATERIAL TIDAK ADA ***')
                    
                    for i,j,k in zip(range(len(pekerjaan[iptKodeUp[:4]][2])),pekerjaan[iptKodeUp[:4]][2], pengamatan[iptKodeUp][1]):
                        if idMat == i+1:
                            while True:
                                try:
                                    mBaru = float(input(f'Masukkan nilai material {material[j][0]} baru ({material[j][1]}): '))
                                    if mBaru <= 0:
                                        print('*** VOLUME MATERIAL HARUS BILANGAN POSITIF ***')
                                    else:
                                        break
                                except:
                                    print('*** VOLUME MATERIAL HARUS BILANGAN POSITIF ***')
                    
                    updatePengamatan2(iptKodeUp, mBaru, idMat)
                    hasilUpdate32 = readSpesifik(iptKodeUp)
                    print(f'Menampilkan data pengamatan dengan kode "{iptKodeUp}":\n{tabulate(hasilUpdate32, headerMain, tablefmt="grid")}')
                    print(ketSubMenuU)
                    
                elif idCol == '3':
                    while True:
                        print('CATATAN: untuk update waktu siklus pengamatan, pastikan penulisan: \n1. Format xxj xxm xxd (j untuk jam, m untuk menit, dan d untuk detik) \n2. Pastikan antar penanda waktu diberi pemisah BERUPA SPASI')
                        upSiklus = input('Masukkan waktu siklus pengamatan baru: ')
                        c31 = True

                        listWaktuUp = upSiklus.split()
                        for i in listWaktuUp:
                            if len(i) < 2 or i[:-1].isdigit() == False or i[-1] not in 'jmd':
                                c31 = False
                                break
                        if c31 == True:
                            try:
                                crSiklus = waktuKeJam(upSiklus)
                                break
                            except:
                                print('*** FORMAT TIDAK SESUAI KAIDAH ***')
                        else:
                            print('*** FORMAT TIDAK SESUAI KAIDAH ***')
                        
                    updatePengamatan1(iptKodeUp, idCol, upSiklus)
                    hasilUpdate33 = readSpesifik(iptKodeUp)
                    print(f'Menampilkan data pengamatan dengan kode "{iptKodeUp}":\n{tabulate(hasilUpdate33, headerMain, tablefmt="grid")}')
                    print(ketSubMenuU)

                elif idCol == '4':
                    while True:
                        try:
                            upVolume = float(input('Masukkan volume pengamatan baru: '))
                            if upVolume > 0:
                                break
                            else:
                                print('*** VOLUME PENGAMATAN HARUS BILANGAN POSITIF ***')
                        except:
                            print('*** VOLUME PENGAMATAN HARUS BILANGAN POSITIF ***')
                    updatePengamatan1(iptKodeUp, idCol, upVolume)
                    hasilUpdate34 = readSpesifik(iptKodeUp)
                    print(f'Menampilkan data pengamatan dengan kode "{iptKodeUp}":\n{tabulate(hasilUpdate34, headerMain, tablefmt="grid")}')
                    print(ketSubMenuU)
                else:
                    print('*** INPUTAN TIDAK VALID ***')

            elif inputSubMenuU == '2':
                print(ketMenuUtama)
                break
            elif inputSubMenuU == '3':
                print('********* TERIMA KASIH TELAH MENGGUNAKAN PROGRAM DATABASE PENGAMATAN PEKERJAAN *********')
                keluarProgram = True
                break
            else:
                print('*** PILIHAN SUB-MENU TIDAK TERSEDIA ***')
        
        if keluarProgram == True:
            break
    elif inputMenu == '4':
        print('=============================================================== MENU DELETE ===============================================================')
        print(ketSubMenuD)
        while True:
            inputSubMenuD = input('Masukkan pilihan sub-menu: ')
            if inputSubMenuD == '1':
                while True:
                    iptKodeDel = input('Silakan masukkan kode pengamatan yang ingin dihapus: ').upper()
                    if iptKodeDel not in pengamatan:
                        print(f'*** TIDAK DITEMUKAN PENGAMATAN DENGAN KODE {iptKodeDel} ***')
                    else:
                        break

                pengDel = readSpesifik2(iptKodeDel)
                print(f'Ditemukan data dengan kode {iptKodeDel}')
                print(tabulate(pengDel, headerMain, tablefmt="grid"))
                deletePengamatan(iptKodeDel)
                readFull()
                print(ketSubMenuD)

            elif inputSubMenuD == '2':
                while True:
                    iptKodePkDel = input('Silakan masukkan kode pekerjaan yang ingin dihapus: ').upper()
                    if iptKodePkDel not in pekerjaan:
                        print(f'*** TIDAK DITEMUKAN PEKERJAAN DENGAN KODE {iptKodePkDel} ***')
                    else:
                        break

                pengDelPk = readSpesifik2(iptKodePkDel)
                print(f'Ditemukan data dengan kode {iptKodePkDel}')
                print(tabulate(pengDelPk, headerMain, tablefmt="grid"))
                deletePengamatan2(iptKodePkDel)
                readFull()
                print(ketSubMenuD)
                
            elif inputSubMenuD == '3':
                deleteSemua()
                readFull()
                print(ketSubMenuD)

            elif inputSubMenuD == '4':
                print(ketMenuUtama)
                break

            elif inputSubMenuD == '5':
                print('********* TERIMA KASIH TELAH MENGGUNAKAN PROGRAM DATABASE PENGAMATAN PEKERJAAN *********')
                keluarProgram = True
                break

            else:
                print('*** PILIHAN SUB-MENU TIDAK TERSEDIA ***')
        
        if keluarProgram == True:
            break

    elif inputMenu == '5':
        print('=============================================================== MENU SIMULASI ===============================================================')
        print(ketSubMenuS)
        while True:
            inputSubMenuS = input('Masukkan pilihan sub-menu: ')
            if inputSubMenuS == '1' or inputSubMenuS == '2' or inputSubMenuS == '3' or inputSubMenuS == '4':
                readPekerjaan()
                while True:
                    iptKodeSim = input('Silakan masukkan kode pekerjaan yang ingin disimulasi: ').upper()
                    if iptKodeSim not in pekerjaan:
                        print(f'*** TIDAK DITEMUKAN PEKERJAAN DENGAN KODE {iptKodeSim} ***')
                    else:
                        break
                
                simulasi(inputSubMenuS, iptKodeSim)
                print('=============================================================== MENU SIMULASI ===============================================================')
                print(ketSubMenuS)

            elif inputSubMenuS == '5':
                print(ketMenuUtama)
                break

            elif inputSubMenuS == '6':
                print('********** TERIMA KASIH TELAH MENGGUNAKAN PROGRAM DATABASE PENGAMATAN PEKERJAAN *********')
                keluarProgram = True
                break

            else:
                print('*** PILIHAN SUB-MENU TIDAK TERSEDIA ***')
        
        if keluarProgram == True:
            break

    elif inputMenu == '6':
        print('********* TERIMA KASIH TELAH MENGGUNAKAN PROGRAM DATABASE PENGAMATAN PEKERJAAN *********')
        break

    else:
        print('***PILIHAN MENU TIDAK TERSEDIA***')