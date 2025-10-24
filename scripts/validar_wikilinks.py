#!/usr/bin/env python3
"""
Valida integridade dos wikilinks após migração.
Identifica links quebrados e gera relatório.
"""

import re
from pathlib import Path
from collections import defaultdict


def extrair_wikilinks(conteudo):
    """Extrai todos os wikilinks de uma nota"""
    return re.findall(r'\[\[([^\]|]+)(?:\|[^\]]*)?\]\]', conteudo)


def normalizar_titulo_para_busca(titulo):
    """Normaliza título para comparação"""
    return titulo.lower().strip()


def construir_indice_notas(notas_dir):
    """Cria índice de notas disponíveis por título"""
    indice = {}

    for arquivo in Path(notas_dir).glob('*.md'):
        try:
            conteudo = arquivo.read_text(encoding='utf-8')

            # Busca título no frontmatter
            match = re.search(r'^title:\s*["\']?([^"\']+)["\']?$', conteudo, re.MULTILINE)
            if match:
                titulo = match.group(1).strip()
                titulo_normalizado = normalizar_titulo_para_busca(titulo)
                indice[titulo_normalizado] = arquivo.name
        except Exception as e:
            print(f"Erro lendo {arquivo.name}: {e}")

    return indice


def validar_links(notas_dir):
    """Valida todos os wikilinks nas notas"""
    indice_notas = construir_indice_notas(notas_dir)

    links_quebrados = defaultdict(list)
    estatisticas = {
        'total_notas': 0,
        'total_links': 0,
        'links_validos': 0,
        'links_quebrados': 0,
    }

    for arquivo in Path(notas_dir).glob('*.md'):
        estatisticas['total_notas'] += 1

        try:
            conteudo = arquivo.read_text(encoding='utf-8')
            wikilinks = extrair_wikilinks(conteudo)

            for link in wikilinks:
                estatisticas['total_links'] += 1
                link_normalizado = normalizar_titulo_para_busca(link)

                if link_normalizado not in indice_notas:
                    estatisticas['links_quebrados'] += 1
                    links_quebrados[arquivo.name].append(link)
                else:
                    estatisticas['links_validos'] += 1

        except Exception as e:
            print(f"Erro processando {arquivo.name}: {e}")

    return links_quebrados, estatisticas


def gerar_relatorio(links_quebrados, estatisticas, output_path):
    """Gera relatório de validação"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# RELATÓRIO DE VALIDAÇÃO DE WIKILINKS\n\n")
        f.write(f"Data: {Path(output_path).stat().st_mtime}\n\n")

        f.write("## ESTATÍSTICAS\n\n")
        f.write(f"- Total de notas: {estatisticas['total_notas']}\n")
        f.write(f"- Total de wikilinks: {estatisticas['total_links']}\n")
        f.write(f"- Links válidos: {estatisticas['links_validos']}\n")
        f.write(f"- Links quebrados: {estatisticas['links_quebrados']}\n")

        if estatisticas['total_links'] > 0:
            taxa_sucesso = (estatisticas['links_validos'] / estatisticas['total_links']) * 100
            f.write(f"- Taxa de integridade: {taxa_sucesso:.1f}%\n\n")

        if links_quebrados:
            f.write("## LINKS QUEBRADOS POR NOTA\n\n")
            for nota, links in sorted(links_quebrados.items()):
                f.write(f"### {nota}\n")
                for link in links:
                    f.write(f"- `[[{link}]]`\n")
                f.write("\n")
        else:
            f.write("✓ Todos os wikilinks estão íntegros!\n")


if __name__ == '__main__':
    NOTAS_DIR = '/mnt/d/jardim-notas/VAULTS-REFERENCIA/Jardim-do-Pesquisador/_notes/Public'
    OUTPUT_PATH = '/mnt/d/jardim-notas/VAULTS-REFERENCIA/Jardim-do-Pesquisador/scripts/relatorio_wikilinks.md'

    print("Validando wikilinks...")
    links_quebrados, stats = validar_links(NOTAS_DIR)
    gerar_relatorio(links_quebrados, stats, OUTPUT_PATH)

    print(f"\n✓ Relatório gerado: {OUTPUT_PATH}")
    print(f"✓ Integridade: {stats['links_validos']}/{stats['total_links']} links válidos")
