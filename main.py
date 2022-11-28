#import library
from ast import pattern
from flask import Flask, render_template, request, redirect, url_for, flash, redirect, request, session, flash
from auth import login
from flask_mysqldb import MySQL
import mysql.connector


#inisiasi object flask
application = Flask(__name__)
application.secret_key = "wiro212sableng"

def getMysqlConnection():
    return mysql.connector.connect(user='root', host='localhost', port='3306', password='', database='perpustakaan')

@application.route('/')
@application.route('/beranda/')
def beranda():
    return render_template('/home/beranda.html')

@application.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] != '181910203' and request.form['password'] != 'nurul@26':
            flash('Invalid username/password','danger')
        else:
            session ['logged_in'] = True
            flash('Login successful','success')
            return redirect(url_for('index'))
    return render_template('/home/login.html')

@application.route('/register/')
def register():
    return render_template('/home/register.html')

@application.route('/profile/')
def profile():
    return render_template('/home/profile.html')

# untuk loginadmin
@application.route('/loginadmin/', methods=['GET', 'POST'])
def loginadmin():
    if request.method == 'POST':
        if request.form['username'] != 'admin' and request.form['password'] != 'pnj21':
            flash('Invalid username/password','danger')
        else:
            session ['logged_in'] = True
            flash('Login successful','success')
            return redirect(url_for('indexadmin'))
    return render_template('/home/loginadmin.html')

# untuk logout
@application.route('/logout/')
def logout():
    session.pop('logged_in', None)
    flash('Logout successful','success')
    return redirect(url_for('login'))

@application.route('/index/')
def index():
    db = getMysqlConnection()
    try:
        sqlstr = "SELECT * from peminjaman"
        cur = db.cursor()
        cur.execute(sqlstr)
        output_json = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return render_template('/home/index.html', datapinjam = output_json)

# untuk daftar buku user
@application.route('/daftarbuku/')
def daftarbuku():
    db = getMysqlConnection()
    try:
        sqlstr = "SELECT * from buku"
        cur = db.cursor()
        cur.execute(sqlstr)
        output_json = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return render_template('/home/daftarbuku.html', databuku = output_json)

@application.route('/meminjam/')
def meminjam():
    db = getMysqlConnection()
    try:
        sqlstr = "SELECT * from peminjaman"
        cur = db.cursor()
        cur.execute(sqlstr)
        output_json = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return render_template('/home/meminjam.html', datapinjam = output_json)

@application.route('/mengembalikan/')
def mengembalikan():
    db = getMysqlConnection()
    try:
        sqlstr = "SELECT * from pengembalian"
        cur = db.cursor()
        cur.execute(sqlstr)
        output_json = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return render_template('/home/mengembalikan.html', datakembali = output_json)


# untuk Admin
@application.route('/indexadmin/')
def indexadmin():
    db = getMysqlConnection()
    try:
        sqlstr = "SELECT * from buku"
        cur = db.cursor()
        cur.execute(sqlstr)
        output_json = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return render_template('/home/indexadmin.html', databuku = output_json)


@application.route('/icons/')
def icons():
    return render_template('/home/icons.html')

# peminjaman buku admin
@application.route('/peminjaman/')
def peminjaman():
    db = getMysqlConnection()
    try:
        sqlstr = "SELECT * from peminjaman"
        cur = db.cursor()
        cur.execute(sqlstr)
        output_json = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return render_template('/home/peminjaman.html', datapinjam = output_json)

@application.route('/addpeminjaman/', methods=['GET','POST'])
def addpeminjaman():
    if request.method == 'GET':
        return render_template('/home/addpeminjaman.html')
    elif request.method == 'POST':
        id_peminjaman = request.form['id_peminjaman']
        tanggal_pinjam = request.form['tanggal_pinjam']
        tanggal_kembali = request.form['tanggal_kembali']
        id_buku = request.form['id_buku']
        id_anggota = request.form['id_anggota']
        id_petugas = request.form['id_petugas']
        db = getMysqlConnection()
        
        try:
            cur = db.cursor()
            sukses = "data berhasil ditambah"
            sqlstr = f"INSERT INTO `peminjaman` (`id_peminjaman`, `tanggal_pinjam`, `tanggal_kembali`, `id_buku`, `id_anggota`, `id_petugas`) VALUES ("+id_peminjaman+",'"+tanggal_pinjam+"', '"+tanggal_kembali+"',"+id_buku+","+id_anggota+","+id_petugas+");"
            print(sqlstr)
            cur.execute(sqlstr)
            db.commit()
            cur.close()
            print('sukses')
            datapinjam = cur.fetchall()
        except Exception as e:
            print("Error in SQL :\n", e)
        finally:
            db.close()
        return redirect(url_for('peminjaman'))
    else:
        return render_template('/home/addpeminjaman.html', datapinjam)

