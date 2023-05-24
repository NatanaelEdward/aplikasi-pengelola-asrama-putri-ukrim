from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.models import User
from django.http import Http404
from django.contrib.auth.decorators import login_required
from .models import Mahasiswas, Kamars, Pengelolas, Pendaftarans
from django.contrib import messages
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.conf import settings
import os
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from django_datatables_view.base_datatable_view import BaseDatatableView

class PendaftaranJson(BaseDatatableView):
    model = Pendaftarans
    columns = ['id', 'nim', 'tanggal_daftar', 'tanggal_masuk', 'tanggal_keluar', 'bukti_bayar']

    def render_column(self, row, column):
        # Customize rendering of specific columns if needed
        if column == 'bukti_bayar':
            if row.bukti_bayar:
                return '<img src="{}" style="width: 50%; height: auto;" alt="Bukti Bayar">'.format(row.bukti_bayar.url)
            else:
                return 'Bukti Bayar Belum di Upload.'
        return super().render_column(row, column)

    def filter_queryset(self, qs):
        # Apply custom filtering if needed
        search_value = self.request.GET.get('search[value]')
        if search_value:
            qs = qs.filter(nim__icontains=search_value)  # Example: Filtering based on 'nim' field
        return qs

def generate_pdf(mahasiswa_queryset):
    # Create the PDF document
    pdf = SimpleDocTemplate("mahasiswa_report.pdf", pagesize=letter)

    # Set up the data for the table
    table_data = [["NIM", "Nama", "Jurusan"]]
    for mahasiswa in mahasiswa_queryset:
        table_data.append([mahasiswa.nim, mahasiswa.nama, mahasiswa.jurusan])
    
    # Define the table style
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ])

    # Create the table and apply the style
    table = Table(table_data)
    table.setStyle(table_style)

    # Build the PDF document with the table
    elements = [table]
    pdf.build(elements)

def mahasiswa_report_view(request):
    mahasiswa_queryset = Mahasiswas.objects.all()
    generate_pdf(mahasiswa_queryset)
    
    # Prepare the response with the PDF file
    with open("mahasiswa_report.pdf", 'rb') as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="mahasiswa_report.pdf"'

    return response

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'accounts/login.html', {'error': 'Invalid login credentials.'})
    else:
        return render(request, 'accounts/login.html')


def create_user(username, password):
    user = User.objects.create_user(username=username, password=password)
    return user


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    current_user = request.user
    data_pengelola = Pengelolas.objects.filter(user=current_user)
    context = {
        'data_pengelola': data_pengelola
    }
    return render(request, 'dashboard.html',context)

@login_required
def profil(request):
    return render(request,'pengelola/profil.html')

@login_required
def log(request):
    return render(request,'log/index.html')

@login_required
def upload_image(request):
    if request.method == 'POST' and request.FILES['bukti_bayar']:
        file = request.FILES['bukti_bayar']
        # Save the file to your database
        pendaftaran = Pendaftarans.objects.get(id=request.POST.get('id_pendaftaran'))
        pendaftaran.bukti_bayar = file
        pendaftaran.save()
        # Return a success response
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'failed'})


# View Mahasiswa


@login_required
def indexMahasiswa(request):
    data_mahasiswa = Mahasiswas.objects.all().select_related('nomor_kamar')
    
    context = {
        'data_mahasiswa': data_mahasiswa
    }
    return render(request, 'mahasiswa/index.html', context)


@login_required
def tambahMahasiswa(request):
    mahasiswa = Mahasiswas()
    kamars = Kamars.objects.filter(status_kamar='Tersedia')

    context = {
        'mahasiswa': mahasiswa,
        'kamars': kamars,
    }

    return render(request, 'mahasiswa/formTambah.html', context)


