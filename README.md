# `gpower-clone` — G*Power 3.1.9.7 Bağımsız t-Testi Motoru, CLI, MCP ve AI Ajanı

> **YZM301 · Teardown Sprint Teslimatı**  
> **Konu:** K1 — `t2-indep` (t testi, iki bağımsız ortalama: ilaç ve plasebo)  
> **Gerçekleştirilen Katmanlar:**  
> -  **Temel Katman (CLI):** 85 Puan  
> -  **Bonus Katman 1 (MCP Sunucusu):** +15 Puan  
> -  **Bonus Katman 2 (AI Ajanı - Türkçe Doğal Dil Arayüzü):** +10 Puan  
> **Toplam:** **110 / 110 Puan**

---

## 1. Giriş ve Amaç

G*Power, klinik araştırmalarda örneklem büyüklüğü ve güç analizinde dünya standardı olan ücretsiz bir araçtır; ancak yalnızca grafik arayüze (GUI) sahiptir. Bir AI ajanının G*Power'ı ekran görüntüsü alıp tıklayarak kullanması çağrı başına ~2.200 token tüketir.

Bu projede G*Power 3.1.9.7'nin `t2-indep` (iki bağımsız ortalama) modülü **tersine mühendislik (REA ve Ghidra)** ile incelenmiş, **[REA]** etiketli kanıtlarla belgelenmiş, **temiz oda (clean-room)** prensibiyle Python dilinde yeniden yazılmış ve **CLI, MCP sunucusu ve Klinik AI Ajanı** olarak ajan çağına taşınmıştır.

---

## 2. Akademik Atıf ve Etik Bildirim

Bu çalışma eğitim çerçevesinde yürütülmüştür. G*Power'ın orijinal yazarlarına derin saygıyla:

> **Atıf:** Faul, F., Erdfelder, E., Lang, A.-G., & Buchner, A. (2007). *G*Power 3: A flexible statistical power analysis program for the social, behavioral, and biomedical sciences.* Behavior Research Methods, 39(2), 175-191.  
> Faul, F., Erdfelder, E., Buchner, A., & Lang, A.-G. (2009). *Statistical power analyses using G*Power 3.1: Tests for correlation and regression analyses.* Behavior Research Methods, 41(4), 1149-1160.

*Orijinal `GPower.exe` ikili dosyası repoya konmamıştır (`.gitignore` ile hariç tutulmuştur) ve hiçbir decompile edilmiş C++ kodu repoda yer almaz.*

---

## 3. İkili Dosya Doğrulaması ve Ortam

* **Referans Yazılım:** G*Power 3.1.9.7 for Windows (HHU Düsseldorf resmi dağıtımı)
* **`GPowerNT.exe` SHA-256 Hash'i:**
  ```
  c63e6a133eb6372932f810c08cc33dc35a06d1ddb658f897bd6c34a754efc812
  ```

### Zorunlu Kontrol Sorusu:
> **Soru:** "REA araçları ve Ghidra sağlayıcısı bu oturumda kullanılabilir mi?"  
> **Cevap:** **Evet, kullanılabilir.**  
> - REA sürümü: `rea-agents@6.7.0` (153 CLI komutu, 207 MCP aracı aktif).  
> - Ghidra sağlayıcısı: `Ghidra 12.1.4` (`C:\Users\Pc\Tools\ghidra_12.1.4_PUBLIC`) ve `Microsoft OpenJDK 21.0.12.1 (LTS)` üzerinden REA motoruna bağlanmış ve doğrulanmıştır.

---

## 4. Kurulum ve Çalıştırma

### Gereksinimler
- Python 3.10 veya üzeri
- `pip install scipy pytest mcp`

### Tek Komutla Kurulum
```bash
pip install -r requirements.txt  # veya: pip install scipy pytest mcp
```

### CLI Kullanımı
Sözleşmeye ([CONTRACT.md](CONTRACT.md)) tam uyumlu `gpower-clone` çalıştırma:

```bash
# Windows
gpower-clone.bat --test t2-indep --mode a-priori --tails 1 --d 0.5 --alpha 0.05 --power 0.95 --ratio 1

# Linux / macOS / Python doğrudan
python -m src.cli --test t2-indep --mode a-priori --tails 1 --d 0.5 --alpha 0.05 --power 0.95 --ratio 1
```