@application.route('/editedpeminjaman<int:id_peminjaman>/', methods=['GET', 'POST'])
def editedpeminjaman(id_peminjaman):
    db = getMysqlConnection()    
    try:
        sqlstr = f"SELECT * from peminjaman where id_peminjaman={id_peminjaman}"
        cur = db.cursor()
        cur.execute(sqlstr)
        old_data = cur.fetchone()
        cur.close()
    except Exception as e:
        print("Error in SQL:\n", e)

    if request.method == 'POST':
        tanggal_pinjam = request.form['tanggal_pinjam']
        tanggal_kembali = request.form['tanggal_kembali']
        id_buku = request.form['id_buku']
        id_anggota = request.form['id_anggota']
        id_petugas = request.form['id_petugas']

        if len(tanggal_pinjam) == 0:
            tanggal_pinjam = old_data[0][1]
        if len(tanggal_kembali) ==  0:
            tanggal_kembali = old_data[0][2]
        if len(id_buku) ==  0:
            id_buku = old_data[0][3]
        if len(id_anggota) ==  0:
            id_anggota = old_data[0][4]
        if len(id_petugas) ==  0:
            id_petugas = old_data[0][5]
        try:
            cur = db.cursor()
            sqlstr = f"update peminjaman set tanggal_pinjam = '{tanggal_pinjam}', tanggal_kembali = '{tanggal_kembali}', id_buku = {id_buku}, id_anggota = {id_anggota}, id_petugas={id_petugas} where id_peminjaman={id_peminjaman}" 
            cur.execute(sqlstr)
            db.commit()
            cur.close()
            print('sukses')
        except Exception as e:
            print("Error in SQL:\n", e)
        finally:
            db.close()
        return redirect(url_for('peminjaman'))
    return render_template('updatedpeminjaman.html')


@application.route('/deletedpeminjaman/<int:id_peminjaman>', methods=['GET', 'POST'])
def deletedpeminjaman(id_peminjaman):
    db = getMysqlConnection()
    try:
        cur = db.cursor()
        sqlstr = f"delete from peminjaman where id_peminjaman={id_peminjaman}"
        cur.execute(sqlstr)
        db.commit()
        cur.close()
        print('sukses')
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return redirect(url_for('peminjaman'))


# pengembalian buku admin
@application.route('/pengembalian/')
def pengembalian():
    db = getMysqlConnection()
    try:
        sqlstr = "SELECT * from pengembalian"
        cur = db.cursor()
        cur.execute(sqlstr)
        output_json = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return render_template('/home/pengembalian.html', datakembali = output_json)

@application.route('/addpengembalian/', methods=['GET','POST'])
def addpengembalian():
    if request.method == 'GET':
        return render_template('/home/addpengembalian.html')
    elif request.method == 'POST':
        id_pengembalian = request.form['id_pengembalian']
        tanggal_pengembalian = request.form['tanggal_pengembalian']
        denda = request.form['denda']
        id_buku = request.form['id_buku']
        id_anggota = request.form['id_anggota']
        id_petugas = request.form['id_petugas']
        db = getMysqlConnection()
        try:
            cur = db.cursor()
            sukses = "data berhasil ditambah"
            sqlstr = f"INSERT INTO `pengembalian` (`id_pengembalian`, `tanggal_pengembalian`, `denda`, `id_buku`, `id_anggota`, `id_petugas`) VALUES ("+id_pengembalian+",'"+tanggal_pengembalian+"', "+denda+","+id_buku+","+id_anggota+","+id_petugas+");"
            print(sqlstr)
            cur.execute(sqlstr)
            db.commit()
            cur.close()
            print('sukses')
            output_json = cur.fetchall()
        except Exception as e:
            print("Error in SQL :\n", e)
        finally:
            db.close()
        return redirect(url_for('pengembalian'))
    else:
        return render_template('/home/addpengembalian.html', datakembali = output_json)
    
@application.route('/editedpengembalian/<int:id_pengembalian>', methods=['GET', 'POST'])
def editedpengembalian(id_pengembalian):
    db = getMysqlConnection()
    tanggal_pengembalian = request.form['tanggal_pengembalian']
    denda = request.form['denda']
    id_buku = request.form['id_buku']
    id_anggota = request.form['id_anggota']
    id_petugas = request.form['id_petugas']
    
    try:
        sqlstr = f"SELECT * from pengembalian where id_pengembalian={id_pengembalian}"
        cur = db.cursor()
        cur.execute(sqlstr)
        old_data = cur.fetchone()
        cur.close()
    except Exception as e:
        print("Error in SQL:\n", e)
        
    if len(tanggal_pengembalian) == 0:
        tanggal_pengembalian = old_data[0][1]
    if len(denda) ==  0:
        denda = old_data[0][2]
    if len(id_buku) ==  0:
        id_buku = old_data[0][3]
    if len(id_anggota) ==  0:
        id_anggota = old_data[0][4]
    if len(id_petugas) ==  0:
        id_petugas = old_data[0][5]
    try:
        cur = db.cursor()
        sqlstr = f"update peminjaman set tanggal_pengembalian = '{tanggal_pengembalian}', denda = {denda}, id_buku = {id_buku}, id_anggota = {id_anggota}, id_petugas={id_petugas} where id_pengembalian={id_pengembalian}" 
        cur.execute(sqlstr)
        db.commit()
        cur.close()
        db.close()
        print('sukses')
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return redirect(url_for('pengembalian'))


