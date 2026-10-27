"""Laporan dari hasil aktual notebook M01-M04, NIM 123450062.

Jalankan dari akar repo: python scripts/export_reports.py
Memerlukan reportlab dan matplotlib. Tidak melakukan training atau membaca ulang test.
"""
import csv,json,math,re
from html import escape
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,Image,KeepTogether

ROOT=Path(__file__).resolve().parents[1]
NIM='123450062'; NAME='Abdillah Fikri Alpome'
SOURCES='Implementasi mengadaptasi kode praktikum Fabio Banyu Cyto dengan izin serta starter DSWorkbench. Seluruh perhitungan dijalankan ulang menggunakan NIM individual. OpenAI Codex digunakan untuk membantu implementasi, pemeriksaan, dan penyusunan draf pembahasan.'
ALL_ANSWERS={}
BODY_SIZE=9
def student_style(text):
    replacements={
      'Hasil tidak menggunakan angka eksperimen Fabio.':'Seluruh hasil diperoleh dari eksekusi dengan seed individual.',
      'Pada eksperimen ini':'Dalam percobaan ini',
      'hidden16':'hidden 16','hidden4':'hidden 4','hidden8':'hidden 8',
      'seed1062':'seed 1062','seed62':'seed 62','seed63':'seed 63',
      'batch32':'batch 32','batch128':'batch 128','batch512':'batch 512',
      'epoch5':'epoch 5','epoch30':'epoch 30','akhir200':'akhir 200',
      'SGD0':'SGD 0','Adam0':'Adam 0','lr0,':'lr 0,','LR1,':'LR 1,',
      'Kasus1':'Kasus 1','batch2':'batch 2','perluasan3':'perluasan 3',
      'Seluruh9':'Seluruh 9','dan13':'dan 13','diuji. Maksimum':'diuji. Nilai maksimum',
      '400 epoch':'400 epoch','selama400':'selama 400','hanya120':'hanya 120',
      'melakukan1875':'melakukan 1875','melakukan399':'melakukan 399','benar400':'benar 400',
      'epoch399':'epoch 399','menjadi59':'menjadi 59','sebagai59':'sebagai 59','dan53':'dan 53',
      '12 kombinasi':'12 kombinasi','dari81':'dari 81','dari15':'dari 15',
      'Seluruh18':'Seluruh 18','dan90':'dan 90','train12000':'train 12000',
      'validation3000':'validation 3000','train3000':'train 3000','test10000':'test 10000',
      'subset12000':'subset 12000','Subset3000':'Subset 3000','setiap kelas1200':'setiap kelas 1200',
      'dan300 validation':'dan 300 validation','masing-masing300':'masing-masing 300',
      'Train loss checkpoint':'Train loss pada checkpoint',
      'Accuracy XOR':'Akurasi XOR','Loss awal memang berubah':'Loss awal berubah',
      'proxy efisiensi':'ukuran pendekatan efisiensi',
    }
    for old,new in replacements.items():text=text.replace(old,new)
    text=re.sub(r"\b(Hidden|Batch|Baseline|FNN|Momentum|Dropout|dropout|patience|maksimal|Search|hidden|Test|train|validation|dari|pada|selama|dan|kelas|Metrics|mencatat|toleransi|hanya|daripada|parameter|faktor|bias|logit|BCE|p|step|gamma|WD|LR|bawah)(?=\d)", r"\1 ", text)
    text=text.replace('loop2-4-1','loop 2-4-1').replace('Baseline33','Baseline 33').replace('P(kelas1)','P(kelas 1)')
    return text
def read(mod):
    directory=ROOT/f'notebooks/modul-{mod}'
    s=json.loads((directory/f'hasil/M{mod}_{NIM}_results.json').read_text(encoding='utf-8'))
    rows=list(csv.DictReader((directory/f'M{mod}_{NIM}_metrics.csv').open(encoding='utf-8',newline='')))
    return directory,s,rows
def plain(s):
    return student_style(str(s)).replace('−','-').replace('–','-').replace('—','-').replace('→','->').replace('×','x').replace('±','+/-').replace('ε','epsilon')
def p(s,size=None,bold=False):
    size=BODY_SIZE if size is None else size
    return Paragraph(escape(plain(s)).replace('\n','<br/>'),ParagraphStyle('body',fontName='Helvetica-Bold' if bold else 'Helvetica',fontSize=size,leading=size*1.28,spaceAfter=4,keepWithNext=bold,textColor=colors.HexColor('#183047')))
def heading(s):return p(s,10,True)
def table(rows,widths=None):
    obj=Table([[p(v,7.3) for v in row] for row in rows],colWidths=widths,repeatRows=1,hAlign='LEFT')
    obj.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#EAF1F6')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),2),('LINEBELOW',(0,0),(-1,0),.5,colors.HexColor('#9DAFBD')),('LINEBELOW',(0,1),(-1,-1),.2,colors.HexColor('#D7E0E6'))]))
    return obj
def pic(path,width=480,max_height=190):
    from PIL import Image as PILImage
    with PILImage.open(path) as im:w,h=im.size
    scale=min(width/w,max_height/h)
    return Image(str(path),width=w*scale,height=h*scale,hAlign='CENTER')
def pdf(path,title,first,second):
    def footer(c,doc):
        c.setFont('Helvetica',7);c.setFillColor(colors.HexColor('#617080'))
        c.drawString(38,24,f'{NAME} | {NIM} | RC | 2026-10-27')
        c.drawRightString(A4[0]-38,24,f'{doc.page}')
    doc=SimpleDocTemplate(str(path),pagesize=A4,rightMargin=38,leftMargin=38,topMargin=32,bottomMargin=38,title=title,author=NAME)
    doc.build([p(title,15,True),p(f'{NAME} | NIM {NIM} | RC | 27 Oktober 2026',9),*first,*second],onFirstPage=footer,onLaterPages=footer)
