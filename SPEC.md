# SPEC.md — `t2-indep` Fonksiyonel Kabul Şartnamesi (Gherkin Formatında)

**Sözleşme Sürümü:** 1.0.0  
**Test Ailesi:** K1 — `t2-indep` (Means: Difference between two independent means)  
**Referans Kâhin:** G*Power 3.1.9.7 Windows (SHA-256: `c63e6a133eb6372932f810c08cc33dc35a06d1ddb658f897bd6c34a754efc812`)  

---

## Özellik: İki Bağımsız Ortalama İçin t-Testi Hesaplama Motoru (`t2-indep`)

Klinik ve davranışsal araştırmalarda iki bağımsız grubun (örn. Deney/İlaç ve Kontrol/Plasebo) ortalama farklarını test eden t-testinin örneklem büyüklüğü, gücü ve etki parametreleri hesaplanır.

---

### Senaryo 1: A Priori Örneklem Büyüklüğü Hesabı (Eşit Gruplar, Tek Kuyruk)
  **Diyelim ki** test ailesi "t2-indep" ve analiz modu "a-priori" olarak seçildi  
  **Ve** hipotez yönü "tails" = 1 (tek kuyruk)  
  **Ve** etki büyüklüğü "d" = 0.5  
  **Ve** I. tip hata "alpha" = 0.05  
  **Ve** hedef güç "power" = 0.95  
  **Ve** denek tahsis oranı "ratio" = 1.0  
  **Hesaplandığında**  
  **O zaman** Grup 1 denek sayısı "n1" = 88 olmalıdır  
  **Ve** Grup 2 denek sayısı "n2" = 88 olmalıdır  
  **Ve** toplam denek sayısı "n_total" = 176 olmalıdır  
  **Ve** serbestlik derecesi "df" = 174 olmalıdır  
  **Ve** noncentrality parametresi "ncp" mutlak farkı 1e-6 toleransıyla 3.3166248 olmalıdır  
  **Ve** kritik t değeri "critical_t" mutlak farkı 1e-6 toleransıyla 1.6536580 olmalıdır  
  **Ve** gerçekleşen güç "actual_power" 0.9514254 olmalıdır (ve hedef güç 0.95'ten büyük veya eşit olmalıdır)

---

### Senaryo 2: A Priori Örneklem Büyüklüğü Hesabı (Eşit Gruplar, Çift Kuyruk)
  **Diyelim ki** test ailesi "t2-indep" ve analiz modu "a-priori" olarak seçildi  
  **Ve** hipotez yönü "tails" = 2 (çift kuyruk)  
  **Ve** etki büyüklüğü "d" = 0.5  
  **Ve** I. tip hata "alpha" = 0.05  
  **Ve** hedef güç "power" = 0.95  
  **Ve** denek tahsis oranı "ratio" = 1.0  
  **Hesaplandığında**  
  **O zaman** Grup 1 denek sayısı "n1" = 105 olmalıdır  
  **Ve** Grup 2 denek sayısı "n2" = 105 olmalıdır  
  **Ve** toplam denek sayısı "n_total" = 210 olmalıdır  
  **Ve** serbestlik derecesi "df" = 208 olmalıdır  
  **Ve** kritik t değeri "critical_t" mutlak farkı 1e-6 toleransıyla 1.9714347 olmalıdır  
  **Ve** noncentrality parametresi "ncp" mutlak farkı 1e-6 toleransıyla 3.6228442 olmalıdır  
  **Ve** gerçekleşen güç "actual_power" mutlak farkı 1e-6 toleransıyla 0.9501460 olmalıdır

---

### Senaryo 3: A Priori Örneklem Büyüklüğü Hesabı (Eşit Olmayan Gruplar, Tavan Yuvarlama Kuralı)
  **Diyelim ki** test ailesi "t2-indep" ve analiz modu "a-priori" olarak seçildi  
  **Ve** hipotez yönü "tails" = 2 (çift kuyruk)  
  **Ve** etki büyüklüğü "d" = 0.5  
  **Ve** I. tip hata "alpha" = 0.05  
  **Ve** hedef güç "power" = 0.80  
  **Ve** denek tahsis oranı "ratio" = 2.0 (Grup 2, Grup 1'in 2 katı)  
  **Hesaplandığında**  
  **O zaman** "n1" tam sayısı ve "n2" tam sayısı hesaplanmalıdır  
  **Ve** "n2" değeri ceil(n1 * ratio) formülüyle tam sayıya tamamlanmalıdır  
  **Ve** "n_total" = n1 + n2 olmalıdır  
  **Ve** gerçekleşen güç "actual_power" >= 0.80 olmalıdır

---

### Senaryo 4: Post Hoc Güç Analizi (Gözlenen Örneklem ile Güç Tespiti)
  **Diyelim ki** test ailesi "t2-indep" ve analiz modu "post-hoc" olarak seçildi  
  **Ve** hipotez yönü "tails" = 1 (tek kuyruk)  
  **Ve** etki büyüklüğü "d" = 0.5  
  **Ve** I. tip hata "alpha" = 0.05  
  **Ve** Grup 1 denek sayısı "n1" = 88  
  **Ve** Grup 2 denek sayısı "n2" = 88  
  **Hesaplandığında**  
  **O zaman** serbestlik derecesi "df" = 174 olmalıdır  
  **Ve** noncentrality parametresi "ncp" mutlak farkı 1e-6 toleransıyla 3.3166248 olmalıdır  
  **Ve** kritik t değeri "critical_t" mutlak farkı 1e-6 toleransıyla 1.6536580 olmalıdır  
  **Ve** hesaplanan güç "power" mutlak farkı 1e-6 toleransıyla 0.9514254 olmalıdır

---

### Senaryo 5: Compromise Analiz Modu
  **Diyelim ki** test ailesi "t2-indep" ve analiz modu "compromise" olarak seçildi  
  **Ve** hipotez yönü "tails" = 1  
  **Ve** etki büyüklüğü "d" = 0.5  
  **Ve** beta / alpha hata oranı "beta_alpha_ratio" = 1.0  
  **Ve** "n1" = 88 ve "n2" = 88  
  **Hesaplandığında**  
  **O zaman** "alpha" ve "beta" değerleri eşit olmalıdır (0.0492887 tolerans 1e-6)  
  **Ve** "power" = 1 - beta = 0.9507113 olmalıdır  
  **Ve** kritik değer "critical_t" = 1.6606859 olmalıdır

---

### Senaryo 6: Criterion Analiz Modu
  **Diyelim ki** test ailesi "t2-indep" ve analiz modu "criterion" olarak seçildi  
  **Ve** hipotez yönü "tails" = 1, "d" = 0.5, "power" = 0.95, "n1" = 88, "n2" = 88  
  **Hesaplandığında**  
  **O zaman** "alpha" mutlak farkı 1e-6 toleransıyla 0.0485965 olmalıdır  
  **Ve** "critical_t" = 1.6676050 olmalıdır

---

### Senaryo 7: Sensitivity Analiz Modu (Saptanabilir Minimum Etki Büyüklüğü)
  **Diyelim ki** test ailesi "t2-indep" ve analiz modu "sensitivity" olarak seçildi  
  **Ve** hipotez yönü "tails" = 1, "alpha" = 0.05, "power" = 0.95, "n1" = 88, "n2" = 88  
  **Hesaplandığında**  
  **O zaman** saptanabilir etki büyüklüğü "d" mutlak farkı 1e-6 toleransıyla 0.4978840 olmalıdır  
  **Ve** "critical_t" = 1.6536580 olmalıdır

---

### Senaryo 8: Geçersiz Girdi ve Sınır Değer Doğrulaması (Hata Yönetimi)
  **Diyelim ki** geçersiz parametre girildi:
    | Durum | Parametreler | Beklenen Hata Kodu |
    |---|---|---|
    | tails geçersiz | `--tails 3` | `OUT_OF_RANGE` |
    | alpha sınır dışı | `--alpha 0.0` veya `--alpha 1.0` | `OUT_OF_RANGE` |
    | power sınır dışı | `--power 0.0` veya `--power 1.0` | `OUT_OF_RANGE` |
    | etki büyüklüğü d negatif | `--d -0.5` | `OUT_OF_RANGE` |
    | örneklem çok küçük | `--n1 1` veya `--n2 1` | `OUT_OF_RANGE` |
    | tutarsız güç | `--power 0.04 --alpha 0.05` | `INCONSISTENT` |
    | eksik parametre | `--mode a-priori` (alpha verilmedi) | `MISSING_PARAM` |
    | tanımsız parametre | `--mode post-hoc --power 0.95` | `UNKNOWN_PARAM` |
  **O zaman** standart hata JSON nesnesi dönülmelidir:
    ```json
    {"error": "<insan tarafından okunabilir açıklama>", "code": "<HATA_KODU>", "field": "<alan_adı>"}
    ```
  **Ve** sıfırdan farklı çıkış kodu verilmelidir (`2`: geçersiz girdi / kural hatası, `1`: hesaplama hatası).
