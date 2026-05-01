import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django.setup()

from antrian.models import Poli, Dokter

polis = [
    'Poli Umum',
    'Poli Kesehatan Ibu dan Anak (KIA)',
    'Poli Penyakit Dalam (Internist)',
    'Poli Anak (Pediatri)',
    'Poli Kebidanan & Kandungan (Obgyn)',
    'Poli Bedah Umum',
    'Poli Mata',
    'Poli THT-KL',
    'Poli Gigi & Mulut',
    'Poli Kulit & Kelamin (Dermatologi)',
    'Poli Saraf (Neurologi)',
    'Poli Jantung (Kardiologi)',
    'Poli Jiwa (Psikiatri)',
    'Poli Gizi',
    'Poli Orthopedi'
]

for p in polis:
    poli_obj, created = Poli.objects.get_or_create(
        nama=p, 
        defaults={'deskripsi': f'Layanan medis dan konsultasi profesional untuk {p}.'}
    )
    
    # Extract specialty name for the mock doctor
    specialty = p.replace('Poli ', '').split('(')[0].strip()
    Dokter.objects.get_or_create(
        nama=f'Dr. {specialty} Utama',
        poli=poli_obj,
        defaults={'jadwal': 'Senin - Jumat, 08:00 - 15:00'}
    )

print("Data Poli dan Dokter berhasil di-seed!")
