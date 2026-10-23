# HALLUCINATIONS.md — Halüsinasyon ve Hata Analizi Günlüğü

Bu belge, tersine mühendislik ve geliştirme sürecinde ajanın başlangıçta yanlış çıkardığı, varsaydığı veya halüsinasyon gördüğü en az iki kritik durumu, bunların nasıl fark edildiğini ve hangi diferansiyel testlerle yakalandığını belgeler.

---

### Halüsinasyon 1: Eşit Olmayan Gruplarda Örneklem Yuvarlama Mantığı (Round vs. Ceil)

* **Ajanın Yanlış İddiası:**  
  Ajan, G*Power'ın allocation ratio ($ratio = N_2/N_1 \neq 1$) durumunda hedef $N_{\text{total}}$ değerini sürekli formülle hesaplayıp $n_1 = \text{round}(N / (1 + ratio))$ ve $n_2 = N - n_1$ şeklinde en yakın tamsayıya yuvarladığını iddia etti.
* **Nasıl Fark Edildi?**  
  $ratio = 2.0$ ve $ratio = 1.5$ senaryolarında G*Power GUI'sinde hesaplanan $N$ değerleri ile motorun ürettiği $N$ değerleri karşılaştırıldığında, motorda $N$ değerinin 1-2 denek eksik kaldığı ve hesaplanan gücün hedeflenen gücün altında (%79.4 gibi) kaldığı görüldü.
* **Hangi Test Yakaladı?**  
  `tests/test_differential.py::TestBoundaryAndUnequalRatios::test_unequal_ratio_a_priori`
* **Doğru Davranış ve Düzeltme:**  
  Ghidra ve kâhin diferansiyel testiyle kanıtlandı ki: G*Power aramayı doğrudan $n_1$ tamsayısı üzerinden artırarak yürütür ve her adımda $n_2 = \lceil n_1 \cdot ratio \rceil$ (tavan / `ceil`) uygular. $\text{actual\_power} \ge \text{target\_power}$ şartını sağlayan ilk $(n_1, n_2)$ çifti seçilir. Bu sayede Grup 2'deki denek oranı hedeflenen tahsis oranının asla altına düşmez.

---

### Halüsinasyon 2: Çift Kuyruklu Testte İkinci Kritik Bölge Olasılığının İhmali

* **Ajanın Yanlış İddiası:**  
  Ajan, çift kuyruklu bağımsız örneklem t-testinde ($\text{tails} = 2$) gücün sadece sağ kuyruk ret bölgesi olan $1 - T_{df, \delta}(t_{\text{crit}})$ formülüyle hesaplanabileceğini, sol kuyruk olasılığının ($T_{df, \delta}(-t_{\text{crit}})$) $\delta > 0$ iken tamamen $0$ sayılabileceğini öne sürdü.
* **Nasıl Fark Edildi?**  
  Standart senaryolarda ($d=0.5, N > 100$) fark $10^{-8}$ düzeyinde kaldığı için fark edilmedi; ancak sınır değer testlerinde (küçük etki $d=0.1$ ve küçük örneklem $N=10$) G*Power'ın `actual_power` değeri ile motorun değeri arasında $10^{-5}$ mertebesinde sapma oluştu ve hocanın sözleşmesindeki $10^{-6}$ toleransı aşıldı.
* **Hangi Test Yakaladı?**  
  `tests/test_differential.py::TestBoundaryAndUnequalRatios::test_two_tailed_a_priori` ve sınır değer analizleri.
* **Doğru Davranış ve Düzeltme:**  
  G*Power'ın çift kuyruklu testlerde gücü iki yönlü ret bölgesinin toplamı olarak hesapladığı kanıtlandı:
  $$\text{power} = (1 - T_{df, \delta}(t_{\text{crit}})) + T_{df, \delta}(-t_{\text{crit}})$$
  Motor bu formülle güncellendiğinde sapma $10^{-7}$ seviyesinin altına indi.

---

### Halüsinasyon 3: Sensitivity Modunda Çift Kuyruk Yön Parametresi

* **Ajanın Yanlış İddiası:**  
  Ajan, sensitivity analizinde çift kuyruk için hem pozitif hem negatif $d$ değerlerinin aranması gerektiğini ve CLI'da bir yön bayrağı olması gerektiğini iddia etti.
* **Nasıl Fark Edildi?**  
  `CONTRACT.md` sözleşmesi incelendiğinde: *"Sensitivity modunda G*Power yalnızca d ≥ 0 yönünü hesaplar. Sözleşmede yön parametresi yoktur."* kuralı görüldü.
* **Hangi Test Yakaladı?**  
  `tests/test_differential.py::TestContractVectors::test_sensitivity`
* **Doğru Davranış ve Düzeltme:**  
  Arama aralığı yalnızca $d \in (0, \infty)$ olarak kısıtlandı ve sözleşmeye tam uyum sağlandı.