def mdtable(rows):return '\n'.join(['| '+' | '.join(map(str,rows[0]))+' |','|'+'---|'*len(rows[0])]+['| '+' | '.join(map(str,row))+' |' for row in rows[1:]])
def report(mod,title,s,summary,hypothesis,data,protocol,checks,rows,figure,caption,discussion,conclusion,limits):
    global BODY_SIZE
    BODY_SIZE=8.5 if mod in ('01','02') else 9
    summary,hypothesis,data,protocol,checks,caption,discussion,conclusion,limits=map(student_style,[summary,hypothesis,data,protocol,checks,caption,discussion,conclusion,limits])
    env=s['environment']
    ident=[['Komponen','Isian'],['Nama',NAME],['NIM',NIM],['Kelas','RC'],['Modul','M'+mod+' - '+title],['Tanggal praktikum','2026-10-27'],['Seed/varian individual',s['seed']],['Device','CPU, '+str(env.get('threads',env.get('torch_threads',1)))+' thread']]
    md=f'''# Laporan Praktikum M{mod} - {title}

## Identitas Praktikan

{mdtable(ident)}

## Ringkasan Singkat

{summary}

## 1. Tujuan dan Hipotesis

### 1.1 Tujuan

Memverifikasi implementasi sesuai protokol, membandingkan konfigurasi terkendali, dan membahas hasil berdasarkan angka eksperimen sendiri.

### 1.2 Hipotesis sebelum eksperimen

{hypothesis}

## 2. Data dan Protokol Eksperimen

### 2.1 Dataset dan split

{data}

### 2.2 Konfigurasi yang dikendalikan

{protocol}

### 2.3 Lingkungan eksekusi

Python {env['python']}; PyTorch {env['torch']}; NumPy {env['numpy']}; CPU lokal DSWorkbench, kernel baru Run All. Versi dan jumlah thread tercetak di notebook.

## 3. Implementasi dan Pemeriksaan Kebenaran

{checks}

## 4. Hasil Eksperimen

### 4.1 Tabel hasil utama

{mdtable(rows)}

### 4.2 Grafik atau visualisasi utama

![Hasil M{mod}]({figure})

**Gambar 1.** {caption}

## 5. Analisis dan Pembahasan

{discussion}

## 7. Kesimpulan dan Keterbatasan

### 7.1 Kesimpulan

{conclusion}

### 7.2 Keterbatasan

{limits}

### 7.3 Tindak lanjut

Ulangi eksperimen pada beberapa seed dan anggaran yang lebih panjang untuk menilai apakah pola tetap bertahan.

## Referensi

1. Materi dan starter resmi DSWorkbench Deep Learning versi 0.4.13.
2. Fabio Banyu Cyto. Implementasi praktikum Deep Learning, diadaptasi dengan izin. https://github.com/fabiobanyu/deep-learning-123450104
3. PyTorch Contributors. Dokumentasi PyTorch. https://docs.pytorch.org/docs/stable/
4. torchvision / scikit-learn untuk pemuatan dataset dan pembagian data sesuai modul.

## Pernyataan Orisinalitas

{SOURCES} Hasil ini tidak diklaim sebagai kode yang seluruhnya ditulis tanpa bantuan. Praktikan meninjau dan memahami laporan sebelum pengumpulan.

**Nama:** {NAME}

**Tanggal:** 2026-10-27

## Checklist Sebelum Mengumpulkan

- [x] Identitas, seed, versi, device, dan sumber terisi.
- [x] Notebook selesai kernel baru Run All; angka laporan mengikuti hasil aktual.
- [x] Semua run tercatat dan grafik berlabel.
- [x] Pemilihan tidak menggunakan test; M02 tidak memakai split test.
- [ ] Praktikan meninjau laporan, mengisi formulir analisis, dan mengumpulkan tugas.
'''
    directory=ROOT/f'notebooks/modul-{mod}'
    (directory/f'M{mod}_{NIM}.md').write_text(md,encoding='utf-8')
    if mod in ('01','02','03','04'):
        first=[heading('Ringkasan singkat'),p(summary),heading('1. Tujuan dan hipotesis'),p('Tujuan: memverifikasi implementasi dan membandingkan hasil terkendali. '+hypothesis),heading('2. Data dan protokol eksperimen'),p(data),p(protocol),p(f"Lingkungan: Python {env['python']}; PyTorch {env['torch']}; NumPy {env['numpy']}; CPU, kernel baru Run All."),heading('3. Implementasi dan pemeriksaan kebenaran'),p(checks),p(SOURCES,7.8)]
        second=[heading('4. Hasil eksperimen'),table(rows,widths=[108,40,36,39,40,55,50,40,49] if mod=='04' else None),Spacer(1,6),KeepTogether([pic(directory/figure,max_height={'01':135,'02':170}.get(mod,190)),p('Gambar 1. '+caption,7.5)]),heading('5. Analisis dan pembahasan'),p(discussion),heading('7. Kesimpulan dan keterbatasan'),p(conclusion+' '+limits),p('Tindak lanjut: beberapa seed dan anggaran lebih panjang. Referensi: starter/materi DSWorkbench; implementasi Fabio Banyu Cyto; dokumentasi PyTorch. Bantuan OpenAI Codex dicantumkan dan hasil perlu ditinjau praktikan.',7.3)]
        if mod=='04':
            second.extend([heading('Confusion matrix model final'),KeepTogether([pic(directory/'figures/confusion-test.png',max_height=190),p('Gambar 2. Confusion matrix pada 10.000 citra test. Baris menunjukkan kelas sebenarnya dan kolom menunjukkan prediksi. Evaluasi dilakukan satu kali setelah model final ditentukan.',7.5)])])
        pdf(directory/f'M{mod}_{NIM}.pdf','M'+mod+' - '+title,first,second)
    if mod=='04':
        words=sum(len(line.split()) for line in md.split('## Checklist')[0].splitlines() if not line.lstrip().startswith(('|','![')))
        assert words<=1200,words
        print('M04 word count outside tables/images:',words)