@application.route('/deletedpengembalian/<int:id_pengembalian>', methods=['GET', 'POST'])
def deletedpengembalian(id_pengembalian):
    db = getMysqlConnection()
    try:
        cur = db.cursor()
        sqlstr = f"delete from pengembalian where id_pengembalian={id_pengembalian}"
        cur.execute(sqlstr)
        db.commit()
        cur.close()
        print('sukses')
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return redirect(url_for('pengembalian'))

#BUKU
@application.route('/buku/')
def buku():
    db = getMysqlConnection()
    try:
        sqlstr = "SELECT * from buku"
        cur = db.cursor()
        cur.execute(sqlstr)
        output_json = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return render_template('/home/buku.html', databuku = output_json)

@application.route('/addbook/', methods=['GET','POST'])
def addbook():
    if request.method == 'GET':
        return render_template('/home/addbook.html')
    elif request.method == 'POST':
        id_buku = request.form['id_buku']
        kode_buku = request.form['kode_buku']
        judul_buku = request.form['judul_buku']
        penulis_buku = request.form['penulis_buku']
        penerbit_buku = request.form['penerbit_buku']
        tahun_penerbit = request.form['tahun_penerbit']
        stok = request.form['stok']
        db = getMysqlConnection()
        try:
            cur = db.cursor()
            sukses = "data berhasil ditambah"
            sqlstr = f"INSERT INTO `buku` (`id_buku`, `kode_buku`, `judul_buku`, `penulis_buku`, `penerbit_buku`, `tahun_penerbit`, `stok`) VALUES ("+id_buku+",'"+kode_buku+"', '"+judul_buku+"','"+penulis_buku+"','"+penerbit_buku+"','"+tahun_penerbit+"',"+stok+");"
            print(sqlstr)
            cur.execute(sqlstr)
            db.commit()
            cur.close()
            print('sukses')
            output_json = cur.fetchall()
        except Exception as e:
            print("Error in SQL :\n", e)
        finally:
            db.close()
        return redirect(url_for('buku'))
    else:
        return render_template('/home/addbook.html', databuku = output_json)

    
@application.route('/editedbook/<int:id_buku>')
def editedbook(id_buku):
    db = getMysqlConnection()
    try:
        sqlstr = f"SELECT * from buku where id_buku={id_buku}"
        cur = db.cursor()
        cur.execute(sqlstr)
        output_json = cur.fetchone()
        cur.close()
        print(output_json)
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return render_template('/home/editedbook.html', databuku=output_json)

@application.route('/editbook<int:id_buku>/', methods=['GET', 'POST'])
def editbook(id_buku):
    db = getMysqlConnection()
    kode_buku = request.form['kode_buku']
    judul_buku = request.form['judul_buku']
    penulis_buku = request.form['penulis_buku']
    penerbit_buku = request.form['penerbit_buku']
    tahun_penerbit = request.form['tahun_penerbit']
    stok = request.form['stok']
    
    try:
        sqlstr = f"SELECT * from buku where id_buku={id_buku}"
        cur = db.cursor()
        cur.execute(sqlstr)
        old_data = cur.fetchone()
        cur.close()
        print(old_data)
    except Exception as e:
        print("Error in SQL:\n", e)
        
    if len(kode_buku) == 0:
        kode_buku = old_data[0][1]
    if len(judul_buku) ==  0:
        judul_buku = old_data[0][2]
    if len(penulis_buku) ==  0:
        penulis_buku = old_data[0][3]
    if len(penerbit_buku) ==  0:
        penerbit_buku = old_data[0][4]
    if len(tahun_penerbit) ==  0:
        tahun_penerbit = old_data[0][5]
    if len(stok) ==  0:
        stok = old_data[0][6]
    try:
        cur = db.cursor()
        sqlstr = f"update buku set kode_buku ={kode_buku}, judul_buku ='{judul_buku}', penulis_buku ='{penulis_buku}', penerbit_buku ='{penerbit_buku}', tahun_penerbit='{tahun_penerbit}' where id_buku={id_buku}" 
        cur.execute(sqlstr)
        db.commit()
        cur.close()
        db.close()
        print('sukses')
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return redirect(url_for('buku'))



