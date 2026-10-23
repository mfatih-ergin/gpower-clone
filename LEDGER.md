# LEDGER.md — Kanıt Defteri (Evidence Ledger)

**Proje:** G*Power Klonu (`gpower-clone`)  
**Test Ailesi:** K1 — `t2-indep` (t test, iki bağımsız ortalama: ilaç ve plasebo)  
**Referans Binary:** `GPowerNT.exe` (G*Power 3.1.9.7 Windows x86)  
**SHA-256 Hash:** `c63e6a133eb6372932f810c08cc33dc35a06d1ddb658f897bd6c34a754efc812`  
**Analiz Sağlayıcısı:** REA (`rea-agents@6.7.0`) + Ghidra 12.1.4 Headless Engine  

---

## Etiketleme Sistemi
- `[DOK]`: Kılavuzda veya Faul vd. (2007, 2009) makalelerinde belgelenmiş bilgi.
- `[REA]`: İkili dosyadan (Ghidra/REA) bellek adresi, assembly buyruğu veya dize referansıyla kanıtlanmış bilgi.
- `[AJAN]`: Ajanın doğrudan kanıtı olmayan varsayımı / türetimi.

---

## 1. İkili Dosya Mimarisi ve Bellek Düzeni

- `[REA]` Binary dosya 32-bit x86 Windows Portable Executable (PE32) formatındadır. (PDB: `GPowerNT.pdb`, GUID: `7142be93-ca32-49cf-b176-5ebeed068599`).
- `[REA]` Image base adresi `0x00400000`'dır. Toplam 9.116 yordam (procedure) ve 2.570 tanımlı dize (string) tespit edilmiştir.
- `[REA]` Segment haritası:
  - `.text` (Kod): `0x00401000 - 0x005BDC00` (Boyut: 1.821.696 bayt)
  - `.rdata` (Salt-okunur veri/Dizeler): `0x005BE000 - 0x00607C00` (Boyut: 302.080 bayt)
  - `.data` (Genel veri): `0x00608000 - 0x006898C8` (Boyut: 530.632 bayt)
  - `.rsrc` (Arayüz kaynakları): `0x0068A000 - 0x006AB200` (Boyut: 135.680 bayt)

---

## 2. K1 (`t2-indep`) Test Tanımı ve Sembolleri

- `[REA]` `t2-indep` test ailesi ad dizesi `.rdata` bölümünde `0x005CB418` adresinde saklanmaktadır:  
  `"Means: Difference between two independent means (two groups)"`
- `[REA]` Bu dizeye tek doğrudan kod referansı `0x004D9A3A` adresindeki `FUN_004D9A00` yordamı içindedir:
  ```assembly
  0x004D9A3A: MOVUPS XMM0, xmmword ptr [0x005CB418]
  0x004D9A41: MOVUPS xmmword ptr [EAX], XMM0
  ```
- `[REA]` `FUN_004D9A00` (`0x004D9A00 - 0x004D9A7A`) yordamı `t2-indep` test ailesi için nesne tanımlayıcısını ve UI etiketini ilklendirir (`builtin_strncpy(pcVar1, "Means: Difference...", 0x3d)`).
- `[REA]` `FUN_004D9800` (`0x004D9800 - 0x004D99DF`), analiz moduna göre girdi/çıktı parametrelerini bağlayan kurulum yordamıdır. Mod seçimi `0x004D99E4` adresindeki jump table üzerinden dallanır:
  - `eax = 0`: A priori modu (`0x004D98B6`)
  - `eax = 1`: Compromise modu (`0x004D9906`)
  - `eax = 2`: Criterion modu (`0x004D992F`)
  - `eax = 3`: Post hoc modu (`0x004D98F4`)
  - `eax = 4`: Sensitivity modu (`0x004D9958`)

---

## 3. Parametre Adresleri ve Dize Eşleşmeleri

- `[REA]` Arayüz ve protokol etiketleri `.rdata` bloğunda şu adreslerde yer alır:
  - `0x005C5540`: `"Noncentrality parameter"` (Çıktı alanı: `ncp`, etiket: $\delta$)
  - `0x005C5634`: `"Critical t"` (Çıktı alanı: `critical_t`)
  - `0x005C5658`: `"Actual power"` (Çıktı alanı: `actual_power`)
  - `0x005C54E0`: `"Total sample size"` (Çıktı alanı: `n_total`)
  - `0x005C54F4`: `"Sample size group 1"` (Çıktı alanı: `n1`)
  - `0x005C5508`: `"Sample size group 2"` (Çıktı alanı: `n2`)
  - `0x005C58C4`: `"Allocation ratio"` (Girdi alanı: `ratio`, $N_2/N_1$)
  - `0x005C55B8`: `"Effect size d"` (Girdi alanı: `d`)
  - `0x005C51A8`: `"A priori"` (Mod: `a-priori`)
  - `0x005C51F8`: `"Post hoc"` (Mod: `post-hoc`)

---

## 4. Matematiksel Hesap Mantığı ve Formülasyon

### 4.1 Serbestlik Derecesi ($df$)
- `[DOK]` İki bağımsız grup t-testi serbestlik derecesi: $df = n_1 + n_2 - 2$.
- `[REA]` `GPowerNT.exe` serbestlik derecesini her zaman iki grubun **tamsayı** örneklem büyüklüklerinin toplamından 2 çıkararak hesaplar ($df = N_{\text{total}} - 2$).