def store_answers(mod,answers):
    answers=list(map(student_style,answers))
    assert len(answers)==5 and all(len(a)>=150 for a in answers)
    ALL_ANSWERS[mod]=answers
    directory=ROOT/f'notebooks/modul-{mod}'
    (directory/'hasil/analisis-formulir.json').write_text(json.dumps(answers,ensure_ascii=False,indent=2),encoding='utf-8')
    nbpath=directory/f'M{mod}_{NIM}.ipynb'
    nb=json.loads(nbpath.read_text(encoding='utf-8'))
    ident='hasil-analisis-'+mod
    nb['cells']=[c for c in nb['cells'] if c.get('id')!=ident]
    nb['cells'].append(dict(cell_type='markdown',id=ident,metadata={},source=('## Pembahasan berdasarkan eksekusi ini\n\n'+'\n\n'.join(f'**{i}.** {a}' for i,a in enumerate(answers,1))).splitlines(True)))
    nbpath.write_text(json.dumps(nb,ensure_ascii=False,indent=1),encoding='utf-8')

def m01():
    d,s,metrics=read('01');rs=s['rows'];cfg=s['configs']
    candidates=[r for r in rs if r['run_id'] in s['mandatory_ids']]
    best=min(candidates,key=lambda r:r['val_loss']);base=next(r for r in rs if r['run_id']=='baseline_relu_h8');exercise=next(r for r in rs if r['run_id']=='latihan_tanh_h8')
    by={(cfg[r['run_id']]['activation'],cfg[r['run_id']]['hidden']):r for r in candidates}
    gaps={a:abs(by[a,16]['val_loss']-by[a,4]['val_loss']) for a in ['relu','tanh','sigmoid']};stable=min(gaps,key=gaps.get)
    pairs=[(abs(a['val_metric']-b['val_metric']),-abs(a['val_loss']-b['val_loss']),a,b) for i,a in enumerate(candidates) for b in candidates[i+1:]]
    _,_,a,b=min(pairs,key=lambda x:x[:2])
    history=list(csv.DictReader((d/f'hasil/M01_{NIM}_history.csv').open(encoding='utf-8')))
    def hit(rid):
        found=next((int(e['epoch']) for e in history if e['run_id']==rid and float(e['val_loss'])<=.30),None)
        return f'epoch {found}' if found is not None else 'tidak tercapai sampai epoch 200'
    base_hit,tanh_hit=hit('baseline_relu_h8'),hit('latihan_tanh_h8')
    sizes='; '.join(f"{act}: hidden4={by[act,4]['val_loss']:.6f}, hidden16={by[act,16]['val_loss']:.6f}" for act in ['relu','tanh','sigmoid'])
    answers=[f'Hidden yang lebih besar tidak selalu memperbaiki validation loss pada eksperimen ini. {sizes}. Kapasitas meningkat dari 17 menjadi 65 parameter, tetapi peringkat tetap dipengaruhi aktivasi dan anggaran optimisasi.',f'Dengan stabilitas didefinisikan sebagai perubahan loss terhadap hidden size, aktivasi {stable} paling stabil: selisih absolutnya {gaps[stable]:.6f}. Ukuran ini hanya sensitivitas terhadap kapasitas pada seed 1062, bukan kestabilan antar-seed.',f"Konfigurasi {a['run_id']} dan {b['run_id']} memperoleh accuracy {a['val_metric']:.4f} dan {b['val_metric']:.4f}, tetapi BCE {a['val_loss']:.6f} dan {b['val_loss']:.6f}. Accuracy menilai kelas setelah threshold 0,5; BCE juga memperhitungkan keyakinan probabilitas.",f"Decision boundary paling tidak pasti pada pita probabilitas sekitar 0,5 di antara dua bulan yang saling berdekatan. Lima titik validasi terdekat 0,5 tercatat di notebook; contohnya p={s['uncertain_validation'][0]['p_kelas_1']:.4f}. Lokasi tersebut masuk akal karena noise 0,22 membuat batas kedua kelas bertumpang tindih.",'Kesimpulan terbatas pada 600 titik make_moons, satu seed 1062, noise 0,22, dan SGD selama 200 epoch. Dataset sintetis kecil ini belum mewakili citra, teks, atau domain lain; peringkat aktivasi dapat berubah ketika data atau optimizer diganti.']
    rows=[['Run','Param.','Train BCE','Val. BCE','Val. acc','Detik/epoch']]+[[r['run_id'],r['parameters'],f"{r['train_loss']:.4f}",f"{r['val_loss']:.4f}",f"{r['val_metric']:.4f}",f"{r['runtime_seconds']/200:.4f}"] for r in rs]
    summary=f"Delapan run mencakup baseline, latihan tanh, dan enam kombinasi wajib. {best['run_id']} dipilih dengan validation loss {best['val_loss']:.6f}; test loss {s['test_loss']:.6f} dan accuracy {s['test_accuracy']:.4f} diperoleh dari satu evaluasi. Hasil tidak menggunakan angka eksperimen Fabio."
    discussion=f"{answers[0]} {answers[2]} Pada latihan hidden8, tanh menghasilkan validation loss {exercise['val_loss']:.6f}, dibanding ReLU {base['val_loss']:.6f}. Aktivasi halus tidak otomatis memberi BCE lebih rendah."
    report('01','Fondasi Jaringan Saraf, FNN, Aktivasi, dan Loss',s,summary,'Hidden16 diperkirakan menurunkan loss dibanding hidden4; tanh diperkirakan lebih mudah dioptimalkan daripada sigmoid. Prediksi latihan: loss awal berubah, boundary tanh lebih halus, dan tanh dapat menurun lebih cepat.','make_moons 600 titik, noise 0,22; split terstratifikasi train/validation/test 360/120/120, seed1062. StandardScaler hanya di-fit pada train.','FNN 2-h-1, h=4/16 pada enam run; baseline/latihan h8. SGD lr0,05, batch32, 200 epoch, bobot dan urutan batch terkendali. Pemilihan memakai validation loss akhir enam run wajib.',f"Forward manual z1=h=(1,5;1), logit2,5, p0,924142, BCE0,078890; 9 parameter. Seluruh tahap NumPy-PyTorch diperiksa <1e-6. Baseline33 parameter; hidden4=17 dan hidden16=65. Delapan run dan satu test lolos assertion.",rows,'figures/final_test.png','Confusion matrix dan decision boundary model final pada 120 titik test; colorbar menunjukkan P(kelas1), garis putus-putus p=0,5. Satu titik bernilai 0,83 poin persentase accuracy.',discussion,f"Model {best['run_id']} memiliki validation accuracy {best['val_metric']:.4f} dan test accuracy {s['test_accuracy']:.4f}. Pemilihan berdasarkan BCE, bukan accuracy.",answers[4])
    initialbase=cfg['baseline_relu_h8']['initial_val_loss'];initialtanh=cfg['latihan_tanh_h8']['initial_val_loss']
    exercise_md=f'''# Latihan Mandiri Modul 01

{NAME} | {NIM} | RC | 2026-10-27 | seed1062

## Prediksi sebelum menjalankan

Digit terakhir NIM adalah 2, sehingga aktivasi latihan tanh. Saya memperkirakan loss awal berubah, tanh berpotensi lebih cepat karena berpusat di nol, dan boundary lebih halus daripada ReLU. Semua komponen lain tetap: hidden8, 33 parameter, SGD0,05, batch32, 200 epoch, split dan bobot awal sama.

## Hasil aktual

{mdtable([['Besaran','ReLU baseline','Tanh latihan'],['Val loss awal',f'{initialbase:.6f}',f'{initialtanh:.6f}'],['Val loss akhir',f"{base['val_loss']:.6f}",f"{exercise['val_loss']:.6f}"],['Val accuracy',f"{base['val_metric']:.4f}",f"{exercise['val_metric']:.4f}"]])}

![Kurva loss](figures/baseline_latihan_loss.png)

**Gambar 1.** BCE train dan validation sepanjang 200 epoch, label garis menunjukkan split dan aktivasi. Kecepatan konvergensi dibandingkan dalam epoch, bukan runtime mesin semata.

![Boundary validasi](figures/baseline_latihan_boundary.png)

**Gambar 2.** Boundary pada validation set yang sama; garis p=0,5 membedakan keputusan, colorbar menunjukkan probabilitas.

## Perbandingan prediksi dan hasil

Loss awal memang berubah sebesar {initialtanh-initialbase:+.6f}. Sebagai perbandingan deskriptif laju penurunan, ambang BCE validasi 0,30 dicapai baseline pada {base_hit}, sedangkan tanh: {tanh_hit}. Pada akhir 200 epoch, BCE tanh dikurangi ReLU adalah {exercise['val_loss']-base['val_loss']:+.6f}; dugaan tanh lebih baik tidak didukung oleh loss akhir. Boundary tanh lebih halus secara bentuk fungsi, tetapi kehalusan tidak menjamin generalisasi lebih baik. Histori seluruh epoch tersimpan di hasil/ dan bukan disalin dari run NIM lain.

Satu seed dan dataset sintetis membatasi kesimpulan. {SOURCES}
'''
    (d/'latihan-01.md').write_text(student_style(exercise_md),encoding='utf-8')
    store_answers('01',answers)

