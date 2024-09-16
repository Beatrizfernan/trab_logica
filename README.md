# Provador de Teoremas com Tableaux Analíticos

Este projeto implementa um provador de teoremas utilizando o método dos tableaux analíticos para fórmulas proposicionais. Desenvolvido em Python, o programa usa a biblioteca Lark para o parsing das fórmulas lógicas.

## Funcionalidades

- Identificação do conectivo principal e subfórmulas imediatas.
- Processamento de fórmulas do tipo α (ex.: `A ∧ B`).
- Processamento de fórmulas do tipo β (ex.: `A ∨ B`, `A → B`).
- Verificação de fechamento de ramos com base em literais contraditórios.
- Determinação da validade ou invalidade de um sequente.

## Instruções de Execução

1. **Clonar o Repositório**
    
    ```bash
    
    git clone <URL_DO_REPOSITÓRIO>
    
    ```
    
2. **Acessar o Diretório do Projeto**
    
    ```bash
   
    cd <DIRETÓRIO_DO_PROJETO>
    
    ```
    
3. **Preparar o Ambiente**
Verifique a versão do Python:
    
    ```bash

    python --version
    
    ```
    
4. **Executar o Programa**
Passe o arquivo de entrada como stdin:
    
    ```bash
   
    python meuprograma.py < exemplo.tab
    
    ```
    

## Integrantes

- **Beatriz Fernandes Souza** - 514933
