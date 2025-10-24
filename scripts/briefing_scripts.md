## TAREFA 2: PRÉ-PROCESSAMENTO DO CSV

### Passo 2.1: Instalar dependências Python (se necessário)
```bash
# Não há dependências externas, apenas biblioteca padrão
python3 --version  # confirmar Python 3.12.3
```

### Passo 2.2: Criar scripts de limpeza

Criar dois scripts na pasta `Jardim-do-Pesquisador/scripts/`:

1. **limpar_duplicatas.py** - Remove duplicatas exatas e notas `-merged`
2. **corrigir_titulos.py** - Corrige títulos problemáticos extraindo contexto

os nomes dos scripst são: `limpeza.py` e `corrige-titulos.py` e estao localizados na pasta scripts/

### Passo 2.3: Executar pipeline de limpeza
```bash
cd /mnt/d/jardim-notas/VAULTS-REFERENCIA/Jardim-do-Pesquisador/scripts

# Etapa 1: Limpar duplicatas e merged
python3 limpar_duplicatas.py

# Verificar resultado
echo "Notas após limpeza:"
wc -l candidatas_limpas.csv

# Etapa 2: Corrigir títulos
python3 corrigir_titulos.py

# Verificar resultado final
echo "Notas finais para conversão:"
wc -l candidatas_finais.csv

# Revisar relatórios
cat relatorio_limpeza.md
cat relatorio_titulos.md
```

**CHECKPOINT OBRIGATÓRIO**: 
Após execução, o agente DEVE reportar:
- Quantas notas merged foram removidas
- Quantas duplicatas foram eliminadas
- Quantos títulos foram corrigidos
- Total final de notas em `candidatas_finais.csv`

Só prosseguir para conversão Jekyll após confirmação humana.
```

---

## FLUXO DE DADOS ATUALIZADO
```
candidatas_selecionadas.csv (101 notas)
           ↓
   [limpar_duplicatas.py]
           ↓
candidatas_limpas.csv (~85-90 notas estimadas)
           ↓
   [corrigir_titulos.py]
           ↓
candidatas_finais.csv (~85-90 notas com títulos corrigidos)
           ↓
   [converter_para_jekyll.py - do briefing original]
           ↓
_notes/Public/*.md (notas prontas para Jekyll)