def m02():
    d,s,metrics=read('02');checks=s['gradient_summaries'];t=s['tanh'];loops=s['loop_results'];clean=loops[-1]
    std=checks['gradcheck_kasus1']['max_rel_err'];tiny=checks['gradcheck_eps9']['max_rel_err']
    hist=list(csv.DictReader((d/f'hasil/M02_{NIM}_history.csv').open(encoding='utf-8')))
    fig,ax=plt.subplots(figsize=(8,3))
    for r in loops[:5]:
        h=[e for e in hist if e['run_id']==r['run_id']]
        ax.semilogy([int(e['epoch']) for e in h],[max(float(e['true_loss_post']),1e-12) for e in h],label=r['run_id'].replace('loop_',''))
    ax.set(title='Diagnosis XOR: BCE benar setelah update',xlabel='Epoch',ylabel='BCE (log; tampilan minimum 1e-12)');ax.legend(fontsize=7,ncol=2);ax.grid(alpha=.25);fig.tight_layout()
    (d/'figures').mkdir(exist_ok=True);fig.savefig(d/'figures/diagnosis.png',dpi=160);plt.close(fig)
    answers=[f'Relative error nonnol muncul karena finite difference hanya pendekatan dan float64 memiliki pembulatan. Pada Kasus1 maksimum error {std:.3e}, sehingga ambang modul 1e-5 masih terpenuhi. Komponen yang gradiennya sama-sama nol dapat memiliki relative error tepat nol.',f'Ketika epsilon berubah dari 1e-5 ke 1e-9, maksimum relative error menjadi {tiny:.3e}, dibanding {std:.3e} sebelumnya, meningkat sekitar {tiny/std:.0f} kali. Dua nilai loss semakin berdekatan, sehingga cancellation dan pembulatan menjadi besar setelah dibagi 2epsilon.',f"Gradien contoh pertama dan kedua bergabung pada operasi perkalian matriks dan penjumlahan bias: dW1=Delta1.T@X dan dW2=H.T@delta2. Karena loss merupakan rata-rata, delta2 sudah memuat faktor1/2. Loss batch aktual {s['batch']['loss']:.9f} dan db2 {s['batch']['grads']['b2']:.9f} sesuai rata-rata kontribusi individual.",f"Urutan step sebelum backward paling sulit dideteksi dari loss saja: perbaikan2 dan3 sama-sama menghasilkan BCE {loops[2]['loss_akhir']:.3e} dan {loops[3]['loss_akhir']:.3e}. Namun urutan salah hanya melakukan399 update, sedangkan urutan benar400; kesetaraan state dengan epoch399 membuktikan pergeseran satu langkah.",f"Backpropagation menghitung gradien loss dengan aturan rantai, misalnya gradien W2 Kasus1 [-0,113787270;-0,075858180]. Optimizer kemudian mengubah parameter menggunakan gradien tersebut; pada XOR digunakan SGD dengan learning rate0,1. Pemisahan ini menjelaskan mengapa backward dan step harus dipanggil dalam urutan yang benar."]
    rows=[['Tahap','Loss awal','Loss akhir','Benar','Norma L2']]+[[r['run_id'].replace('loop_',''),f"{r['loss_awal']:.5f}",f"{r['loss_akhir']:.3e}",f"{r['benar_dari_4']}/4",f"{r['norma_parameter']:.4f}"] for r in loops]
    shrink=(1-t['norm_ratio'])*100
    summary=f"Gradien manual cocok dengan autograd dan finite difference pada Kasus1, perluasan3 neuron, tanh dan batch2. Relative error batch maksimum {checks['gradcheck_batch2']['max_rel_err']:.3e}. Loop benar mencapai BCE {clean['loss_akhir']:.6f} dengan {clean['benar_dari_4']}/4 benar; target loss<0,1 belum terpenuhi."
    checks_text=f"Seluruh9 komponen Kasus1/tanh dan13 komponen perluasan/batch diuji. Maksimum relative error Kasus1 {std:.3e}; epsilon1e-9 {tiny:.3e}. Akumulasi dua backward menghasilkan gradien2x; reset memulihkan1x. Loop bersih identik dengan perbaikan4."
    discussion=f"Norma gradien W1 tanh turun {shrink:.2f}% dari {t['relu_norm_dW1']:.6f} menjadi {t['tanh_norm_dW1']:.6f}, mendukung prediksi latihan. Empat perbaikan kumulatif adalah aktivasi ReLU, penggunaan logit tanpa sigmoid ganda, urutan backward-step, dan zero_grad setiap iterasi. BCE nol pada loop dengan akumulasi bukan bukti implementasi benar; norma bobot dan jumlah update harus diperiksa."
    report('02','Backpropagation dan Automatic Differentiation',s,summary,'Mengganti ReLU dengan tanh diperkirakan mengecilkan norma dW1 pada Kasus1 karena faktor1-tanh(z1)^2<1; perubahan p-y tetap harus diperhitungkan. Epsilon terlalu kecil diperkirakan meningkatkan error.','Kasus1 tetap x=(2,-1),y=1; W1=[[0,5;-0,5],[1;1]], b1=0, W2=(2,-1), b2=0,5. Batch menambah x2=(-1,3),y2=0. Diagnosis memakai empat titik XOR tanpa validation/test.','Float64, seed62, loop2-4-1, SGD0,1 selama400 epoch. Neuron ketiga memakai W1=(-1;0,5), bias0,25, W2=-0,5. Mean loss dipakai untuk batch. Metrics20 kolom asli ditambah record_type wajib checkpoint.',checks_text,rows,'figures/diagnosis.png','BCE benar setelah update pada lima tahap kumulatif, garis berlabel. Nilai di bawah1e-12 dibatasi hanya untuk tampilan log; metrics mempertahankan nilai asli.',discussion,f"Enam run loop dan53 komponen gradient check tersimpan sebagai59 baris metrics. Accuracy XOR {clean['benar_dari_4']}/4 tidak berarti target BCE<0,1 tercapai.",'Eksperimen menggunakan kasus sangat kecil dan satu seed. Konvergensi XOR bergantung pada inisialisasi; tidak ada klaim generalisasi ke dataset lain.')
    exercise=f'''# Latihan Mandiri Modul 02

{NAME} | {NIM} | RC | 2026-10-27 | seed62 | float64

## Prediksi sebelum menjalankan

Saya memperkirakan norma gradien W1 mengecil saat ReLU diganti tanh karena turunannya1-tanh(z1)^2 berada di bawah1 pada z1=(1,5;1). Besar p-y juga berubah, sehingga prediksi harus diuji, bukan hanya melihat turunan aktivasi.

## Turunan manual tanpa autograd

h=[tanh(1,5),tanh(1)], z2=2h1-h2+0,5, d=sigmoid(z2)-1.

dz1=d*[2,-1]*[1-tanh(1,5)^2,1-tanh(1)^2].

dW1=outer(dz1,[2,-1]); db1=dz1; dW2=d*h; db2=d.

## Hasil aktual dan perbandingan

Norma dW1 ReLU {t['relu_norm_dW1']:.9f}, tanh {t['tanh_norm_dW1']:.9f}; turun {shrink:.2f}%. Dz1 tanh adalah {t['dz1']}. BCE tanh {t['loss']:.9f} dan probabilitas {t['p']:.9f}. Sembilan komponen diperiksa: maksimum relative error {checks['latihan_tanh']['max_rel_err']:.3e}, sesuai ambang1e-5. Autograd digunakan sesudah turunan NumPy untuk memverifikasi, bukan untuk menghasilkan turunan manual.

Prediksi pengecilan norma W1 didukung, tetapi tidak berlaku untuk seluruh gradien: faktor p-y berubah dan dapat membesar. Nilai dW1 lengkap adalah {t['grads']['W1']}; semua angka tersedia pada hasil/M02_{NIM}_gradients.csv. Karena Kasus1 memakai parameter tetap, hasil bagian ini sama untuk beberapa NIM; loop XOR memakai seed62 dan dihitung ulang.

{SOURCES}
'''
    (d/'latihan-02.md').write_text(student_style(exercise),encoding='utf-8')
    store_answers('02',answers)