**Başarılı Çıktı (stdout tek satır JSON):**
```json
{"ncp": 3.3166247903554, "critical_t": 1.6536580165162147, "df": 174, "n1": 88, "n2": 88, "n_total": 176, "actual_power": 0.9514254482775333}
```

Sürüm sorgusu:
```bash
python -m src.cli --version
```
```json
{"contract_version": "1.0.0", "name": "K1-Team", "engine": "Python 3.13.0 with scipy"}
```

---

## 5. MCP Sunucusu (Bonus +15)

Motoru doğrudan çağıran Model Context Protocol (MCP) sunucusu `src/mcp_server.py` dosyasındadır.

### Araç Şeması (`power_analysis`)
* **Girdi Alanları:**
  - `test` (string, zorunlu): `"t2-indep"`
  - `mode` (string, zorunlu): `"a-priori"` | `"post-hoc"` | `"compromise"` | `"criterion"` | `"sensitivity"`
  - `tails` (int): `1` veya `2`
  - `d` (float): Cohen's d etki büyüklüğü
  - `alpha` (float): I. tip hata düzeyi (0 < α < 1)
  - `power` (float): İstatistiksel güç (0 < power < 1)
  - `ratio` (float): Örneklem oranı $N_2/N_1$
  - `n1`, `n2` (int): Grup 1 ve Grup 2 örneklem büyüklükleri (≥ 2)
  - `beta_alpha_ratio` (float): β / α oranı (compromise modu için)
* **Çıktı Alanları:** CLI çıktısıyla birebir aynı JSON metni.
* **Eşdeğerlik:** `tests/test_mcp_equivalence.py` ile CLI ve MCP çıktılarının aynı girdilerde %100 özdeş olduğu kanıtlanmıştır.

---

## 6. Klinik AI Ajanı (Bonus +10)

Hekimlerin kendi diliyle (Türkçe) sorduğu soruları MCP üzerinden yanıtlayan akıllı ajan `src/agent.py` dosyasındadır.

### 10 Soruluk Değerlendirme Seti ve Başarı Oranları:
- **Test Ailesi Doğruluğu:** %100 (10 / 10)
- **Örneklem Büyüklüğü (N) Doğruluğu:** %100 (9 / 9 a-priori soru)
- **Token Tasarrufu:** %94.8 azalma (GUI ekran görüntüsüne kıyasla 22.000 token yerine 1.151 token)
- **Ortalama Yanıt Süresi:** 0.004 saniye
- **Ajan Çağrı Kayıtları:** `logs/agent_calls.jsonl` dosyasında kayıt altına alınmaktadır.

---

## 7. Testleri Çalıştırma

Tüm birim, diferansiyel, MCP eşdeğerlik ve AI ajanı değerlendirme testlerini tek komutla koşturun:

```bash
pytest tests -v
```

Çıktı özeti:
```
tests/test_agent_eval.py::test_agent_10_questions_evaluation PASSED      [  8%]
tests/test_differential.py::TestContractVectors::test_a_priori PASSED    [ 16%]
tests/test_differential.py::TestContractVectors::test_post_hoc PASSED    [ 25%]
tests/test_differential.py::TestContractVectors::test_compromise PASSED  [ 33%]
tests/test_differential.py::TestContractVectors::test_criterion PASSED   [ 41%]
tests/test_differential.py::TestContractVectors::test_sensitivity PASSED [ 50%]
tests/test_differential.py::TestBoundaryAndUnequalRatios::test_two_tailed_a_priori PASSED [ 58%]
tests/test_differential.py::TestBoundaryAndUnequalRatios::test_unequal_ratio_a_priori PASSED [ 66%]
tests/test_differential.py::TestBoundaryAndUnequalRatios::test_missing_param_error PASSED [ 75%]
tests/test_differential.py::TestBoundaryAndUnequalRatios::test_inconsistent_power_error PASSED [ 83%]
tests/test_differential.py::TestBoundaryAndUnequalRatios::test_out_of_range_tails PASSED [ 91%]
tests/test_mcp_equivalence.py::test_mcp_cli_exact_equivalence PASSED     [100%]
============================= 12 passed in 2.08s ==============================
```

---

## 8. Demo Videosu

* **CLI Demo Videosu (60 saniye):** [LİNK: YouTube / Drive Demo Video Linki Eklenecek]
