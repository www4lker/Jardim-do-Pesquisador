#!/usr/bin/env python3
"""
Converte notas selecionadas para formato Jekyll.
Adiciona frontmatter YAML, preserva conteúdo e wikilinks.
"""

import os
import re
import csv
import shutil
from pathlib import Path
from datetime import datetime


def normalizar_nome_arquivo(titulo):
    """Converte título em nome de arquivo válido"""
    # Remove caracteres especiais, mantém letras, números, espaços e hífens
    nome = re.sub(r'[^\w\s-]', '', titulo.lower())
    nome = re.sub(r'[-\s]+', '-', nome)
    return nome.strip('-') + '.md'


def extrair_metadados(conteudo):
    """Extrai data de criação se existir no formato informal"""
    match = re.search(r'criado em:\s*(\d{2}:\d{2}\s+\d{4}-\d{2}-\d{2})', conteudo, re.IGNORECASE)
    if match:
        try:
            data_str = match.group(1)
            # Converte "01:51 2022-08-10" para datetime
            data = datetime.strptime(data_str, '%H:%M %Y-%m-%d')
            return data.strftime('%Y-%m-%d')
        except Exception:
            pass
    return datetime.now().strftime('%Y-%m-%d')


def adicionar_frontmatter(conteudo, titulo, data):
    """Adiciona frontmatter YAML ao início da nota"""
    # Remove possível H1 duplicado do título
    conteudo_sem_h1 = re.sub(r'^#\s+' + re.escape(titulo) + r'\s*\n', '', conteudo, count=1, flags=re.MULTILINE)

    frontmatter = f"""---
title: "{titulo}"
date: {data}
---

"""
    return frontmatter + conteudo_sem_h1.lstrip()


def converter_nota(caminho_origem, titulo, destino_dir, log_file):
    """Converte uma nota individual"""
    try:
        origem = Path(caminho_origem)
        conteudo = origem.read_text(encoding='utf-8')

        data = extrair_metadados(conteudo)
        conteudo_convertido = adicionar_frontmatter(conteudo, titulo, data)

        nome_arquivo = normalizar_nome_arquivo(titulo)
        caminho_destino = Path(destino_dir) / nome_arquivo

        # Evita sobrescrever se já existir
        if caminho_destino.exists():
            base_stem = caminho_destino.stem
            data_suffix = datetime.now().strftime('%Y%m%d')
            contador = 1
            while True:
                if contador == 1:
                    candidato = Path(destino_dir) / f"{base_stem}-{data_suffix}.md"
                else:
                    candidato = Path(destino_dir) / f"{base_stem}-{data_suffix}-{contador}.md"
                if not candidato.exists():
                    caminho_destino = candidato
                    nome_arquivo = candidato.name
                    break
                contador += 1

        caminho_destino.write_text(conteudo_convertido, encoding='utf-8')

        log_file.write(f"✓ {titulo} → {nome_arquivo}\n")
        return True

    except Exception as e:
        log_file.write(f"✗ {titulo}: {str(e)}\n")
        return False


def converter_lote(csv_selecionadas, vault_base, destino_dir, max_notas=100):
    """Converte lote de notas selecionadas"""
    destino_dir = Path(destino_dir)
    destino_dir.mkdir(parents=True, exist_ok=True)

    log_path = destino_dir.parent / 'scripts' / 'log_conversao.txt'

    with open(csv_selecionadas, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        selecionadas = list(reader)[:max_notas]

    print(f"Convertendo {len(selecionadas)} notas...")

    sucessos = 0
    with open(log_path, 'w', encoding='utf-8') as log:
        log.write(f"Conversão iniciada: {datetime.now()}\n\n")

        for i, nota in enumerate(selecionadas, 1):
            caminho_completo = Path(vault_base) / nota['caminho']

            if converter_nota(caminho_completo, nota['titulo'], destino_dir, log):
                sucessos += 1

            if i % 10 == 0:
                print(f"Progresso: {i}/{len(selecionadas)}")

        log.write(f"\n\nTotal: {sucessos}/{len(selecionadas)} convertidas com sucesso\n")

    print(f"\n✓ Conversão concluída: {sucessos}/{len(selecionadas)}")
    print(f"✓ Log salvo em: {log_path}")
    print(f"✓ Notas em: {destino_dir}")


if __name__ == '__main__':
    CSV_SELECIONADAS = '/mnt/d/jardim-notas/VAULTS-REFERENCIA/Jardim-do-Pesquisador/scripts/candidatas_finais.csv'
    VAULT_BASE = '/mnt/d/jardim-notas/VAULTS-REFERENCIA/vault-consolidado-genealogia'
    DESTINO_DIR = '/mnt/d/jardim-notas/VAULTS-REFERENCIA/Jardim-do-Pesquisador/_notes/Public'

    converter_lote(CSV_SELECIONADAS, VAULT_BASE, DESTINO_DIR, max_notas=100)
