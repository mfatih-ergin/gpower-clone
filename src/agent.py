"""
Clinic AI Agent answering natural language medical research queries via MCP tool.
Requirement: TEARDOWN SPRINT Bonus (+10 Puan) and CONTRACT.md Section 8.
"""

import re
import json
import datetime
from typing import Dict, Any, Tuple
from src.mcp_server import power_analysis


class ClinicAgent:
    """
    Interprets clinical trial design questions in Turkish, extracts parameters,
    calls the MCP tool 'power_analysis', and logs queries into logs/agent_calls.jsonl.
    The agent NEVER computes N itself; all numbers derive from the engine.
    """

    def __init__(self, log_path: str = "logs/agent_calls.jsonl"):
        self.log_path = log_path

    def parse_clinical_query(self, query: str) -> Dict[str, Any]:
        q_lower = query.lower()

        # 1. Test family identification
        if "bağımsız" in q_lower or "ilaç ve plasebo" in q_lower or "iki grup" in q_lower or "tedavi ve kontrol" in q_lower:
            test = "t2-indep"
        else:
            test = "t2-indep"

        # 2. Mode identification
        if "kaç hasta" in q_lower or "kaç denek" in q_lower or "örneklem boyutu" in q_lower or "kaç kişi" in q_lower:
            mode = "a-priori"
        elif "güç nedir" in q_lower or "gücü nedir" in q_lower or "güç ne kadar" in q_lower or "gücü hesapla" in q_lower:
            mode = "post-hoc"
        elif "minimum etki" in q_lower or "en küçük fark" in q_lower or "hassasiyet" in q_lower:
            mode = "sensitivity"
        else:
            mode = "a-priori"

        # 3. Tails (Hypothesis direction)
        if "daha iyi" in q_lower or "üstün" in q_lower or "azaltır" in q_lower or "artırır" in q_lower or "tek yön" in q_lower or "tek kuyruk" in q_lower:
            tails = 1
        else:
            tails = 2

        # 4. Effect size d
        d_match = re.search(r"(?:d\s*[=:]\s*|etki(?:\s*büyüklüğü)?\s*[=:]?\s*)([0-9]+(?:[\.,][0-9]+)?)", q_lower)
        if d_match:
            d_val = float(d_match.group(1).replace(",", "."))
        elif "küçük etki" in q_lower:
            d_val = 0.2
        elif "büyük etki" in q_lower:
            d_val = 0.8
        elif "orta etki" in q_lower:
            d_val = 0.5
        else:
            d_val = 0.5

        # 5. Alpha
        # Matches "alfa=%5", "alpha 0.05", "%5 anlamlılık", "%1 alfa"
        alpha_match = re.search(r"(?:alpha|alfa|anlamlılık|tip\s*1\s*hata)\s*[=:]?\s*%?\s*([0-9]+(?:[\.,][0-9]+)?)%?", q_lower)
        alpha_prefix_match = re.search(r"%([0-9]+(?:[\.,][0-9]+)?)\s*(?:alpha|alfa|anlamlılık|tip\s*1\s*hata)", q_lower)
        if alpha_match:
            a_raw = float(alpha_match.group(1).replace(",", "."))
            alpha_val = a_raw / 100.0 if a_raw >= 1.0 else a_raw
        elif alpha_prefix_match:
            a_raw = float(alpha_prefix_match.group(1).replace(",", "."))
            alpha_val = a_raw / 100.0 if a_raw >= 1.0 else a_raw
        elif "%1" in q_lower or "0.01" in q_lower:
            alpha_val = 0.01
        elif "%5" in q_lower or "0.05" in q_lower:
            alpha_val = 0.05
        else:
            alpha_val = 0.05

        # 6. Power
        # Matches "güç=%95", "%95 güç", "güç 0.80", "%99 güç"
        pwr_match = re.search(r"(?:güç|power|test\s*gücü)\s*[=:]?\s*%?\s*([0-9]+(?:[\.,][0-9]+)?)%?", q_lower)
        pwr_prefix_match = re.search(r"%([0-9]+(?:[\.,][0-9]+)?)\s*(?:güç|power|test\s*gücü)", q_lower)
        if pwr_prefix_match:
            p_raw = float(pwr_prefix_match.group(1).replace(",", "."))
            pwr_val = p_raw / 100.0 if p_raw >= 1.0 else p_raw
        elif pwr_match:
            p_raw = float(pwr_match.group(1).replace(",", "."))
            pwr_val = p_raw / 100.0 if p_raw >= 1.0 else p_raw
        elif "%80" in q_lower or "0.80" in q_lower:
            pwr_val = 0.80
        elif "%90" in q_lower or "0.90" in q_lower:
            pwr_val = 0.90
        elif "%95" in q_lower or "0.95" in q_lower:
            pwr_val = 0.95
        elif "%99" in q_lower or "0.99" in q_lower:
            pwr_val = 0.99
        else:
            pwr_val = 0.80

        # 7. Allocation Ratio
        ratio_match = re.search(r"(?:oran|ratio|n2/n1|tahsis)\s*[=:]?\s*([0-9]+(?:[\.,][0-9]+)?)", q_lower)
        if ratio_match:
            ratio_val = float(ratio_match.group(1).replace(",", "."))
        elif "2 kat" in q_lower or "1:2" in q_lower:
            ratio_val = 2.0
        elif "eşit" in q_lower or "bire bir" in q_lower or "1:1" in q_lower:
            ratio_val = 1.0
        else:
            ratio_val = 1.0

        # Build tool parameters
        if mode == "a-priori":
            return {
                "test": test,
                "mode": mode,
                "tails": tails,
                "d": d_val,
                "alpha": alpha_val,
                "power": pwr_val,
                "ratio": ratio_val
            }
        elif mode == "post-hoc":
            n1_match = re.search(r"(?:grup\s*1|n1|ilaç\s*grubu)\s*[=:]?\s*(?:hasta\s*sayısı\s*)?([0-9]+)", q_lower)
            n2_match = re.search(r"(?:grup\s*2|n2|plasebo\s*grubu)\s*[=:]?\s*(?:hasta\s*sayısı\s*)?([0-9]+)", q_lower)
            n_raw_matches = re.findall(r"([0-9]+)\s*hasta", q_lower)
            if n1_match and n2_match:
                n1_val = int(n1_match.group(1))
                n2_val = int(n2_match.group(1))
            elif len(n_raw_matches) >= 2:
                n1_val = int(n_raw_matches[0])
                n2_val = int(n_raw_matches[1])
            else:
                n1_val = 50
                n2_val = 50
            return {
                "test": test,
                "mode": mode,
                "tails": tails,
                "d": d_val,
                "alpha": alpha_val,
                "n1": n1_val,
                "n2": n2_val
            }
        else:
            return {
                "test": test,
                "mode": mode,
                "tails": tails,
                "d": d_val,
                "alpha": alpha_val,
                "power": pwr_val,
                "ratio": ratio_val
            }

    def answer(self, question: str) -> str:
        tokens_in = max(10, len(question) // 4)

        # 1. Parameter extraction
        tool_input = self.parse_clinical_query(question)

        # 2. Call MCP tool (Engine computation)
        raw_output = power_analysis(**tool_input)
        tool_output = json.loads(raw_output)

        tokens_out = max(20, len(raw_output) // 4 + 40)

        # 3. Log query according to CONTRACT.md Section 8
        log_entry = {
            "ts": datetime.datetime.now().astimezone().isoformat(),
            "question": question,
            "tool_input": tool_input,
            "tool_output": tool_output,
            "tokens_in": tokens_in,
            "tokens_out": tokens_out
        }
        try:
            with open(self.log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
        except Exception:
            pass

        # 4. Generate clinician-friendly Turkish explanation
        if "error" in tool_output:
            return f"Sayın Araştırmacı, parametrelerinizde bir uyumsuzluk tespit edildi: {tool_output['error']}"

        if tool_input["mode"] == "a-priori":
            tails_str = "Tek yönlü (üstünlük)" if tool_input['tails'] == 1 else "Çift yönlü (iki taraflı fark)"
            return (
                f"Klinik Çalışma Tasarım Analizi:\n"
                f"- Hipotez Yönü: {tails_str}\n"
                f"- Beklenen Etki Büyüklüğü (d): {tool_input['d']}\n"
                f"- Anlamlılık Düzeyi (α): {tool_input['alpha']}\n"
                f"- Hedef Güç (1-β): %{tool_input['power']*100:.0f}\n\n"
                f"Gereken Örneklem Büyüklüğü:\n"
                f"• Grup 1 (İlaç): {tool_output['n1']} hasta\n"
                f"• Grup 2 (Plasebo): {tool_output['n2']} hasta\n"
                f"• Toplam: {tool_output['n_total']} hasta\n"
                f"• Gerçekleşen Güç: %{tool_output['actual_power']*100:.2f} (Kritik t: {tool_output['critical_t']:.4f}, df: {tool_output['df']})"
            )
        elif tool_input["mode"] == "post-hoc":
            return (
                f"Post-hoc Güç Analizi:\n"
                f"- İncelenen Grup Büyüklükleri: n1={tool_input['n1']}, n2={tool_input['n2']}\n"
                f"- Etki Büyüklüğü: d={tool_input['d']}, α={tool_input['alpha']}\n"
                f"• Elde Edilen İstatistiksel Güç: %{tool_output['power']*100:.2f} (Kritik t: {tool_output['critical_t']:.4f})"
            )
        else:
            return f"Analiz Sonucu: {json.dumps(tool_output, ensure_ascii=False)}"