@application.route('/deletedbook/<int:id_buku>', methods=['GET', 'POST'])
def deletedbook(id_buku):
    db = getMysqlConnection()
    try:
        cur = db.cursor()
        sqlstr = f"delete from buku where id_buku={id_buku}"
        cur.execute(sqlstr)
        db.commit()
        cur.close()
        print('sukses')
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return redirect(url_for('book'))


#ANGGOTA
@application.route('/anggota/')
def anggota():
    db = getMysqlConnection()
    try:
        sqlstr = "SELECT * from anggota"
        cur = db.cursor()
        cur.execute(sqlstr)
        output_json = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return render_template('/home/anggota.html', dataanggota = output_json)


@application.route('/addanggota/', methods=['GET','POST'])
def addanggota():
    if request.method == 'GET':
        return render_template('/home/addanggota.html')
    elif request.method == 'POST':
        id_anggota = request.form['id_anggota']
        kode_anggota = request.form['kode_anggota']
        nama_anggota = request.form['nama_anggota']
        jk_anggota = request.form['jk_anggota']
        jurusan_anggota = request.form['jurusan_anggota']
        no_telp_anggota = request.form['no_telp_anggota']
        alamat_anggota = request.form['alamat_anggota']
        db = getMysqlConnection()
        try:
            cur = db.cursor()
            sukses = "data berhasil ditambah"
            sqlstr = f"INSERT INTO `anggota` (`id_anggota`, `kode_anggota`, `nama_anggota`, `jk_anggota`, `jurusan_anggota`, `no_telp_anggota`, `alamat_anggota`) VALUES ("+id_anggota+",'"+kode_anggota+"', '"+nama_anggota+"','"+jk_anggota+"','"+jurusan_anggota+"','"+alamat_anggota+"');"
            print(sqlstr)
            cur.execute(sqlstr)
            db.commit()
            cur.close()
            print('sukses')
            output_json = cur.fetchall()
        except Exception as e:
            print("Error in SQL :\n", e)
        finally:
            db.close()
        return redirect(url_for('buku'))
    else:
        return render_template('/home/addbook.html', databuku = output_json)

@application.route('/editanggota/<int:id_anggota>/', methods=['GET', 'POST'])
def editanggota(id_anggota):
    db = getMysqlConnection()
    kode_anggota = request.form['kode_anggota']
    nama_anggota = request.form['nama_anggota']
    jk_anggota = request.form['jk_anggota']
    jurusan_anggota = request.form['jurusan_anggota']
    no_telp_anggota = request.form['no_telp_anggota']
    alamat_anggota = request.form['alamat_anggota']
    
    try:
        sqlstr = f"SELECT * from anggota where id_anggota={id_anggota}"
        cur = db.cursor()
        cur.execute(sqlstr)
        old_data = cur.fetchone()
        cur.close()
    except Exception as e:
        print("Error in SQL:\n", e)
        
    if len(kode_anggota) == 0:
        kode_anggota = old_data[0][1]
    if len(nama_anggota) ==  0:
        nama_anggota = old_data[0][2]
    if len(jk_anggota) ==  0:
        jk_anggota = old_data[0][3]
    if len(jurusan_anggota) ==  0:
        jurusan_anggota = old_data[0][4]
    if len(no_telp_anggota) ==  0:
        no_telp_anggota = old_data[0][5]
    if len(alamat_anggota) ==  0:
        alamat_anggota = old_data[0][6]
    try:
        cur = db.cursor()
        sqlstr = f"update anggota set kode_anggota = '{kode_anggota}', nama_anggota = '{nama_anggota}', jk_anggota = '{jk_anggota}', jurusan_anggota = '{jurusan_anggota}', no_telp_anggota='{no_telp_anggota}', alamat_anggota = '{alamat_anggota}' where id_anggota={id_anggota}" 
        cur.execute(sqlstr)
        db.commit()
        cur.close()
        db.close()
        print('sukses')
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return redirect(url_for('anggota'))
            

@application.route('/deletedanggota/<int:id_anggota>', methods=['GET', 'POST'])
def deletedanggota(id_anggota):
    db = getMysqlConnection()
    try:
        cur = db.cursor()
        sqlstr = f"delete from anggota where id_anggota={id_anggota}"
        cur.execute(sqlstr)
        db.commit()
        cur.close()
        print('sukses')
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return redirect(url_for('anggota'))


#PETUGAS
@application.route('/petugas/')
def petugas():
    return render_template('/home/petugas.html')


#RAK
@application.route('/rak/')
def rak():
    return render_template('/home/rak.html')

if __name__ == '__main__':
    application.run(debug=True)