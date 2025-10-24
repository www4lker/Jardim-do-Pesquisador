#!/usr/bin/env python3
"""
Corrige títulos problemáticos nas notas candidatas, extraindo contexto dos arquivos.
Gera CSV final com títulos revisados e relatório de alterações.
"""

import csv
import re
from pathlib import Path
from typing import Optional

VAULT_BASE = Path('/mnt/d/jardim-notas/VAULTS-REFERENCIA/vault-consolidado-genealogia')
INPUT_CSV = Path('/mnt/d/jardim-notas/VAULTS-REFERENCIA/Jardim-do-Pesquisador/scripts/candidatas_limpas.csv')
OUTPUT_CSV = Path('/mnt/d/jardim-notas/VAULTS-REFERENCIA/Jardim-do-Pesquisador/scripts/candidatas_finais.csv')
RELATORIO_PATH = Path('/mnt/d/jardim-notas/VAULTS-REFERENCIA/Jardim-do-Pesquisador/scripts/relatorio_titulos.md')


def titulo_problematico(titulo: str) -> bool:
    """Heurística para identificar títulos que precisam de correção."""
    if not titulo:
        return True
    clean = titulo.strip()
    if clean == '':
        return True
    if len(clean) <= 3:
        return True
    if '...' in clean:
        return True
    if re.fullmatch(r'[\d\.\- ]+', clean):
        return True
    return False


def extrair_heading(primeiro_texto: str) -> Optional[str]:
    """Extrai o primeiro heading útil do conteúdo."""
    match = re.search(r'^\s*#\s+(.+)$', primeiro_texto, flags=re.MULTILINE)
    if match:
        return match.group(1).strip()

    # fallback: primeira linha não vazia que não é metadado
    for linha in primeiro_texto.splitlines():
        linha = linha.strip()
        if not linha:
            continue
        if linha.lower().startswith('criado em'):
            continue
        if linha.startswith('#'):
            continue
        return linha
    return None


def construir_contexto(rel_path: Path) -> str:
    """Constrói contexto usando os dois últimos diretórios antes do arquivo."""
    directories = list(rel_path.parts[:-1])
    if not directories:
        return ''
    contexto = directories[-2:] if len(directories) >= 2 else directories
    return " / ".join(contexto)


def corrigir_titulo(row: dict) -> tuple[str, bool, str]:
    """Retorna título corrigido, flag se alterado e motivo."""
    titulo_original = row['titulo']
    caminho_relativo = Path(row['caminho'])
    arquivo = VAULT_BASE / caminho_relativo

    if not titulo_problematico(titulo_original):
        return titulo_original, False, ''

    if not arquivo.exists():
        return titulo_original, False, 'arquivo_inexistente'

    try:
        conteudo = arquivo.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        conteudo = arquivo.read_text(encoding='latin-1')
    except Exception:
        return titulo_original, False, 'erro_leitura'

    heading = extrair_heading(conteudo)
    if heading:
        heading = heading.replace('"', "'").strip()
    contexto = construir_contexto(caminho_relativo)

    if heading:
        titulo_corrigido = heading
    else:
        # fallback para nome do arquivo sem extensão
        titulo_corrigido = caminho_relativo.stem.replace('-', ' ').title()

    if contexto:
        if contexto.lower() not in titulo_corrigido.lower():
            titulo_corrigido = f"{contexto} – {titulo_corrigido}"

    # Normalizar espaços
    titulo_corrigido = re.sub(r'\s+', ' ', titulo_corrigido).strip()

    if titulo_corrigido != titulo_original:
        return titulo_corrigido, True, 'titulo_substituido'
    return titulo_original, False, ''


def processar_titulos():
    if not INPUT_CSV.exists():
        raise FileNotFoundError(f"Arquivo de entrada não encontrado: {INPUT_CSV}")

    correcoes = []
    linhas_atualizadas = []

    with INPUT_CSV.open('r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []

        for row in reader:
            novo_titulo, alterado, motivo = corrigir_titulo(row)
            if alterado:
                correcoes.append({
                    'caminho': row['caminho'],
                    'titulo_original': row['titulo'],
                    'titulo_corrigido': novo_titulo,
                    'motivo': motivo,
                })
            row['titulo'] = novo_titulo
            linhas_atualizadas.append(row)

    # Escrever CSV final
    with OUTPUT_CSV.open('w', newline='', encoding='utf-8') as f_out:
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(linhas_atualizadas)

    # Gerar relatório
    with RELATORIO_PATH.open('w', encoding='utf-8') as f_rel:
        f_rel.write("# RELATÓRIO DE CORREÇÃO DE TÍTULOS\n\n")
        f_rel.write(f"Notas processadas: {len(linhas_atualizadas)}\n")
        f_rel.write(f"Títulos corrigidos: {len(correcoes)}\n\n")

        if correcoes:
            f_rel.write("## LISTA DE TÍTULOS CORRIGIDOS\n\n")
            for correcao in correcoes:
                f_rel.write(f"- {correcao['caminho']}\n")
                f_rel.write(f"  Título original: {correcao['titulo_original']}\n")
                f_rel.write(f"  Título corrigido: {correcao['titulo_corrigido']}\n\n")

    return len(linhas_atualizadas), len(correcoes)


if __name__ == '__main__':
    print("Corrigindo títulos...")
    total_notas, total_corrigidos = processar_titulos()
    print(f"\n✓ CSV final gerado: {OUTPUT_CSV}")
    print(f"✓ Títulos corrigidos: {total_corrigidos}")
    print(f"✓ Relatório detalhado: {RELATORIO_PATH}")
