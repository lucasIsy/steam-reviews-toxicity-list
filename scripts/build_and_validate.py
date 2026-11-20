#!/usr/bin/env python3
"""Valida lists/tos/*.csv e gera (ou verifica) o arquivo consolidado lists/lista_tos.csv."""

from __future__ import annotations

import argparse
import csv
import io
import sys
from pathlib import Path

EXPECTED_FIELDS = ["termo", "classificacao", "linguagem", "motivo", "categoria"]
ROOT = Path(__file__).resolve().parent.parent
TOS_DIR = ROOT / "lists" / "tos"
CONSOLIDATED_PATH = ROOT / "lists" / "lista_tos.csv"


def load_and_validate() -> list[dict[str, str]]:
    if not TOS_DIR.is_dir():
        raise SystemExit(f"Erro: diretório não encontrado: {TOS_DIR}")

    csv_files = sorted(TOS_DIR.glob("*.csv"))
    if not csv_files:
        raise SystemExit(f"Erro: nenhum CSV encontrado em {TOS_DIR}")

    errors: list[str] = []
    all_rows: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()

    for path in csv_files:
        expected_lang = path.stem.lower()
        with path.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            if reader.fieldnames != EXPECTED_FIELDS:
                errors.append(
                    f"{path.name}: cabeçalho inválido {reader.fieldnames!r} "
                    f"(esperado {EXPECTED_FIELDS!r})"
                )
                continue

            for idx, row in enumerate(reader, start=2):
                termo = (row.get("termo") or "").strip()
                cls = (row.get("classificacao") or "").strip()
                lang = (row.get("linguagem") or "").strip()
                motivo = (row.get("motivo") or "").strip()
                cat = (row.get("categoria") or "").strip()

                if not termo:
                    errors.append(f"{path.name}:{idx}: 'termo' vazio")
                if termo != termo.lower():
                    errors.append(f"{path.name}:{idx}: 'termo' deve estar em minúsculas ({termo!r})")
                if cls != "remover":
                    errors.append(f"{path.name}:{idx}: 'classificacao' deve ser 'remover' (recebido {cls!r})")
                if lang != expected_lang:
                    errors.append(
                        f"{path.name}:{idx}: 'linguagem' ({lang!r}) difere do arquivo ({expected_lang!r})"
                    )
                if motivo != "TOS Violation":
                    errors.append(f"{path.name}:{idx}: 'motivo' deve ser 'TOS Violation' (recebido {motivo!r})")
                if not cat:
                    errors.append(f"{path.name}:{idx}: 'categoria' vazia")

                key = (termo.lower(), lang.lower())
                if key in seen:
                    errors.append(f"{path.name}:{idx}: termo duplicado {key}")
                seen.add(key)

                all_rows.append(
                    {
                        "termo": termo,
                        "classificacao": cls,
                        "linguagem": lang,
                        "motivo": motivo,
                        "categoria": cat,
                    }
                )

    if errors:
        print("Falha na validação:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        raise SystemExit(1)

    return all_rows


def render_csv(rows: list[dict[str, str]]) -> str:
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=EXPECTED_FIELDS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return buf.getvalue()


def main() -> None:
    parser = argparse.ArgumentParser(description="Valida listas TOS e gera lista_tos.csv.")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Apenas valida e verifica se lists/lista_tos.csv está sincronizado (sem sobrescrever).",
    )
    args = parser.parse_args()

    rows = load_and_validate()
    rendered = render_csv(rows)

    if args.check:
        if not CONSOLIDATED_PATH.exists():
            print(f"Erro: {CONSOLIDATED_PATH} não existe. Rode sem --check.", file=sys.stderr)
            raise SystemExit(1)
        current = CONSOLIDATED_PATH.read_text(encoding="utf-8").replace("\r\n", "\n")
        if current != rendered:
            print(
                f"Erro: {CONSOLIDATED_PATH.name} está desatualizado. "
                "Execute 'python scripts/build_and_validate.py' para sincronizar.",
                file=sys.stderr,
            )
            raise SystemExit(1)
        print(f"OK: {len(rows)} termos validados e {CONSOLIDATED_PATH.name} sincronizado.")
        return

    CONSOLIDATED_PATH.write_text(rendered, encoding="utf-8")
    print(f"OK: {len(rows)} termos validados e gravados em {CONSOLIDATED_PATH}.")


if __name__ == "__main__":
    main()