def m03():
    d,s,metrics=read('03');runs=s['runs'];by={r['run_id']:r for r in runs}
    core=[r for r in runs if r['group']=='grid'];best=min(core,key=lambda r:r['val_loss']);fast=min(core,key=lambda r:r['runtime_s']);final=by[s['selected_run']]
    winners={opt:min([r for r in core if r['optimizer']==opt],key=lambda r:r['val_loss']) for opt in ['sgd','momentum','adam']}
    batches=[by[f'batch_{b}'] for b in [32,128,512]];efficient=max(batches,key=lambda r:r['val_acc']/r['runtime_s'])
    no,step,cos=by['scheduler_none'],by['scheduler_step'],by['scheduler_cosine']
    hist=list(csv.DictReader((d/f'hasil/M03_{NIM}_history.csv').open(encoding='utf-8')))
    large=[r for r in hist if r['run_id']=='baseline_sgd_lr1']
    first_rise=next((int(large[i]['epoch']) for i in range(1,len(large)) if float(large[i]['val_loss'])>float(large[i-1]['val_loss'])),None)
    answers=[f"Model grid terbaik adalah {best['run_id']} dengan validation loss {best['val_loss']:.6f} dan runtime {best['runtime_s']:.2f} detik. Run tercepat adalah {fast['run_id']} dengan waktu {fast['runtime_s']:.2f} detik dan loss {fast['val_loss']:.6f}; loss terendah dan waktu tercepat mengukur tujuan berbeda.",f"Adam terbaik memakai LR {winners['adam']['learning_rate']:g}, sedangkan SGD terbaik LR {winners['sgd']['learning_rate']:g}. Adam membagi momen pertama gradien dengan skala momen keduanya, sehingga nilai learning rate numerik yang sama tidak memberikan besar pembaruan yang sama seperti SGD.",f"Pada baseline SGD LR1, validation loss akhir {by['baseline_sgd_lr1']['val_loss']:.6f} dan grad_norm_mean {by['baseline_sgd_lr1']['grad_norm_mean']:.6f}. Kenaikan loss antar-epoch pertama teramati pada epoch {first_rise}; langkah terlalu besar dapat melewati daerah minimum dan menghasilkan osilasi.",f"Tanpa scheduler diperoleh loss {no['val_loss']:.6f}; StepLR {step['val_loss']:.6f}; CosineAnnealingLR {cos['val_loss']:.6f}, semuanya lima epoch. Scheduler tidak menjamin perbaikan: penurunan LR terlalu awal dapat membatasi langkah optimisasi ketika model belum cukup belajar.",f"Jika efisiensi diukur sebagai validation accuracy dibagi runtime pada run lima epoch yang tersedia, batch {efficient['batch_size']} paling tinggi: accuracy {efficient['val_acc']:.4f}, waktu {efficient['runtime_s']:.2f} detik, dan {efficient['n_update']} update. Ini rekomendasi berdasarkan proxy efisiensi, bukan bukti pada eksperimen dengan batas waktu persis sama."]
    rows=[['Run','Train CE','Val. CE','Val. acc','Detik/epoch']]+[[r['run_id'],f"{r['train_loss']:.4f}",f"{r['val_loss']:.4f}",f"{r['val_acc']:.4f}",f"{r['runtime_per_epoch_s']:.3f}"] for r in runs]
    summary=f"Delapan belas run mencakup tiga baseline LR, sembilan grid optimizer, dan enam kondisi scheduler/batch. Model final {final['run_id']} memiliki validation loss {final['val_loss']:.6f}, test loss {s['test_loss']:.6f}, dan test accuracy {s['test_accuracy']:.4f}; test dievaluasi satu kali setelah seluruh kandidat terkunci."
    discussion=f"{answers[1]} {answers[3]} Batch32 melakukan1875 update, batch512 hanya120 pada lima epoch. Karena anggaran epoch tidak sama dengan anggaran waktu atau update, keuntungan satu batch perlu dibaca bersama runtime."
    report('03','Optimizer dan Strategi Pelatihan',s,summary,'Adam diperkirakan cepat mencapai loss rendah; scheduler belum tentu membantu pada lima epoch. Batch32 diperkirakan memberi loss lebih rendah melalui lebih banyak update, tetapi memerlukan lebih banyak waktu.','Fashion-MNIST, subset train12000/validation3000 terstratifikasi seed62 dari60000 train resmi; test10000 terpisah. Mean/std hanya dari subset train.','FNN784-128-10, 101770 parameter, lima epoch. SGD/Momentum0,9/Adam diuji pada LR masing-masing. Scheduler none/StepLR(step2,gamma0,5)/Cosine; batch32/128/512 memakai optimizer/LR terbaik grid. Pemilihan dari15 kandidat inti+tambahan, berdasarkan loss epoch terakhir.','Split terpisah, setiap kelas1200 train dan300 validation. Semua run memanggil fungsi sama, seed bobot/loader diulang. Seluruh18 run dan90 epoch tercatat; jumlah update batch32=1875 dan512=120; tepat satu test.',rows,'figures/pemenang-optimizer.png','Cross-entropy validation sepanjang lima epoch untuk pemenang masing-masing optimizer; label mencantumkan LR. Kurva baseline dan scheduler/batch juga tersedia di notebook.',discussion,f"Final {final['run_id']} dipilih dari validation loss; test accuracy {s['test_accuracy']:.4f}. Pilihan efisiensi batch pada mesin ini adalah batch{efficient['batch_size']} menurut accuracy/runtime.",'Satu seed, subset12000 citra dan lima epoch tidak cukup untuk menyatakan optimizer terbaik pada semua dataset. Rasio accuracy/runtime hanyalah proxy karena waktu tiap run tidak dikunci sama.')
    exercise=f'''# Latihan Mandiri Modul 03

{NAME} | {NIM} | RC | 2026-10-27 | seed62

## Prediksi sebelum menjalankan

Batch32 diperkirakan melakukan lebih banyak update dan dapat menurunkan loss lebih jauh, tetapi runtime akan lebih lama dibanding batch512. Karena anggaran sama-sama lima epoch, perbandingan belum adil bila tujuan sebenarnya adalah batas waktu yang sama. Prediksi tercatat sebelum training di hasil/prediksi-sebelum-run.json.

## Hitungan dan hasil aktual

ceil(12000/32)*5=1875 update; ceil(12000/512)*5=120 update. Rasio jumlah update adalah15,625 kali. Data, split, inisialisasi, optimizer, learning rate dan lima epoch sama; hanya batch berubah.

{mdtable([['Batch','Update','Val loss','Val accuracy','Runtime (s)']]+[[r['batch_size'],r['n_update'],f"{r['val_loss']:.6f}",f"{r['val_acc']:.4f}",f"{r['runtime_s']:.3f}"] for r in batches])}

![Scheduler dan batch](figures/scheduler-batch.png)

**Gambar 1.** Kiri membandingkan scheduler dan kanan batch size; sumbu horizontal epoch dan vertikal validation cross-entropy. Tiga kondisi batch memiliki jumlah update berbeda walaupun epoch sama.

## Perbandingan dengan prediksi

Batch32 dikurangi batch512 memberi selisih validation loss {by['batch_32']['val_loss']-by['batch_512']['val_loss']:+.6f}, serta runtime {by['batch_32']['runtime_s']-by['batch_512']['runtime_s']:+.3f} detik. Jumlah update yang lebih besar tidak boleh disamakan dengan optimizer yang secara intrinsik lebih baik. {answers[4]}

{SOURCES}
'''
    (d/'latihan-03.md').write_text(student_style(exercise),encoding='utf-8');store_answers('03',answers)

