# Relatório de Progresso - Castro Mobile Estoque e Vendas

**Data:** 23/11/2025
**Versão:** 1.0 (Em Desenvolvimento)

## 1. Visão Geral do Projeto
O projeto consiste em um sistema de gestão de estoque e vendas (PDV) desenvolvido em **Python** utilizando a biblioteca **Flet** para a interface gráfica e **SQLite** para o banco de dados. O sistema possui um design moderno e futurista ("Neon/Cyberpunk") e foca na agilidade e facilidade de uso.

## 2. Estrutura e Tecnologia
- **Linguagem**: Python 3.x
- **Interface (GUI)**: Flet (Flutter based)
- **Banco de Dados**: SQLite (`estoque_vendas.db`)
- **Arquitetura**: Modular (`main.py`, `views.py`, `database.py`, `ui_components.py`)

## 3. Funcionalidades Implementadas

### 3.1. Dashboard Financeiro
Painel inicial com indicadores chave de desempenho:
- **Faturamento Total**: Soma de todas as vendas pagas.
- **Lucro Líquido**: Estimativa baseada no preço de venda - preço de compra.
- **Total a Receber (Fiado)**: Valor total de vendas pendentes.
- **Total Investido**: Valor total do estoque atual (preço de compra x quantidade).
- **Itens Vendidos**: Quantidade total de produtos vendidos.

### 3.2. Gestão de Produtos
Módulo completo para administração do inventário.
- **CRUD Completo**: Adicionar, Editar, Excluir e Visualizar produtos.
- **Campos do Produto**:
  - Nome, Categoria, Preço de Venda, Preço de Compra, Quantidade.
  - **Novos Campos**: Foto (URL), Código de Barras, Fornecedor, Descrição, Status (Ativo/Inativo).
- **Filtros Avançados**:
  - Por Categoria.
  - Por Faixa de Preço (Mín/Máx).
  - Por Baixo Estoque (<= 5 un) e Esgotado.
  - Por Mais Vendidos.
  - Por Produtos Inativos.
- **Ordenação Inteligente**:
  - A-Z (Alfabética).
  - Preço (Menor -> Maior).
  - Estoque (Maior -> Menor).
  - Recentes (Data de cadastro).
- **Visual Rápido (Quick View)**:
  - Popup interativo ao clicar no produto.
  - Exibe foto, detalhes completos e botões de ação rápida.
  - Histórico de Movimentações (Vendas do produto).

### 3.3. Gestão de Clientes
- Cadastro de clientes com Nome, Telefone, CPF e Email.
- Histórico de Compras individual por cliente.
- Integração com o sistema de vendas e dívidas.

### 3.4. Caixa e Vendas (PDV)
- **Carrinho de Compras**: Adição dinâmica de produtos.
- **Busca Rápida**: Pesquisa de produtos por nome em tempo real.
- **Seleção de Cliente**: Vínculo da venda a um cliente cadastrado.
- **Venda Fiado**: Opção para marcar a venda como "Pendente", gerando débito para o cliente.
- **Finalização**: Baixa automática no estoque e registro financeiro.

### 3.5. Controle de Devedores
- Lista automática de clientes com pagamentos pendentes.
- Exibição do total devido por cliente.
- Botão para **Quitar Dívida**, que atualiza o status das vendas para "PAGO" e o financeiro.

## 4. Interface e UX
- **Tema**: Dark Mode com acentos em Neon (Azul, Roxo, Verde, Vermelho).
- **Responsividade**: Layouts adaptáveis com barras de rolagem e containers expansíveis.
- **Identidade Visual**: Ícone personalizado e título "Castro Mobile Estoque e Vendas".

## 5. Próximos Passos Sugeridos
- Implementação de autenticação de usuários (Login).
- Geração de relatórios em PDF/Excel.
- Backup automático do banco de dados.
