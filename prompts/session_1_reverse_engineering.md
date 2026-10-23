# Oturum 1: Tersine Mühendislik ve Kanıt Defteri Çıkarma Prompt'u (Session 1 Prompt)

## Görev
G*Power 3.1.9.7 (GPowerNT.exe) ikili dosyasını REA ve Ghidra kullanarak incele.
Konumuz: **K1 — t testi, iki bağımsız ortalama (ilaç ve plasebo) / `t2-indep`**.

## Kurallar ve Kısıtlar
1. Yalnızca `SPEC.md` ve `LEDGER.md` üretilecek; hiçbir kaynak kod yazılmayacak.
2. Kod decompile çıktıları doğrudan repoya konmayacak. Kanıt defterinde sadece fonksiyon adresleri, assembly buyrukları ve dize (string) referansları yer alacak.
3. Her iddia mutlaka etiketlenecek:
   - `[DOK]`: Kılavuzda veya makalelerde yazılı olan bilgi.
   - `[REA]`: İkili dosyadan (Ghidra/REA) bellek adresi veya sembolle kanıtlanmış bilgi.
   - `[AJAN]`: Ajanın doğrudan kanıtı olmayan varsayımı / çıkarımı.
4. Kılavuzda OLMAYAN davranışları ara:
   - Örneklem boyutunun tamsayıya yuvarlanma kuralı (ceil / floor / round).
   - Eşit olmayan oranlarda ($ratio \neq 1$) $n_1$ ve $n_2$ dağılımı.
   - İteratif N arama algoritması ve durma toleransı ($\epsilon$).
   - Serbestlik derecesi ($df$) hesaplama anı ve formülü.
   - Non-centrality parameter (NCP, $\delta$) formülü.
   - Sınır değerlerde ve geçersiz girdilerde verilen tepkiler.

## Çıktı Hedefleri
- `LEDGER.md`: Kanıt defteri.
- `SPEC.md`: Gherkin formatında (`Given - When - Then`) hazırlanmış, kabul kriterlerini içeren spesifikasyon belgesi.