# when inserting mahasiswa, pendaftaran also set
@login_required
def postMahasiswa(request):
    if request.method == 'POST':
        nim = request.POST.get('nim')
        nama = request.POST.get('nama')
        jurusan = request.POST.get('jurusan')
        no_telepon = request.POST.get('no_telepon')
        tempat_lahir = request.POST.get('tempat_lahir')
        tanggal_lahir_str = request.POST.get('tanggal_lahir')
        tanggal_lahir = datetime.strptime(
            tanggal_lahir_str, '%Y-%m-%d').date()
        nomor_kamar_id = request.POST.get('nomor_kamar')

        try:
            if Mahasiswas.objects.filter(nim=nim).exists():
                messages.error(
                    request, 'Mahasiswa dengan NIM {} sudah terdaftar'.format(nim))
                return redirect('tambahMahasiswa')

            new_mahasiswa = Mahasiswas(nim=nim, nama=nama, jurusan=jurusan,
                                       no_telepon=no_telepon, tanggal_lahir=tanggal_lahir, tempat_lahir=tempat_lahir)
            if nomor_kamar_id:
                nomor_kamar = Kamars.objects.get(pk=nomor_kamar_id)
                new_mahasiswa.nomor_kamar = nomor_kamar
                nomor_kamar.status_kamar = 'Terpakai'
                nomor_kamar.mahasiswa_id = nim
                nomor_kamar.save()

            new_mahasiswa.save()

            # Set pengelola field as current user
            pengelola = Pengelolas.objects.get(user=request.user)

            pendaftaran = Pendaftarans(
                tanggal_daftar=datetime.now(),
                nim=new_mahasiswa,
                pengelola=pengelola)
            pendaftaran.save()
            messages.success(
                request, 'Mahasiswa dengan NIM {} berhasil ditambahkan'.format(nim))
            return redirect('mahasiswa')
        except Exception as e:
            messages.error(
                request, 'Terjadi kesalahan saat menambahkan mahasiswa: {}'.format(str(e)))
            return redirect('tambahMahasiswa')
    else:
        messages.error(
            request, 'Terjadi kesalahan saat menambahkan mahasiswa: {}'.format(str(e)))


@login_required
def updateMahasiswa(request, nim):
    data_mahasiswa = Mahasiswas.objects.get(nim=nim)
    data_kamar = Kamars.objects.filter(status_kamar='Tersedia')
    context = {
        'data_mahasiswa': data_mahasiswa,
        'data_kamar': data_kamar,
    }
    return render(request, 'mahasiswa/formUpdate.html', context)


@login_required
def postUpdateMahasiswa(request):
    if request.method == 'POST':
        nim = request.POST.get('nim')
        nama = request.POST.get('nama')
        jurusan = request.POST.get('jurusan')
        no_telepon = request.POST.get('no_telepon')
        tempat_lahir = request.POST.get('tempat_lahir')
        tanggal_lahir_str = request.POST.get('tanggal_lahir')
        tanggal_lahir = datetime.strptime(tanggal_lahir_str, '%Y-%m-%d').date()
        metode_pembayaran = request.POST.get('metode_pembayaran')
        nomor_kamar = request.POST.get('nomor_kamar')

        try:
            mahasiswa = Mahasiswas.objects.get(nim=nim)
            kamar = None
            if nomor_kamar:
                kamar = Kamars.objects.get(nomor_kamar=nomor_kamar)

            mahasiswa.nama = nama
            mahasiswa.jurusan = jurusan
            mahasiswa.no_telepon = no_telepon
            mahasiswa.tempat_lahir = tempat_lahir
            mahasiswa.tanggal_lahir = tanggal_lahir
            mahasiswa.nomor_kamar = kamar
            mahasiswa.save()

            messages.success(
                request, 'Data mahasiswa dengan NIM {} berhasil diperbarui'.format(nim))
            return redirect('mahasiswa')

        except Exception as e:
            messages.error(
                request, 'Terjadi kesalahan saat memperbarui data mahasiswa: {}'.format(str(e)))
            return redirect('updateMahasiswa', nim=nim)
    else:
        return redirect('mahasiswa')

@login_required
def hapusMahasiswa(request, nim):
    data_mahasiswa = Mahasiswas.objects.get(nim=nim)
    context = {
        'data_mahasiswa': data_mahasiswa
    }
    return render(request, 'mahasiswa/formDelete.html', context)