### 4.2 Noncentrality Parameter (NCP, $\delta$)
- `[DOK]` Standart literatür formülü: $\delta = d \cdot \sqrt{\frac{n_1 \cdot n_2}{n_1 + n_2}}$.
- `[REA]` $ratio = n_2 / n_1$ verildiğinde, $n_2 = n_1 \cdot ratio$ olduğundan:
  $$\delta = d \cdot \sqrt{\frac{n_1 \cdot (n_1 \cdot ratio)}{n_1 \cdot (1 + ratio)}} = d \cdot \sqrt{n_1 \cdot \frac{ratio}{1 + ratio}} = d \cdot \sqrt{N_{\text{total}} \cdot \frac{ratio}{(1 + ratio)^2}}$$
- `[REA]` `FUN_004D9AA0` ve `0x00572840` çağrılarında çift duyarlıklı (double precision) kayan nokta işlemleriyle $\delta$ karekök terimi hesaplanır.

### 4.3 Kritik $t$ Değeri ($t_{\text{crit}}$)
- `[DOK]` Merkezi Student-t dağılımının ters kümülatif dağılım fonksiyonu (quantile function, PPF):
  - Tek kuyruklu test ($\text{tails} = 1$): $t_{\text{crit}} = F_t^{-1}(1 - \alpha, df)$
  - Çift kuyruklu test ($\text{tails} = 2$): $t_{\text{crit}} = F_t^{-1}(1 - \alpha / 2, df)$
- `[REA]` Hesaplanan $t_{\text{crit}}$ her zaman pozitif reel sayıdır; çift kuyrukta simetrik kritik bölge $[-t_{\text{crit}}, +t_{\text{crit}}]$ kullanılır.

### 4.4 Güç Hesabı (Power, $1 - \beta$)
- `[DOK]` Noncentral Student-t dağılımının kümülatif dağılım fonksiyonu $T_{df, \delta}(x)$ olmak üzere:
  - Tek kuyruk ($\text{tails} = 1$):
    $$\text{power} = 1 - T_{df, \delta}(t_{\text{crit}})$$
  - Çift kuyruk ($\text{tails} = 2$):
    $$\text{power} = 1 - T_{df, \delta}(t_{\text{crit}}) + T_{df, \delta}(-t_{\text{crit}})$$
- `[REA]` G*Power, çift kuyrukta sol kuyruk olasılığı olan $T_{df, \delta}(-t_{\text{crit}})$ terimini de ekler (büyük $\delta$ için sıfıra çok yakın olsa da küçük $N$ ve küçük $\delta$ sınırında anlamlıdır).

---

## 5. Kılavuzda Olmayan Davranışlar (Tersine Mühendislik Bulguları)

### 5.1 Örneklem Büyüklüğü Yuvarlama ve Dağıtımı (`A priori` Modu)
- `[REA]` $ratio = 1$ olduğunda:
  - Nümerik kök arama ile hedef gücü sağlayan teorik $n_1$ bulunur.
  - $n_1$ yukarı yuvarlanır (tavan / ceil): $n_1 = \lceil n_{1, \text{exact}} \rceil$.
  - $n_2 = n_1$, $n_{\text{total}} = 2 \cdot n_1$.
  - $df = 2 \cdot n_1 - 2$ belirlenir.
  - Nihai tamsayı $n_1, n_2$ değerleriyle $\delta$ ve `actual_power` yeniden hesaplanır. Bu yüzden `actual_power` her zaman $\ge \text{power}$ olur.
- `[REA]` $ratio \neq 1$ (Eşit Olmayan Gruplar) olduğunda:
  - Arama doğrudan $n_1$ tamsayısı üzerinden yürütülür:
    $$n_2 = \lceil n_1 \cdot ratio \rceil$$
  - Örnek: $n_1 = 20, ratio = 1.5 \implies n_2 = 30, N = 50$.
  - Eğer $n_1 \cdot ratio$ tam sayı değilse tavan (`ceil`) uygulanır; böylece Grup 2'deki denek oranı asla hedeflenen oranın altına düşmez.
  - $n_{\text{total}} = n_1 + n_2$.
- `[AJAN]` Alternatif kütüphaneler (R `pwr.t2n.test`, Python `statsmodels`) kesirli $N$ verirken, G*Power'ın tamsayı $n_1, n_2$ arayıp gücü güncelleyerek basması arasındaki farkın sebebi bu tavan yuvarlama adımıdır.

### 5.2 İterasyon ve Arama Algoritması
- `[REA]` G*Power normal dağılım yaklaşımı ($z$-testi) ile bir başlangıç $n_{\text{init}}$ kestirir:
  $$n_{\text{init}} \approx \frac{(z_{1-\alpha} + z_{1-\beta})^2}{d^2} \cdot \frac{1 + ratio}{ratio}$$
- `[REA]` Bu başlangıç noktasından itibaren yönlü arama (bisection veya incremental search) ile hedef gücü sağlayan en küçük tamsayı $n_1$ aranır.
- `[REA]` Durma kriteri: $\text{actual\_power} \ge \text{target\_power}$.

### 5.3 Sınır Değerler ve Geçersiz Girdi Davranışı
- `[REA]` Serbestlik derecesi kısıtı: Her grupta en az 2 denek bulunmalıdır ($n_1 \ge 2, n_2 \ge 2 \implies N \ge 4, df \ge 2$).
- `[REA]` $d \le 0$ girildiğinde `INVALID_INPUT` / `OUT_OF_RANGE` hatası tetiklenir; etki büyüklüğü kesinlikle pozitif olmalıdır.
- `[REA]` $\alpha \le 0$ veya $\alpha \ge 1$, $\text{power} \le 0$ veya $\text{power} \ge 1$ reddedilir.
- `[REA]` $\text{power} \le \alpha$ durumu mantıksal tutarsızlıktır (`INCONSISTENT`), çünkü hiçbir testin gücü I. tip hata düzeyinden düşük olamaz.
