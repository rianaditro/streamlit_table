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
    minutes TEXT,
    hms TEXT,
    calls TEXT,
    reject TEXT,
    failed TEXT,
    coffs TEXT,
    smses TEXT,
    asr TEXT
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
    calls TEXT,
    reject TEXT,
    failed TEXT,
    coffs TEXT,
    smses TEXT,
    asr TEXT
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
    ip_address TEXT
)
''')

# Membuat tabel
c.execute('''
CREATE TABLE IF NOT EXISTS module_ge_table (
    upload_id INTEGER,
    upload_datetime TEXT,
    upload_ip TEXT,
    mobile_port TEXT,
    port_status TEXT,
    signal_strenght TEXT,
    call_duration TEXT,
    dialed_calls TEXT,
    successfull_calls TEXT,
    asr TEXT,
    acd TEXT,
    allocated_ammount TEXT,
    consumed_amount TEXT
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS asr_value (
    asr_value INTEGER,
    id INTEGER PRIMARY_KEY
)
''')

c.execute('''
INSERT INTO asr_value (
    asr_value, id)
    VALUES (30, 1)
''')

# Menyimpan perubahan
conn.commit()

# Menutup koneksi
conn.close()

print("Database dan tabel berhasil dibuat.")