def m04():
    d,s,metrics=read('04');runs=s['runs'];by={r['run_id']:r for r in runs};base=by['baseline'];final=by['final_retrain'];reg=[r for r in runs if r['group']=='regularisasi'];trials=[r for r in runs if r['group']=='random_search']
    best_gap=min(reg,key=lambda r:r['gap']);best_val=min(reg,key=lambda r:r['val_loss']);trial=min(trials,key=lambda r:r['val_loss']);biggest=max(trials,key=lambda r:r['parameters'])
    history=list(csv.DictReader((d/f'hasil/M04_{NIM}_history.csv').open(encoding='utf-8')))
    bh=[e for e in history if e['run_id']=='baseline'];rise=next((int(e['epoch']) for e in bh if int(e['epoch'])>base['best_epoch'] and float(e['val_loss'])>base['val_loss']),None)
    answers=[f"Baseline menunjukkan validation loss minimum {base['val_loss']:.6f} pada epoch {base['best_epoch']}, lalu lebih tinggi sesudahnya, misalnya epoch {rise}. Pada epoch terakhir loss validasi {base['val_loss_last']:.6f} dan gap {base['gap_last']:.6f}; ketidakseimbangan train-validation ini menjadi bukti overfitting.",f"Di antara baseline dan tiga strategi terpisah, gap checkpoint terkecil dimiliki {best_gap['run_id']} sebesar {best_gap['gap']:.6f}, sedangkan validation loss terendah dimiliki {best_val['run_id']} sebesar {best_val['val_loss']:.6f}. Gap kecil saja dapat muncul karena underfitting; karena itu tetap perlu melihat kedua loss.",f"Trial dengan jumlah parameter terbesar yang tercatat adalah {biggest['run_id']} ({biggest['parameters']:,} parameter; loss {biggest['val_loss']:.6f}). Trial pemenang {trial['run_id']} mempunyai {trial['parameters']:,} parameter dan loss {trial['val_loss']:.6f}; kapasitas terbesar tidak otomatis paling baik pada validasi.",f"Hyperparameter tidak dapat diperingkat pengaruh kausalnya dari12 kombinasi acak yang tidak seimbang. Trial terbaik memakai hidden={trial['hidden']}, dropout={trial['dropout']}, weight_decay={trial['weight_decay']:g}, LR={trial['learning_rate']:g}, dengan loss {trial['val_loss']:.6f}. Perbedaan trial mencampur beberapa faktor sehingga analisis pengaruh tunggal memerlukan ablation terkendali.",f"Model final memiliki validation loss {final['val_loss']:.6f} dan test loss {s['test_loss']:.6f}, sehingga test minus validation adalah {s['test_loss']-final['val_loss']:+.6f}. Ini menggambarkan perbedaan hasil pada dua split untuk model terpilih, bukan alasan menyesuaikan hyperparameter setelah melihat test; hanya satu lintasan test dilakukan."]
    rows=[['Run','Hidden','Dropout','WD','LR','Epoch best/stop','Val loss','Gap','Val acc']]+[[r['run_id'],r['hidden'],r['dropout'],f"{r['weight_decay']:g}",f"{r['learning_rate']:g}",f"{r['best_epoch']}/{r['epochs_completed']}",f"{r['val_loss']:.5f}",f"{r['gap']:.5f}",f"{r['val_acc']:.4f}"] for r in runs]
    summary=f"Baseline dan tiga strategi regularisasi diuji terpisah, ditambah latihan dropout0,2, dua belas random-search trial dan satu refit final. Trial {trial['run_id']} menang dengan validation loss {trial['val_loss']:.6f}. Refit menghasilkan loss validasi identik; test satu kali memberi loss {s['test_loss']:.6f} dan accuracy {s['test_accuracy']:.4f}."
    answers[2]=f"Pada eksperimen ini pemenang random_11 memang memakai jumlah parameter maksimum dalam ruang yang dicoba, yaitu {trial['parameters']:,}. Namun trial lain dengan kapasitas sama, misalnya {biggest['run_id']}, memperoleh loss {biggest['val_loss']:.6f}, dibanding {trial['val_loss']:.6f} pada pemenang. Jadi jumlah parameter saja belum menentukan peringkat."
    grouped={key:{v:sum(r['val_loss'] for r in trials if r[key]==v)/sum(r[key]==v for r in trials) for v in sorted({r[key] for r in trials})} for key in ['hidden','dropout','weight_decay','learning_rate']}
    most=max(grouped,key=lambda key:max(grouped[key].values())-min(grouped[key].values()))
    vals=grouped[most];low=min(vals,key=vals.get);high=max(vals,key=vals.get)
    answers[3]=f"Secara deskriptif, {most} memiliki rentang rerata validation loss antarkelompok terbesar: nilai {high} memberi rerata {vals[high]:.6f}, sedangkan {low} memberi {vals[low]:.6f}. Namun hanya 12 dari 81 kombinasi diuji dan jumlah anggota tiap kelompok tidak seimbang; faktor lain ikut berubah, sehingga ini bukan bukti pengaruh kausal tunggal."
    discussion=' '.join([answers[0],answers[1],answers[3]])
    report('04','Regularisasi dan Hyperparameter Tuning',s,summary,'Baseline512-512 pada3000 train diperkirakan overfit; dropout0,5 menekan gap tetapi lebih lambat. Dropout0,2 diperkirakan menurunkan train loss lebih cepat daripada0,5. Early stopping diperkirakan menghindari kenaikan loss validasi.','Fashion-MNIST, train3000/validation3000 terstratifikasi seed62; mean/std dihitung hanya pada train. Test10000 baru dibuka setelah konfigurasi terkunci.','Baseline784-512-512-10, Adam0,001, batch128, maksimal30 epoch. Tiga strategi: dropout0,5, WD0,001, atau patience5; setiap run hanya mengubah satu faktor. Search81 kombinasi hidden64/128/256, dropout0/0,2/0,5, WD0/1e-4/1e-3, LR1e-4/3e-4/1e-3. Dua belas trial unik dipilih dengan seed63 dan patience5. Semua run memulihkan checkpoint loss validasi terbaik; hasil akhir epoch juga dicatat terpisah.','Baseline669706 parameter; split tanpa overlap, masing-masing300 train dan300 validation per kelas. Dua belas kombinasi search unik; refit mengulang loss validasi pemenang tepat dalam toleransi1e-10. Metrics mencatat18 run termasuk latihan dan refit; test satu lintasan.',rows,'figures/gap-regularisasi.png','Gap=validation loss-train loss, keduanya dihitung dalam eval mode. Garis dibedakan berdasarkan strategi dan berakhir pada epoch berhenti masing-masing. Nilai pada tabel berasal dari checkpoint validasi terbaik, bukan selalu epoch terakhir.',discussion,f"Konfigurasi final {trial['run_id']} memiliki test accuracy {s['test_accuracy']:.4f}. {answers[4]}",'Subset3000 citra, satu seed dan hanya12 dari81 kombinasi membatasi kesimpulan. Perbandingan checkpoint terbaik dan epoch terakhir harus dibedakan; search tidak membuktikan pengaruh kausal satu hyperparameter.')
    a,b=by['dropout_0.2'],by['dropout_0.5']
    loss5a=next(float(e['train_loss']) for e in history if e['run_id']=='dropout_0.2' and int(e['epoch'])==5)
    loss5b=next(float(e['train_loss']) for e in history if e['run_id']=='dropout_0.5' and int(e['epoch'])==5)
    exercise=f'''# Latihan Mandiri Modul 04

{NAME} | {NIM} | RC | 2026-10-27 | seed62

## Prediksi sebelum menjalankan

Dropout0,2 diperkirakan menurunkan train loss lebih cepat daripada0,5 karena lebih banyak unit aktif. Dropout0,5 diperkirakan mengurangi gap lebih kuat, tetapi dapat memperlambat pelatihan. Prediksi disimpan sebelum run pertama di hasil/prediksi-sebelum-run.json.

## Protokol dan hasil aktual

Semua kondisi memakai baseline784-512-512-10, Adam0,001, batch128,30 epoch; hanya probabilitas dropout berubah. Loss train/validation dihitung dalam eval mode sehingga mask dropout tidak mengacaukan pengukuran gap. Tabel menunjukkan checkpoint terbaik berdasarkan aturan pemilihan yang sama pada kedua run; kurva menampilkan seluruh epoch.

{mdtable([['Kondisi','Train loss','Val loss','Gap','Epoch terbaik']]+[[r['run_id'],f"{r['train_loss']:.6f}",f"{r['val_loss']:.6f}",f"{r['gap']:.6f}",r['best_epoch']] for r in [base,a,b]])}

![Train loss dropout](figures/latihan-dropout.png)

**Gambar 1.** Train cross-entropy tanpa mask dropout pada setiap epoch; legenda membedakan baseline, dropout0,2 dan0,5. Interpretasi kecepatan menggunakan kurva dan histori, bukan membandingkan checkpoint pada epoch berbeda tanpa catatan.

## Perbandingan prediksi dan hasil

Pada epoch 5 yang sama, train loss dropout 0,2 sebesar {loss5a:.6f}, dibanding {loss5b:.6f} pada dropout 0,5; hasil ini {'mendukung' if loss5a<loss5b else 'tidak mendukung'} prediksi penurunan lebih cepat. Train loss checkpoint 0,2 dikurangi 0,5 adalah {a['train_loss']-b['train_loss']:+.6f}; gap berubah dari {b['gap']:.6f} pada 0,5 menjadi {a['gap']:.6f} pada 0,2. Epoch terbaik masing-masing {a['best_epoch']} dan {b['best_epoch']}. Regularisasi yang lebih kuat belum tentu memberi validation loss terbaik; besarnya gap perlu dibaca bersama kedua loss. Satu seed tidak cukup untuk menggeneralisasi tingkat dropout optimal. Pada checkpoint terbaik, validation loss dropout 0,2 adalah {a['val_loss']:.6f}, sedangkan dropout 0,5 adalah {b['val_loss']:.6f}; prediksi bahwa dropout 0,5 memperkecil gap tidak didukung oleh hasil ini. Dropout yang terlalu besar menghilangkan banyak unit saat training sehingga kapasitas efektif berkurang dan optimisasi melambat; jika terjadi underfitting, train loss dan validation loss dapat sama-sama memburuk. Percobaan ini tidak menunjukkan kedua loss memburuk secara bersamaan pada checkpoint terbaik. Catatan prediksi awal menekankan train loss dan gap; arah validation loss belum dicatat secara eksplisit sebelum run.

{SOURCES}
'''
    (d/'latihan-04.md').write_text(student_style(exercise),encoding='utf-8');store_answers('04',answers)

if __name__=='__main__':
    import sys
    requested=sys.argv[1:] or ['01','02','03','04']
    for mod in requested:
        globals()['m'+mod]()
        print('REPORT COMPLETE',mod,flush=True)
    for mod in ['01','02','03','04']:
        path=ROOT/f'notebooks/modul-{mod}/hasil/analisis-formulir.json'
        if path.is_file():ALL_ANSWERS[mod]=json.loads(path.read_text(encoding='utf-8'))
    (ROOT/'notebooks/analisis-formulir-123450062.json').write_text(json.dumps(ALL_ANSWERS,ensure_ascii=False,indent=2,sort_keys=True),encoding='utf-8')
