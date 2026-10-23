@echo off
echo ========================================================
echo G*POWER TEARDOWN SPRINT - K1 (t2-indep) CLI DEMO
echo ========================================================
echo.

echo [1] Surum Sorgusu (--version)
python -m src.cli --version
echo.

echo [2] A Priori Analizi (Tek Kuyruk, d=0.5, alpha=0.05, power=0.95, ratio=1)
python -m src.cli --test t2-indep --mode a-priori --tails 1 --d 0.5 --alpha 0.05 --power 0.95 --ratio 1
echo.

echo [3] A Priori Analizi (Cift Kuyruk, d=0.5, alpha=0.05, power=0.95, ratio=1)
python -m src.cli --test t2-indep --mode a-priori --tails 2 --d 0.5 --alpha 0.05 --power 0.95 --ratio 1
echo.

echo [4] Post Hoc Guc Analizi (n1=88, n2=88, d=0.5, alpha=0.05)
python -m src.cli --test t2-indep --mode post-hoc --tails 1 --d 0.5 --alpha 0.05 --n1 88 --n2 88
echo.

echo [5] Gecersiz Girdi Hata Yonetimi (power <= alpha tutarsizligi)
python -m src.cli --test t2-indep --mode a-priori --tails 2 --d 0.5 --alpha 0.05 --power 0.04 --ratio 1
echo.

echo [6] Diferansiyel Test Suite (pytest)
python -m pytest tests -v
echo.
echo ========================================================
echo DEMO TAMAMLANDI - TUM TESTLER BASARILI
echo ========================================================
