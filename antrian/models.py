from django.db import models
from django.utils import timezone

class Poli(models.Model):
    nama = models.CharField(max_length=100)
    deskripsi = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nama

class Dokter(models.Model):
    nama = models.CharField(max_length=100)
    poli = models.ForeignKey(Poli, on_delete=models.CASCADE, related_name='dokter')
    jadwal = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.nama} - {self.poli.nama}"

class Pasien(models.Model):
    nama = models.CharField(max_length=100)
    nik = models.CharField(max_length=16, unique=True)
    no_rekam_medis = models.CharField(max_length=20, unique=True, blank=True, null=True)
    no_telepon = models.CharField(max_length=15)
    alamat = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.no_rekam_medis:
            super().save(*args, **kwargs)
            self.no_rekam_medis = f"RM-{self.id:06d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nama

class Antrian(models.Model):
    STATUS_CHOICES = (
        ('Menunggu', 'Menunggu'),
        ('Diperiksa', 'Diperiksa'),
        ('Selesai', 'Selesai'),
        ('Batal', 'Batal'),
    )
    pasien = models.ForeignKey(Pasien, on_delete=models.CASCADE, related_name='antrian')
    poli = models.ForeignKey(Poli, on_delete=models.CASCADE)
    dokter = models.ForeignKey(Dokter, on_delete=models.CASCADE)
    tanggal = models.DateField()
    waktu_kunjungan = models.TimeField(null=True, blank=True)
    nomor_antrian = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Menunggu')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('poli', 'tanggal', 'nomor_antrian')
        ordering = ['tanggal', 'poli', 'nomor_antrian']

    def __str__(self):
        return f"Antrian {self.nomor_antrian} - {self.poli.nama} ({self.tanggal})"

    @classmethod
    def generate_nomor_antrian(cls, poli, tanggal):
        last_antrian = cls.objects.filter(poli=poli, tanggal=tanggal).order_by('nomor_antrian').last()
        if last_antrian:
            return last_antrian.nomor_antrian + 1
        return 1
