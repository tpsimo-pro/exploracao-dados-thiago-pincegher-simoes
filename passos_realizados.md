# Passo a Passo das Atividades Realizadas

Este documento descreve as etapas executadas para o tratamento e análise do dataset de Planos de Ação Nacional (PAN).

## 1. Limpeza e Tratamento de Dados
Foi realizada uma limpeza técnica no arquivo CSV original para garantir a qualidade dos dados.

*   **O que foi feito:** Remoção de caracteres de controle não renderizados (ASCII < 32) e conversão da codificação original (`latin-1`) para `UTF-8 com BOM`.
*   **Motivo:** A presença de caracteres invisíveis e o uso de uma codificação legada poderiam causar erros na execução de scripts Python e corromper a exibição de acentos (como em "Ação" ou "Espécies") em ferramentas como o Microsoft Excel e bibliotecas de Data Science.

## 2. Desenvolvimento das Atividades
Após a estabilização da base de dados, seguimos com a realização dos tópicos impostos no Google Classroom.
