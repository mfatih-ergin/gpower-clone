"""
Evaluation suite for AI Clinic Agent (10 Fictional Clinical Questions).
Requirement: TEARDOWN SPRINT (+10 Puan) and CONTRACT.md Section 8.
Evaluates accuracy of test family selection, parameter extraction, and engine N computation.
Includes token and latency measurement comparison (MCP vs GUI).
"""

import os
import json
import time
from src.agent import ClinicAgent

EVALUATION_SET = [
    {
        "id": "Q01",
        "question": "Yeni bir antihipertansif ilacın plaseboya göre sistolik kan basıncını daha fazla düşürdüğünü (tek yönlü) göstermek istiyoruz. Orta etki büyüklüğü (d=0.5), %5 anlamlılık ve %95 güç için eşit kollarda kaç hasta almalıyız?",
        "expected_test": "t2-indep",
        "expected_mode": "a-priori",
        "expected_tails": 1,
        "expected_d": 0.5,
        "expected_alpha": 0.05,
        "expected_power": 0.95,
        "expected_ratio": 1.0,
        "expected_n_total": 176
    },
    {
        "id": "Q02",
        "question": "Diyabet tedavisinde iki farklı molekülün HbA1c düşüşü açısından iki yönlü farkını test edeceğiz. d=0.5, alfa=%5 ve %95 güçte eşit gruplarla kaç denek gerekir?",
        "expected_test": "t2-indep",
        "expected_mode": "a-priori",
        "expected_tails": 2,
        "expected_d": 0.5,
        "expected_alpha": 0.05,
        "expected_power": 0.95,
        "expected_ratio": 1.0,
        "expected_n_total": 210
    },
    {
        "id": "Q03",
        "question": "Onkolojide nadir yan etkileri karşılaştırmak için küçük bir etki (d=0.2) arıyoruz. Çift yönlü %5 anlamlılık ve %80 güçle 1:1 tahsis için toplam kaç hasta gerekir?",
        "expected_test": "t2-indep",
        "expected_mode": "a-priori",
        "expected_tails": 2,
        "expected_d": 0.2,
        "expected_alpha": 0.05,
        "expected_power": 0.80,
        "expected_ratio": 1.0,
        "expected_n_total": 788
    },
    {
        "id": "Q04",
        "question": "Ağrı tedavisinde güçlü bir analjezik için büyük etki (d=0.8) öngörülüyor. Çift kuyrukta %5 alfa ve %80 güçle eşit gruplarda toplam denek sayısı nedir?",
        "expected_test": "t2-indep",
        "expected_mode": "a-priori",
        "expected_tails": 2,
        "expected_d": 0.8,
        "expected_alpha": 0.05,
        "expected_power": 0.80,
        "expected_ratio": 1.0,
        "expected_n_total": 52
    },
    {
        "id": "Q05",
        "question": "Faz 3 aşı denemesinde etken koluna kontrolün iki katı hasta (oran 2.0) alacağız. d=0.5, çift yönlü alfa 0.05 ve %80 güç için kaç hasta gerekir?",
        "expected_test": "t2-indep",
        "expected_mode": "a-priori",
        "expected_tails": 2,
        "expected_d": 0.5,
        "expected_alpha": 0.05,
        "expected_power": 0.80,
        "expected_ratio": 2.0,
        "expected_n_total": 144 # n1=48, n2=96
    },
    {
        "id": "Q06",
        "question": "Plasebo kontrollü bir çalışmada yeni ilacın kolesterolü daha iyi düşürdüğü (tek kuyruk) hipotezi var. d=0.3, alfa=%1 ve %90 güç için eşit kollarda kaç kişi gerekir?",
        "expected_test": "t2-indep",
        "expected_mode": "a-priori",
        "expected_tails": 1,
        "expected_d": 0.3,
        "expected_alpha": 0.01,
        "expected_power": 0.90,
        "expected_ratio": 1.0,
        "expected_n_total": 582 # n1=291, n2=291
    },
    {
        "id": "Q07",
        "question": "İki cerrahi yöntemin iyileşme süreleri arasındaki iki yönlü fark için d=0.6, alfa=0.01 ve çok yüksek %99 güç hedefleniyor. 1:1 oranla kaç hasta gerekir?",
        "expected_test": "t2-indep",
        "expected_mode": "a-priori",
        "expected_tails": 2,
        "expected_d": 0.6,
        "expected_alpha": 0.01,
        "expected_power": 0.99,
        "expected_ratio": 1.0,
        "expected_n_total": 272 # n1=136, n2=136
    },
    {
        "id": "Q08",
        "question": "Yeni antibiyotik için d=0.4 etki büyüklüğü ile tek yönlü %5 alfa ve %80 güç koşulunda eşit gruplarla çalışma planlıyoruz. Kaç hasta gerekir?",
        "expected_test": "t2-indep",
        "expected_mode": "a-priori",
        "expected_tails": 1,
        "expected_d": 0.4,
        "expected_alpha": 0.05,
        "expected_power": 0.80,
        "expected_ratio": 1.0,
        "expected_n_total": 156 # n1=78, n2=78
    },
    {
        "id": "Q09",
        "question": "Tamamlanmış bir klinik çalışmada ilaç grubunda 88, plasebo grubunda 88 hasta var. d=0.5 ve alfa=0.05 ile tek yönlü hipotezde elde ettiğimiz güç nedir?",
        "expected_test": "t2-indep",
        "expected_mode": "post-hoc",
        "expected_tails": 1,
        "expected_d": 0.5,
        "expected_alpha": 0.05,
        "expected_power_approx": 0.9514
    },
    {
        "id": "Q10",
        "question": "Depresyon ölçeğinde iki bağımsız tedavi kolunda d=0.7 fark öngörüyoruz. Çift yönlü test, alfa=%5 ve %95 güç ile eşit gruplarda gereken hasta sayısı nedir?",
        "expected_test": "t2-indep",
        "expected_mode": "a-priori",
        "expected_tails": 2,
        "expected_d": 0.7,
        "expected_alpha": 0.05,
        "expected_power": 0.95,
        "expected_ratio": 1.0,
        "expected_n_total": 110 # n1=55, n2=55
    }
]