@login_required
def postHapusMahasiswa(request, nim):
    mahasiswa = Mahasiswas.objects.get(nim=nim)
    mahasiswa.delete()
    return redirect('mahasiswa')

# View Pengelola


@login_required
def indexPengelola(request):
    User = get_user_model()
    current_user = request.user
    data_pengelola = Pengelolas.objects.filter(user=current_user)
    context = {
        'data_pengelola': data_pengelola
    }
    return render(request, 'pengelola/profil.html', context)


@login_required
def tambahPengelola(request):
    try:
        pengelola = Pengelolas.objects.get(user=request.user)
    except Pengelolas.DoesNotExist:
        pengelola = Pengelolas(user=request.user)

    context = {
        'pengelola': pengelola,
    }
    return render(request, 'pengelola/formTambah.html', context)


@login_required
def postPengelola(request):
    if request.method == 'POST':
        try:
            pengelola = Pengelolas.objects.get(user=request.user)
        except Pengelolas.DoesNotExist:
            pengelola = Pengelolas(user=request.user)

        pengelola.nama = request.POST.get('nama')
        pengelola.tanggal_lahir = request.POST.get('tanggal_lahir')
        pengelola.alamat = request.POST.get('alamat')
        pengelola.no_telepon = request.POST.get('no_telepon')
        pengelola.save()
        messages.success(
            request, 'Data pengelola berhasil disimpan')
        return redirect('pengelola')
    else:
        messages.error(
            request, 'Terjadi kesalahan saat menyimpan data pengelola')
        return redirect('tambahPengelola')

@login_required
def postUpdatePengelola(request):
    id_pengelola = request.POST.get('id_pengelola')
    nama = request.POST.get('nama')
    tanggal_lahir_str = request.POST.get('tanggal_lahir')
    tanggal_lahir = datetime.strptime(tanggal_lahir_str, '%Y-%m-%d').date()
    alamat = request.POST.get('alamat')
    no_telepon = request.POST.get('no_telepon')

    pengelola = Pengelolas.objects.get(id_pengelola=id_pengelola)

    pengelola.nama = nama
    pengelola.tanggal_lahir = tanggal_lahir
    pengelola.alamat = alamat
    pengelola.no_telepon = no_telepon

    pengelola.save()
    return redirect('pengelola')

@login_required
def hapusPengelola(request, id_pengelola):
    data_pengelola = Pengelolas.objects.get(id_pengelola=id_pengelola)
    context = {
        'data_pengelola': data_pengelola
    }
    return render(request, 'pengelola/formDelete.html', context)

@login_required
def postHapusPengelola(request, id_pengelola):
    pengelola = Pengelolas.objects.get(id_pengelola=id_pengelola)
    pengelola.delete()
    return redirect('pengelola')

@login_required
def updatePengelola(request):
    # data_pengelola = Pengelolas.objects.get(id_pengelola=id_pengelola)
    # context = {
    #     'data_pengelola': data_pengelola
    # }
    return render(request, 'pengelola/formUpdate.html')

# View Pendaftaran


#to do: current user's pengelola name to pendaftaran

@login_required
def indexPendaftaran(request):
    if request.method == 'GET':
        current_user = request.user
        data_pendaftaran = Pendaftarans.objects.all().select_related('nim')
        data_pengelola = Pengelolas.objects.get(user=current_user)
        data_pengelola.save()
        context = {
            'data_pengelola': data_pengelola,
            'data_pendaftaran': data_pendaftaran
        }
        
        return render(request, 'pendaftaran/index.html', context)

@login_required
def updatePendaftaran(request, id_pendaftaran):
    data_pendaftaran = Pendaftarans.objects.get(id_pendaftaran=id_pendaftaran)
    context = {
        'data_pendaftaran': data_pendaftaran
    }
    return render(request, 'pendaftaran/formUpdate.html', context)

