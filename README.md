# 📦 Sistema de Gestão de Inventário para Restaurante com Segurança da Informação

![Status](https://img.shields.io/badge/Status-Concluído-green)

Projeto acadêmico de um sistema de gestão de inventário em Python, desenvolvido para a disciplina de Linguagem de Programação Python. O foco do projeto é a manipulação de estruturas de dados, algoritmos de busca e ordenação, e a implementação de conceitos básicos de segurança da Informação.

**Orientador:** Prof. Lucio Nunes de Lira

---

## 🚀 Funcionalidades Principais

O sistema é totalmente baseado em interface de terminal (CLI) e não utiliza banco de dados externo. Todas as operações são feitas em memória (usando dicionários) e salvas em arquivos locais ao encerrar o programa (processamento em lote).

### Gestão de Inventário
- **Adicionar, Atualizar e Remover:** Gerenciamento completo dos produtos no inventário.
- **Listagem de Produtos:** Exibe todos os produtos cadastrados, ordenados por nome.
- **Busca de Produtos:** Permite a busca por ID ou por nome.
- **Estatísticas do Estoque:** Mostra a quantidade total de produtos e o valor total do inventário.

### Segurança da Informação
- **Autenticação de Usuário:** O sistema exige login (usuário e senha) para acesso.
- **Armazenamento Seguro de Senhas:** Usuário e senha são armazenados no arquivo `login.txt` usando **Hashing SHA-256**, garantindo que não fiquem em texto claro.
- **Criptografia de Dados:** Os dados do inventário são **cifrados (Cifra de César)** antes de serem salvos no arquivo `inventario.csv`. Os dados são decifrados ao serem carregados na memória.
- **Validação de Entradas:** Garante que IDs sejam únicos e que preço e quantidade sejam numéricos.

---

## 🛠️ Conceitos e Tecnologias Aplicadas

Este projeto foi construído inteiramente em **Python 3**, com foco nos seguintes conceitos:

- **Estrutura de Dados:** Uso principal de **Dicionários** para representar o inventário em memória e **Listas** para operações auxiliares.
- **Manipulação de Arquivos:** Leitura e escrita em arquivos de texto (`login.txt`) e `.csv` (`inventario.csv`).
- **Algoritmos de Busca:**
     * **Busca Linear:** Utilizada para pesquisar produtos por nome diretamente no dicionário.
     * **Busca Binária:** Utilizada para pesquisar rapidamente por nome em uma lista ordenada.
- **Algoritmos de Ordenação:** O sistema seleciona o algoritmo automaticamente com base no volume de dados:
    * **Bubble/Selection/Insertion Sort:** Para até 100 produtos.
    * **Merge Sort:** Para mais de 100 produtos.
- **Segurança:**
     * **Hashing:** Módulo `hashlib` (SHA-256) para senhas.
     * **Criptografia:** Implementação de uma Cifra de César customizada para os dados do inventário.

---

## 🚦 Como Executar

1. Clone este repositório:
```bash
git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
```
2. Navegue até o diretório do projeto:
```bash
cd seu-repositorio
```
3. Execute o script principal:
```bash
python main.py
```

> **Nota sobre a Primeira Execução:**
> Na primeira vez que o sistema for executado, o arquivo `login.txt` estará vazio. O programa solicitará que você crie um **usuário e senha iniciais** para ter acesso ao sistema.

---

## 👥 Equipe

* ABYNER HENRIQUE SIMOES
* CARLOS EDUARDO OLIVEIRA DOARTE
* GABRIEL BRAGA COSTA
* MATHEUS FELICIANO DAS NEVES
* PEDRO HENRIQUE BENEDICTO FARIA

---

## 📄 Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo `LICENSE` para mais detalhes.
