from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from .models import Poli, Dokter, Pasien, Antrian

def login_pasien(request):
    if request.method == 'POST':
        nik = request.POST.get('nik')
        pasien = Pasien.objects.filter(nik=nik).first()
        if pasien:
            request.session['pasien_id'] = pasien.id
            messages.success(request, f'Selamat datang kembali, {pasien.nama}!')
            return redirect('beranda')
        else:
            messages.error(request, 'NIK tidak ditemukan. Silakan daftar terlebih dahulu.')
            return redirect('register_pasien')
    return render(request, 'antrian/login.html')

def register_pasien(request):
    if request.method == 'POST':
        nik = request.POST.get('nik')
        nama = request.POST.get('nama')
        no_telepon = request.POST.get('no_telepon') or request.POST.get('no_hp', '')
        
        if Pasien.objects.filter(nik=nik).exists():
            messages.warning(request, 'NIK sudah terdaftar. Silakan login.')
            return redirect('login_pasien')
            
        pasien = Pasien.objects.create(nik=nik, nama=nama, no_telepon=no_telepon)
        request.session['pasien_id'] = pasien.id
        messages.success(request, 'Pendaftaran berhasil. Silakan ambil antrian.')
        return redirect('beranda')
    return render(request, 'antrian/register.html')

def logout_pasien(request):
    if 'pasien_id' in request.session:
        del request.session['pasien_id']
    messages.success(request, 'Anda telah keluar.')
    return redirect('login_pasien')

def beranda(request):
    polis = Poli.objects.all()
    today = timezone.localdate()
    total_antrian_hari_ini = Antrian.objects.filter(tanggal=today).count()
    
    context = {
        'polis': polis,
        'total_antrian': total_antrian_hari_ini
    }
    
    if 'pasien_id' in request.session:
        pasien = Pasien.objects.filter(id=request.session['pasien_id']).first()
        context['pasien'] = pasien
        
    return render(request, 'antrian/beranda.html', context)

def ambil_antrian(request):
    if 'pasien_id' not in request.session:
        messages.warning(request, 'Silakan login terlebih dahulu untuk mengambil antrian.')
        return redirect('login_pasien')
        
    pasien = get_object_or_404(Pasien, id=request.session['pasien_id'])

    if request.method == 'POST':
        poli_id = request.POST.get('poli')
        dokter_id = request.POST.get('dokter')
        tanggal_str = request.POST.get('tanggal')
        waktu = request.POST.get('waktu_kunjungan')

        if not all([poli_id, dokter_id, tanggal_str, waktu]):
            messages.error(request, 'Semua kolom harus diisi.')
            return redirect('ambil_antrian')
            
        poli = get_object_or_404(Poli, pk=poli_id)
        dokter = get_object_or_404(Dokter, pk=dokter_id)
        
        # Save order details in session to confirm later
        request.session['temp_antrian'] = {
            'poli_id': poli_id,
            'dokter_id': dokter_id,
            'tanggal': tanggal_str,
            'waktu': waktu
        }
        return redirect('konfirmasi_antrian')

    polis = Poli.objects.all()
    dokters = Dokter.objects.all()
    return render(request, 'antrian/ambil_antrian.html', {'polis': polis, 'dokters': dokters, 'pasien': pasien})

def konfirmasi_antrian(request):
    if 'pasien_id' not in request.session or 'temp_antrian' not in request.session:
        return redirect('ambil_antrian')
        
    pasien = get_object_or_404(Pasien, id=request.session['pasien_id'])
    temp = request.session['temp_antrian']
    poli = get_object_or_404(Poli, pk=temp['poli_id'])
    dokter = get_object_or_404(Dokter, pk=temp['dokter_id'])
    
    if request.method == 'POST':
        # Create Antrian
        nomor_antrian = Antrian.generate_nomor_antrian(poli, temp['tanggal'])
        antrian = Antrian.objects.create(
            pasien=pasien,
            poli=poli,
            dokter=dokter,
            tanggal=temp['tanggal'],
            waktu_kunjungan=temp['waktu'],
            nomor_antrian=nomor_antrian
        )
        del request.session['temp_antrian']
        messages.success(request, 'Antrian berhasil diambil.')
        return redirect('status_antrian', antrian_id=antrian.id)
        
    return render(request, 'antrian/konfirmasi_antrian.html', {
        'pasien': pasien,
        'poli': poli,
        'dokter': dokter,
        'tanggal': temp['tanggal'],
        'waktu': temp['waktu']
    })

def status_antrian(request, antrian_id):
    antrian = get_object_or_404(Antrian, id=antrian_id)
    return render(request, 'antrian/status.html', {'antrian': antrian})

def daftar_antrian(request):
    today = timezone.localdate()
    # List polyclinics and their queues today
    antrian_hari_ini = Antrian.objects.filter(tanggal=today).order_by('poli', 'nomor_antrian')
    return render(request, 'antrian/daftar.html', {'antrian_list': antrian_hari_ini, 'tanggal': today})
