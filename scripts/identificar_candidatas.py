#!/usr/bin/env python3
"""
Escaneia vault-consolidado-genealogia procurando notas sobre hibridismo.
Gera CSV com candidatas à migração.
"""

import os
import re
from pathlib import Path
from datetime import datetime
import csv

# Termos de busca para hibridismo (case-insensitive)
TERMOS_HIBRIDO = [
    r'\bhíbrid[oa]s?\b',
    r'\bautoria híbrida\b',
    r'\bcoautoria\b',
    r'\bhuman[oa]?-[iI][aA]\b',
    r'\bhuman[oa]?-máquina\b',
    r'\bhuman[oa]?-tecnologia\b',
]

TERMOS_IA = [
    r'\b[iI]nteligência [aA]rtificial\b',
    r'\b[iI]\.?[aA]\.?\b',
    r'\bLLM\b',
    r'\bGPT\b',
    r'\bClaude\b',
    r'\bChatGPT\b',
    r'\bagent[es]?\b',
    r'\bprompt[s]?\b',
    r'\bmodelo[s]? de linguagem\b',
]

TERMOS_METODOLOGICOS = [
    r'\bmetodologi[a]?\b',
    r'\bquali-quantitativ[oa]\b',
    r'\bmétodo[s]? mist[oa]s?\b',
    r'\btriangula[çc][ãa]o\b',
]

TERMOS_ONTOLOGICOS = [
    r'\bciborg[s]?\b',
    r'\bpós-human[oa]s?\b',
    r'\bantropoceno\b',
    r'\bnatureza[- ]cultura\b',
    r'\bactant[es]?\b',
    r'\bagenciamento\b',
]

TODOS_TERMOS = TERMOS_HIBRIDO + TERMOS_IA + TERMOS_METODOLOGICOS + TERMOS_ONTOLOGICOS


def extrair_titulo(conteudo, nome_arquivo):
    """Extrai título da nota (primeiro H1 ou nome do arquivo)"""
    match = re.search(r'^#\s+(.+)$', conteudo, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return nome_arquivo.replace('.md', '').replace('-', ' ').title()


def contar_wikilinks(conteudo):
    """Conta wikilinks [[]] na nota"""
    return len(re.findall(r'\[\[([^\]]+)\]\]', conteudo))


def buscar_termos(conteudo, termos):
    """Retorna lista de termos encontrados (sem duplicatas)"""
    encontrados = set()
    for termo in termos:
        if re.search(termo, conteudo, re.IGNORECASE):
            encontrados.add(termo)
    return sorted(encontrados)


def escanear_vault(vault_path, output_csv):
    """Escaneia vault e gera CSV com candidatas"""
    candidatas = []

    vault_path = Path(vault_path)
    arquivos_md = list(vault_path.rglob('*.md'))

    print(f"Escaneando {len(arquivos_md)} arquivos...")

    for i, arquivo in enumerate(arquivos_md, 1):
        if i % 100 == 0:
            print(f"Processados: {i}/{len(arquivos_md)}")

        try:
            conteudo = arquivo.read_text(encoding='utf-8')
        except Exception as e:
            print(f"Erro lendo {arquivo}: {e}")
            continue

        termos_encontrados = buscar_termos(conteudo, TODOS_TERMOS)

        if not termos_encontrados:
            continue

        titulo = extrair_titulo(conteudo, arquivo.stem)
        wikilinks = contar_wikilinks(conteudo)
        caminho_relativo = arquivo.relative_to(vault_path)

        candidatas.append({
            'caminho': str(caminho_relativo),
            'titulo': titulo,
            'wikilinks': wikilinks,
            'relevancia': len(termos_encontrados),
            'termos': '; '.join(termos_encontrados),
        })

    # Ordenar por relevância (mais termos) e depois por wikilinks
    candidatas.sort(key=lambda x: (x['relevancia'], x['wikilinks']), reverse=True)

    # Salvar CSV
    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['caminho', 'titulo', 'wikilinks', 'relevancia', 'termos'])
        writer.writeheader()
        writer.writerows(candidatas)

    print(f"\n✓ Encontradas {len(candidatas)} notas candidatas")
    print(f"✓ Resultados salvos em: {output_csv}")
    print(f"\nTop 10 por relevância:")
    for c in candidatas[:10]:
        print(f"  [{c['relevancia']}] {c['titulo']} ({c['wikilinks']} links)")


if __name__ == '__main__':
    VAULT_PATH = '/mnt/d/jardim-notas/VAULTS-REFERENCIA/vault-consolidado-genealogia'
    OUTPUT_CSV = '/mnt/d/jardim-notas/VAULTS-REFERENCIA/Jardim-do-Pesquisador/scripts/candidatas_migracao.csv'

    escanear_vault(VAULT_PATH, OUTPUT_CSV)
