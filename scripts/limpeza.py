#!/usr/bin/env python3
"""
Limpa CSV removendo duplicatas exatas e notas -merged.
Remove duplicatas mantendo primeira ocorrência.
Exclui completamente notas com '-merged' no caminho.
"""

import csv
from pathlib import Path
from collections import OrderedDict

def limpar_csv(input_csv, output_csv):
    """Remove duplicatas e notas merged"""
    
    # Usar OrderedDict para manter ordem enquanto remove duplicatas
    notas_unicas = OrderedDict()
    notas_removidas = {
        'duplicatas': [],
        'merged': []
    }
    
    with open(input_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for linha in reader:
            caminho = linha['caminho']
            titulo = linha['titulo']
            
            # Ignorar notas -merged
            if '-merged.md' in caminho:
                notas_removidas['merged'].append({
                    'caminho': caminho,
                    'titulo': titulo
                })
                continue
            
            # Criar chave única baseada em caminho normalizado
            # Remove variações de diretório que possam causar duplicatas
            chave = caminho.lower().strip()
            
            # Se já existe, é duplicata
            if chave in notas_unicas:
                notas_removidas['duplicatas'].append({
                    'caminho_original': notas_unicas[chave]['caminho'],
                    'caminho_duplicata': caminho,
                    'titulo': titulo
                })
                continue
            
            # Adicionar nota única
            notas_unicas[chave] = linha
    
    # Salvar CSV limpo
    if notas_unicas:
        with open(output_csv, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['caminho', 'titulo', 'wikilinks', 'relevancia', 'termos']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(notas_unicas.values())
    
    # Gerar relatório
    relatorio = []
    relatorio.append("# RELATÓRIO DE LIMPEZA DO CSV\n")
    relatorio.append(f"Total de notas originais: {len(notas_unicas) + len(notas_removidas['duplicatas']) + len(notas_removidas['merged'])}")
    relatorio.append(f"Notas únicas mantidas: {len(notas_unicas)}")
    relatorio.append(f"Notas merged removidas: {len(notas_removidas['merged'])}")
    relatorio.append(f"Duplicatas removidas: {len(notas_removidas['duplicatas'])}\n")
    
    if notas_removidas['merged']:
        relatorio.append("## NOTAS MERGED REMOVIDAS\n")
        for nota in notas_removidas['merged']:
            relatorio.append(f"- {nota['caminho']}")
            relatorio.append(f"  Título: {nota['titulo']}\n")
    
    if notas_removidas['duplicatas']:
        relatorio.append("\n## DUPLICATAS REMOVIDAS\n")
        for dup in notas_removidas['duplicatas']:
            relatorio.append(f"- MANTIDO: {dup['caminho_original']}")
            relatorio.append(f"  REMOVIDO: {dup['caminho_duplicata']}")
            relatorio.append(f"  Título: {dup['titulo']}\n")
    
    return '\n'.join(relatorio), len(notas_unicas)

if __name__ == '__main__':
    INPUT_CSV = '/mnt/d/jardim-notas/VAULTS-REFERENCIA/Jardim-do-Pesquisador/scripts/candidatas_selecionadas.csv'
    OUTPUT_CSV = '/mnt/d/jardim-notas/VAULTS-REFERENCIA/Jardim-do-Pesquisador/scripts/candidatas_limpas.csv'
    RELATORIO_PATH = '/mnt/d/jardim-notas/VAULTS-REFERENCIA/Jardim-do-Pesquisador/scripts/relatorio_limpeza.md'
    
    print("Limpando CSV...")
    relatorio, total_limpas = limpar_csv(INPUT_CSV, OUTPUT_CSV)
    
    # Salvar relatório
    with open(RELATORIO_PATH, 'w', encoding='utf-8') as f:
        f.write(relatorio)
    
    print(f"\n✓ CSV limpo gerado: {OUTPUT_CSV}")
    print(f"✓ Total de notas após limpeza: {total_limpas}")
    print(f"✓ Relatório detalhado: {RELATORIO_PATH}")