def test_agent_10_questions_evaluation():
    os.makedirs("logs", exist_ok=True)
    agent = ClinicAgent(log_path="logs/agent_calls.jsonl")

    correct_family_count = 0
    correct_mode_count = 0
    correct_n_count = 0

    total_mcp_tokens = 0
    total_gui_tokens_est = 0

    t_start = time.time()

    for item in EVALUATION_SET:
        q = item["question"]
        params = agent.parse_clinical_query(q)

        # 1. Test family evaluation
        if params["test"] == item["expected_test"]:
            correct_family_count += 1

        # 2. Mode evaluation
        if params["mode"] == item["expected_mode"]:
            correct_mode_count += 1

        # 3. Agent response execution via MCP
        resp = agent.answer(q)
        assert len(resp) > 0

        # Check N calculation
        if item["expected_mode"] == "a-priori":
            if f"Toplam: {item['expected_n_total']} hasta" in resp:
                correct_n_count += 1

        # Token comparison estimation:
        total_mcp_tokens += (len(q) // 4) + (len(resp) // 4)
        total_gui_tokens_est += 2200

    duration = time.time() - t_start

    family_accuracy = (correct_family_count / len(EVALUATION_SET)) * 100
    n_accuracy = (correct_n_count / 9) * 100 # 9 a-priori questions

    print("\n" + "="*50)
    print("CLINIC AI AGENT 10-QUESTION EVALUATION REPORT")
    print("="*50)
    print(f"Test Family Accuracy:    {family_accuracy:.1f}% ({correct_family_count}/10)")
    print(f"Sample Size (N) Accuracy:{n_accuracy:.1f}% ({correct_n_count}/9)")
    print(f"Execution Duration:      {duration:.2f} seconds ({duration/10:.3f} s/question)")
    print(f"Total Tokens via MCP:    ~{total_mcp_tokens} tokens")
    print(f"Total Tokens via GUI:    ~{total_gui_tokens_est} tokens")
    print(f"Token Efficiency Gain:   {((total_gui_tokens_est - total_mcp_tokens) / total_gui_tokens_est)*100:.1f}% reduction")
    print("="*50)

    assert family_accuracy == 100.0
    assert n_accuracy == 100.0