@login_required
def postUpdatePendaftaran(request):
    id_pendaftaran = request.POST.get('id_pendaftaran')
    tanggal_daftar_str = request.POST.get('tanggal_daftar')
    tanggal_daftar = datetime.strptime(
        tanggal_daftar_str, '%Y-%m-%d').date() if tanggal_daftar_str else None
    tanggal_masuk_str = request.POST.get('tanggal_masuk')
    tanggal_masuk = datetime.strptime(
        tanggal_masuk_str, '%Y-%m-%d').date() if tanggal_masuk_str else None
    tanggal_keluar_str = request.POST.get('tanggal_keluar')
    tanggal_keluar = datetime.strptime(
        tanggal_keluar_str, '%Y-%m-%d').date() if tanggal_keluar_str else None
    bukti_bayar = request.FILES.get('bukti_bayar')

    try:
        pendaftaran = Pendaftarans.objects.get(id_pendaftaran=id_pendaftaran)
    except Pendaftarans.DoesNotExist:
        raise Http404("Pendaftarans matching query does not exist.")

    pendaftaran.tanggal_daftar = tanggal_daftar
    pendaftaran.tanggal_masuk = tanggal_masuk if tanggal_masuk else None
    pendaftaran.tanggal_keluar = tanggal_keluar if tanggal_keluar else None
    

    if bukti_bayar is not None:
        # Check if a new file is provided
        if pendaftaran.bukti_bayar:
            # If the existing file exists, delete it
            Pendaftarans.delete(pendaftaran.bukti_bayar.name)

        # Save the new file
        pendaftaran.bukti_bayar.save(bukti_bayar.name, bukti_bayar)
    else:
        # If no new file is provided, keep the existing file
        bukti_bayar_existing = pendaftaran.bukti_bayar
        pendaftaran.bukti_bayar = bukti_bayar_existing

    pendaftaran.save()

    return redirect('pendaftaran')

# View Kamar


@login_required
def indexKamar(request):
    data_kamar = Kamars.objects.all().prefetch_related('mahasiswas_set').order_by('nomor_kamar')

    for kamar in data_kamar:
        is_terpakai = False
        for mahasiswa in kamar.mahasiswas_set.all():
            if mahasiswa.nomor_kamar == kamar:
                is_terpakai = True
                break
        if is_terpakai:
            kamar.status_kamar = 'Terpakai'
        else:
            kamar.status_kamar = 'Tersedia'
        kamar.save()

    context = {
        'data_kamar': data_kamar,
    }

    return render(request, 'kamar/index.html', context)


@login_required
def updateKamar(request, nomor_kamar):
    data_kamar = Kamars.objects.get(nomor_kamar=nomor_kamar)
    context = {
        'data_kamar': data_kamar
    }

    return render(request, 'kamar/formUpdate.html', context)


@login_required
def postUpdateKamar(request):
    nomor_kamar = request.POST.get('nomor_kamar')
    status_kamar = request.POST.get('status_kamar')
    data_kamar = Kamars.objects.get(nomor_kamar=nomor_kamar)

    data_kamar.status_kamar = status_kamar

    data_kamar.save()

    return redirect('kamar')


@login_required
def tambahKamar(request):
    data_kamar = Kamars()
    context = {
        'data_kamar': data_kamar
    }
    return render(request, 'kamar/formTambah.html', context)


@login_required
def postKamar(request):
    last_kamar = Kamars.objects.last()
    if last_kamar:
        nomor_kamar = last_kamar.nomor_kamar + 1
    else:
        nomor_kamar = 1

    new_kamar = Kamars(nomor_kamar=nomor_kamar, status_kamar='Tersedia')
    new_kamar.save()

    return redirect('kamar')

@login_required
def hapusKamar(request, nomor_kamar):
    data_kamar = Kamars.objects.get(nomor_kamar=nomor_kamar)
    context = {
        'data_kamar': data_kamar
    }
    return render(request, 'kamar/formDelete.html', context)

@login_required
def postHapusKamar(request, nomor_kamar):
    kamar = Kamars.objects.get(nomor_kamar=nomor_kamar)
    kamar.delete()
    return redirect('kamar')
