# Oturum 2: Temiz Oda Yeniden Yazım Prompt'u (Session 2 Prompt)

## Görev
G*Power 3.1.9.7 `t2-indep` hesaplama motorunu ve `gpower-clone` CLI arayüzünü temiz oda prensibiyle yeniden yaz.

## Kurallar ve Kısıtlar
1. İkili dosya (GPowerNT.exe), Ghidra veya decompile çıktıları kesinlikle görülmeyecek / kullanılmayacak.
2. Girdi kaynağı YALNIZCA `SPEC.md` ve `CONTRACT.md` arayüz sözleşmesidir.
3. Hesaplama mantığı tek bir motorda (`src/engine.py`) toplanacak; CLI (`src/cli.py`) ve bonus katmanlar (MCP sunucusu) bu motoru çağıran ince katmanlar olacaktır.
4. CLI arayüzü `CONTRACT.md`'ye tam uyumlu olacaktır:
   - Komut: `gpower-clone --test t2-indep --mode <mode> [...]`
   - Başarılı çıktı: `stdout`'a tek satır JSON, çıkış kodu `0`.
   - Hata çıktısı: `{"error": "...", "code": "...", "field": "..."}` ve sıfırdan farklı çıkış kodu (`2` geçersiz girdi, `1` iç hata).
   - Tam sayılar (`n1`, `n2`, `n_total`, `df`) kesinlikle JSON int formatında basılacak.
5. Dağılım fonksiyonları için `scipy.stats` (örneğin `nct`, `t`) kullanılabilir; ancak N arama algoritması, yuvarlama kuralları ve parametre türetimleri motorda temiz olarak kodlanacaktır.
6. Gizli test vektörlerinde N değerleri en az %90 tam eşleşmeli, ondalık değerler $10^{-6}$ toleransında kalmalıdır.

## Çıktı Hedefleri
- `src/engine.py`: İki bağımsız grup t-testi hesaplama motoru.
- `src/cli.py`: Sözleşmeye tam uyumlu CLI arayüzü.
- `tests/test_engine.py`: Birim testleri ve diferansiyel test suite'i.
