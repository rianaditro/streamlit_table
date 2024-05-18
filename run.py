import sqlite3

# Membuat atau menghubungkan ke database
conn = sqlite3.connect('main.sqlite')

# Membuat cursor
c = conn.cursor()

# Membuat tabel
c.execute('''
CREATE TABLE IF NOT EXISTS module_32_table (
    upload_id INTEGER,
    upload_datetime TEXT,
    upload_ip TEXT,
    module TEXT,
    sim TEXT,
    net TEXT,
    grp TEXT,
    minutes TEXT,
    hms TEXT,
    calls INTEGER,
    reject TEXT,
    failed INTEGER,
    coffs TEXT,
    smses TEXT,
    asr FLOAT
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS module_4_table (
    upload_id INTEGER,
    upload_datetime TEXT,
    upload_ip TEXT,
    module TEXT,
    '-' TEXT,
    reset TEXT,
    minutes TEXT,
    hms TEXT,
    calls INTEGER,
    reject INTEGER,
    failed INTEGER,
    coffs TEXT,
    smses TEXT,
    asr FLOAT
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS perangkat_table (
    nama_perangkat TEXT,
    ip_address TEXT PRIMARY_KEY,
    tipe_perangkat TEXT
    
)
''')


c.execute('''
CREATE TABLE IF NOT EXISTS history_upload (
    upload_id INTEGER PRIMARY_KEY,
    upload_datetime TEXT,
    ip_address TEXT,
    data TEXT
    
)
''')

# Menyimpan perubahan
conn.commit()

# Menutup koneksi
conn.close()

print("Database dan tabel berhasil dibuat.")