import os
import json
import datetime
import hashlib
import csv

ARQUIVO_LOGIN = "login.txt"
ARQUIVO_INVENTARIO = "inventario.csv"
CARDAPIO_FILE = "cardapio.json"
PEDIDOS_FILE = "pedidos.json"


# CIFRA DE CÉSAR (CRIPTOGRAFIA DO INVENTÁRIO)
def cifrar(texto: str, shift: int = 3) -> str: # Cifra texto com Cifra de césar e somente letras são deslocadas
    resultado = ""
    for char in texto:
        if 'A' <= char <= 'Z' or 'a' <= char <= 'z':
            base = ord('A') if char.isupper() else ord('a')
            novo_char = chr((ord(char) - base + shift) % 26 + base)
            resultado += novo_char
        else:
            resultado += char
    return resultado

def decifrar(texto: str, shift: int = 3) -> str: # Decifra o texto
    return cifrar(texto, -shift)


# SISTEMA DE LOGIN - Gabriel - (HASH SHA-256)
def hash_sha256(texto: str) -> str: # Retorna o texto em hash-256
    return hashlib.sha256(texto.encode()).hexdigest()


def arquivo_login_valido() -> bool: # Verificação da existência do arquivo login.txt e se contém os hashes para usuário e senha com 64 caracteres
    if not os.path.exists(ARQUIVO_LOGIN):
        return False
    try:
        with open(ARQUIVO_LOGIN, "r", encoding="utf-8") as f:
            conteudo = f.read().strip()
        if not conteudo:
            return False
        partes = conteudo.split(";")
        if len(partes) != 2:
            return False
        return all(len(p) == 64 for p in partes)
    except Exception:
        return False


def registrar_usuario_inicial(): #  Primeira execução: cria usuário e senha iniciais, salvando apenas os hashes.
    print("\n=== REGISTRO INICIAL DO SISTEMA ===")
    usuario = input("Defina um nome de usuário: ").strip()
    senha = input("Defina uma senha: ").strip()

    with open(ARQUIVO_LOGIN, "w", encoding="utf-8") as f:
        f.write(f"{hash_sha256(usuario)};{hash_sha256(senha)}")

    print("\n✔ Registro concluído! Reinicie o programa para fazer login.\n")

def carregar_credenciais(): # Retorna os valores lidos
    with open(ARQUIVO_LOGIN, "r", encoding="utf-8") as f:
        usuario_hash, senha_hash = f.read().strip().split(";")
    return usuario_hash, senha_hash

def login() -> bool: # login com até 3 tentativas
    usuario_hash, senha_hash = carregar_credenciais()

    for tentativa in range(3):
        print("\n=== LOGIN ===")
        usuario_input = input("Usuário: ").strip()
        senha_input = input("Senha: ").strip()

        if (hash_sha256(usuario_input) == usuario_hash and
                hash_sha256(senha_input) == senha_hash):
            print("\n✔ Login bem-sucedido!")
            return True
        else:
            print("\n✘ Usuário ou senha incorretos!")
            restantes = 2 - tentativa
            if restantes >= 0:
                print(f"Tentativas restantes: {restantes}")
    print("\n❌ Número máximo de tentativas excedido. Encerrando.")
    return False


def editar_usuario_senha(): # Alterar usuário e senha cadastrados
    print("\n=== ALTERAR USUÁRIO E SENHA ===")
    usuario = input("Novo usuário: ").strip()
    senha = input("Nova senha: ").strip()

    with open(ARQUIVO_LOGIN, "w", encoding="utf-8") as f:
        f.write(f"{hash_sha256(usuario)};{hash_sha256(senha)}") # Escreve as alterações em hash

    print("\n✔ Credenciais atualizadas com sucesso!\n")

# ============================================================
# INVENTÁRIO (PRODUTOS DO RESTAURANTE)
# ============================================================

# Estrutura:
# inventario = {
#   id (int): {
#       "nome": str,
#       "quantidade": int,
#       "preco": float,
#       "importado": bool
#   },
#   ...
# }

inventario = {}


def adicionar_produto(identif: int, nome: str, quantidade: int,
                      preco: float, importado: bool) -> bool:
    """Adiciona um novo produto ao inventário."""
    if identif in inventario:
        print("❌ Já existe um produto com esse ID.")
        return False

    inventario[identif] = {
        "nome": nome,
        "quantidade": quantidade,
        "preco": preco,
        "importado": importado
    }
    print(f"✔ Produto '{nome}' adicionado com sucesso.")
    return True


def remover_produto(identif: int) -> bool:
    """Remove um produto do inventário pelo ID."""
    if identif in inventario:
        del inventario[identif]
        print("✔ Produto removido com sucesso.")
        return True
    print("❌ ID não encontrado no inventário.")
    return False


def atualizar_produto(identif: int,
                      nome: str = None,
                      quantidade: int = None,
                      preco: float = None,
                      importado: bool = None) -> bool:
    """Atualiza campos de um produto pelo ID."""
    if identif not in inventario:
        print("❌ Produto não encontrado.")
        return False

    dados = inventario[identif]

    if nome is not None:
        dados["nome"] = nome
    if quantidade is not None:
        dados["quantidade"] = quantidade
    if preco is not None:
        dados["preco"] = preco
    if importado is not None:
        dados["importado"] = importado

    print("✔ Produto atualizado com sucesso.")
    return True


def listar_itens_ordenados():
    """Lista o inventário ordenado por nome do produto (usando sort customizado)."""
    lista_ordenada = ordenar_inventario_por_nome()
    if not lista_ordenada:
        print("\nInventário vazio.\n")
        return

    print("\n===== INVENTÁRIO ATUAL (ORDENADO POR NOME) =====\n")
    for item in lista_ordenada:
        print(
            f"ID: {item['id']} | "
            f"Nome: {item['nome']} | "
            f"Qtd: {item['quantidade']} | "
            f"Preço: R$ {item['preco']:.2f} | "
            f"Importado: {item['importado']}"
        )
    print()


def verificar_existencia_nome(nome: str) -> bool:
    """Retorna True se algum produto tiver esse nome (case-insensitive)."""
    nome = nome.lower()
    for dados in inventario.values():
        if dados["nome"].lower() == nome:
            return True
    return False


def encontrar_id_por_nome(nome: str):
    """Retorna o ID do primeiro produto com esse nome, ou None se não encontrar."""
    nome = nome.lower()
    for identif, dados in inventario.items():
        if dados["nome"].lower() == nome:
            return identif
    return None


def estatisticas_inventario():
    """Exibe quantidade de produtos e valor total do estoque."""
    total_produtos = len(inventario)
    valor_total = 0.0
    for dados in inventario.values():
        valor_total += dados["quantidade"] * dados["preco"]

    print("\n===== ESTATÍSTICAS DO INVENTÁRIO =====")
    print(f"Total de produtos cadastrados: {total_produtos}")
    print(f"Valor total estimado do estoque: R$ {valor_total:.2f}")
    print("======================================\n")


def carregar_inventario(caminho: str = ARQUIVO_INVENTARIO):
    """Carrega o inventário cifrado do arquivo CSV para o dicionário em memória."""
    global inventario

    if not os.path.exists(caminho):
        print("Arquivo de inventário não encontrado. Criando vazio...")
        inventario = {}
        return

    inventario.clear()

    with open(caminho, "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            linha = linha.strip()
            if not linha:
                continue

            partes = linha.split(";")
            if len(partes) != 5:
                continue  # linha inválida

            id_dec = int(decifrar(partes[0]))
            nome_dec = decifrar(partes[1])
            qtd_dec = int(decifrar(partes[2]))
            preco_dec = float(decifrar(partes[3]))
            importado_dec = True if decifrar(partes[4]) == "True" else False

            inventario[id_dec] = {
                "nome": nome_dec,
                "quantidade": qtd_dec,
                "preco": preco_dec,
                "importado": importado_dec
            }

    print("✔ Inventário carregado com sucesso.")


def salvar_inventario(caminho: str = ARQUIVO_INVENTARIO):
    """Salva o inventário cifrado em CSV (processamento em lote)."""
    with open(caminho, "w", encoding="utf-8") as arquivo:
        for identif, dados in inventario.items():
            linha = ";".join([
                cifrar(str(identif)),
                cifrar(dados["nome"]),
                cifrar(str(dados["quantidade"])),
                cifrar(str(dados["preco"])),
                cifrar(str(dados["importado"]))
            ])
            arquivo.write(linha + "\n")

    print("✔ Inventário salvo em disco.")


# ============================================================
# ORDENAÇÃO E BUSCA (INVENTÁRIO)
# ============================================================

def inventario_para_lista():
    """Converte o dicionário de inventário para lista de dicts com campo 'id'."""
    return [
        {"id": identif,
         "nome": dados["nome"],
         "quantidade": dados["quantidade"],
         "preco": dados["preco"],
         "importado": dados["importado"]}
        for identif, dados in inventario.items()
    ]


def insertion_sort(lista):
    """Ordena lista de produtos (dicts) por nome usando Insertion Sort."""
    lista_ord = lista[:]
    for i in range(1, len(lista_ord)):
        chave = lista_ord[i]
        j = i - 1
        while j >= 0 and lista_ord[j]["nome"].lower() > chave["nome"].lower():
            lista_ord[j + 1] = lista_ord[j]
            j -= 1
        lista_ord[j + 1] = chave
    return lista_ord


def merge(esq, dir_):
    """Função auxiliar do Merge Sort."""
    resultado = []
    i = j = 0
    while i < len(esq) and j < len(dir_):
        if esq[i]["nome"].lower() <= dir_[j]["nome"].lower():
            resultado.append(esq[i])
            i += 1
        else:
            resultado.append(dir_[j])
            j += 1
    resultado.extend(esq[i:])
    resultado.extend(dir_[j:])
    return resultado


def merge_sort(lista):
    """Ordena lista de produtos (dicts) por nome usando Merge Sort."""
    if len(lista) <= 1:
        return lista[:]
    meio = len(lista) // 2
    esq = merge_sort(lista[:meio])
    dir_ = merge_sort(lista[meio:])
    return merge(esq, dir_)


def ordenar_inventario_por_nome():
    """
    Usa Insertion Sort se houver até 100 produtos,
    senão, Merge Sort.
    """
    lista = inventario_para_lista()
    if len(lista) <= 100:
        return insertion_sort(lista)
    else:
        return merge_sort(lista)


def busca_linear_por_nome(nome: str):
    """Busca linear por nome no inventário."""
    nome = nome.lower()
    resultados = []
    for identif, dados in inventario.items():
        if dados["nome"].lower() == nome:
            resultados.append({"id": identif, **dados})
    return resultados


def busca_binaria_por_nome(nome: str):
    """
    Busca binária por nome em uma lista previamente ordenada.
    Retorna lista com 0 ou 1 elemento (nesse exemplo).
    """
    lista_ord = ordenar_inventario_por_nome()
    nome = nome.lower()
    inicio, fim = 0, len(lista_ord) - 1

    while inicio <= fim:
        meio = (inicio + fim) // 2
        atual = lista_ord[meio]["nome"].lower()

        if atual == nome:
            return [lista_ord[meio]]
        elif atual < nome:
            inicio = meio + 1
        else:
            fim = meio - 1
    return []


# ============================================================
# CARDÁPIO E PEDIDOS (RESTAURANTE)
# ============================================================

def carregar_cardapio():
    """Carrega o cardápio do arquivo JSON."""
    if not os.path.exists(CARDAPIO_FILE):
        return {}
    with open(CARDAPIO_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar_cardapio(cardapio):
    """Salva o cardápio em JSON."""
    with open(CARDAPIO_FILE, "w", encoding="utf-8") as f:
        json.dump(cardapio, f, ensure_ascii=False, indent=2)


def listar_cardapio(cardapio):
    """Exibe o cardápio."""
    if not cardapio:
        print("\nO cardápio ainda está vazio.\n")
        return

    print("\n=========== CARDÁPIO ===========")
    for id_prato, dados in cardapio.items():
        print(f"ID {id_prato} - {dados['nome']} - R$ {dados['preco']:.2f}")
        print("   Ingredientes:", ", ".join(dados["ingredientes"]))
    print("================================\n")


def adicionar_prato(cardapio, codigo, nome, preco, ingredientes):
    """Adiciona um novo prato ao cardápio."""
    cardapio[str(codigo)] = {
        "nome": nome,
        "preco": preco,
        "ingredientes": ingredientes
    }


def remover_prato(cardapio, codigo):
    """Remove um prato do cardápio, se existir."""
    codigo = str(codigo)
    if codigo in cardapio:
        del cardapio[codigo]
        return True
    return False


def atualizar_prato(cardapio, codigo, nome=None, preco=None, ingredientes=None):
    """Atualiza dados de um prato do cardápio."""
    codigo = str(codigo)
    if codigo not in cardapio:
        return False

    if nome is not None:
        cardapio[codigo]["nome"] = nome
    if preco is not None:
        cardapio[codigo]["preco"] = preco
    if ingredientes is not None:
        cardapio[codigo]["ingredientes"] = ingredientes

    return True


def carregar_pedidos():
    """Carrega pedidos do JSON."""
    if not os.path.exists(PEDIDOS_FILE):
        return []
    with open(PEDIDOS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar_pedidos(pedidos):
    """Salva pedidos em JSON."""
    with open(PEDIDOS_FILE, "w", encoding="utf-8") as f:
        json.dump(pedidos, f, ensure_ascii=False, indent=2, default=str)


def criar_pedido(cardapio, pedidos, id_prato, quantidade):
    """
    Cria um pedido. Agora integrado com o INVENTÁRIO:
    - Para cada ingrediente do prato, procuramos um produto do inventário
      com o MESMO NOME (campo 'nome').
    - Verificamos se há quantidade suficiente.
    - Se houver, descontamos do inventário.
    """
    id_prato = str(id_prato)

    if id_prato not in cardapio:
        print("❌ Prato não encontrado no cardápio.")
        return None

    prato = cardapio[id_prato]

    # Verifica ingrediente por ingrediente se o estoque é suficiente.
    for ing in prato["ingredientes"]:
        ing = ing.strip()
        id_prod = encontrar_id_por_nome(ing)
        if id_prod is None:
            print(f"❌ Ingrediente '{ing}' não encontrado no inventário.")
            return None
        if inventario[id_prod]["quantidade"] < quantidade:
            print(f"❌ Estoque insuficiente para o ingrediente: {ing}")
            return None

    # Desconta estoque
    for ing in prato["ingredientes"]:
        ing = ing.strip()
        id_prod = encontrar_id_por_nome(ing)
        inventario[id_prod]["quantidade"] -= quantidade

    total = prato["preco"] * quantidade

    pedido = {
        "id": len(pedidos) + 1,
        "prato": prato["nome"],
        "quantidade": quantidade,
        "total": total,
        "horario": datetime.datetime.now().isoformat()
    }

    pedidos.append(pedido)
    return pedido


def listar_pedidos(pedidos):
    """Lista pedidos realizados."""
    if not pedidos:
        print("\nNenhum pedido foi registrado ainda.\n")
        return

    print("\n======= PEDIDOS REALIZADOS =======")
    for p in pedidos:
        print(f"Pedido {p['id']} - {p['prato']} x{p['quantidade']} = R$ {p['total']:.2f}")
        print(f"  Horário: {p['horario']}")
    print("==================================\n")


def faturamento_total(pedidos):
    """Retorna a soma total dos pedidos."""
    return sum(p["total"] for p in pedidos)

def exportar_cardapio_para_csv(cardapio, caminho_csv="cardapio.csv"):
    """
    Exporta o cardápio (JSON/dict) para um arquivo CSV.
    Cada prato vira uma linha no CSV.
    Ingredientes são unidos em uma única string separada por vírgula.
    """
    with open(caminho_csv, "w", newline="", encoding="utf-8") as arquivo:
        writer = csv.writer(arquivo, delimiter=";")
        
        # Cabeçalho
        writer.writerow(["codigo", "nome", "preco", "ingredientes"])
        
        # Linhas
        for codigo, dados in cardapio.items():
            ingredientes_str = ", ".join(dados["ingredientes"])
            writer.writerow([
                codigo,
                dados["nome"],
                dados["preco"],
                ingredientes_str
            ])

    print(f"✔ Cardápio exportado para {caminho_csv}")
    
def exportar_pedidos_para_csv(pedidos, caminho_csv="pedidos.csv"):
    """
    Exporta a lista de pedidos (JSON/lista de dicts) para um arquivo CSV.
    Campos: id, prato, quantidade, total, horario
    """
    with open(caminho_csv, "w", newline="", encoding="utf-8") as arquivo:
        writer = csv.writer(arquivo, delimiter=";")
        
        # Cabeçalho
        writer.writerow(["id", "prato", "quantidade", "total", "horario"])
        
        # Linhas
        for p in pedidos:
            writer.writerow([
                p["id"],
                p["prato"],
                p["quantidade"],
                f"{p['total']:.2f}",
                p["horario"]
            ])

    print(f"✔ Pedidos exportados para {caminho_csv}")

# ============================================================
# FUNÇÕES DE INTERFACE (MENUS)
# ============================================================

def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


def menu_cardapio(cardapio):
    while True:
        limpar_tela()
        print("===== MENU DO CARDÁPIO =====")
        print("1 - Listar Cardápio")
        print("2 - Adicionar Prato")
        print("3 - Remover Prato")
        print("4 - Atualizar Prato")
        print("0 - Voltar")
        op = input("Escolha: ").strip()

        if op == "1":
            listar_cardapio(cardapio)
            input("Enter para continuar...")

        elif op == "2":
            try:
                cod = input("Código do prato: ").strip()
                nome = input("Nome: ").strip()
                preco = float(input("Preço: R$ ").replace(",", "."))
                ingredientes = input("Ingredientes separados por vírgula: ").split(",")
                ingredientes = [i.strip() for i in ingredientes if i.strip()]

                adicionar_prato(cardapio, cod, nome, preco, ingredientes)
                print("✔ Prato adicionado!")
            except Exception as e:
                print(f"Erro ao adicionar prato: {e}")

            input("Enter...")

        elif op == "3":
            cod = input("Código do prato: ").strip()
            if remover_prato(cardapio, cod):
                print("✔ Prato removido!")
            else:
                print("❌ Código inválido.")
            input("Enter...")

        elif op == "4":
            cod = input("Código do prato: ").strip()

            print("\nDeixe em branco para não alterar.\n")
            nome = input("Novo nome: ").strip()
            preco = input("Novo preço: ").strip()
            ing = input("Novos ingredientes (vírgula): ").strip()

            nome = nome if nome != "" else None
            preco = float(preco.replace(",", ".")) if preco != "" else None
            ing = [i.strip() for i in ing.split(",")] if ing != "" else None

            if atualizar_prato(cardapio, cod, nome, preco, ing):
                print("✔ Prato atualizado!")
            else:
                print("❌ Prato não encontrado.")

            input("Enter...")

        elif op == "0":
            break

        else:
            print("Opção inválida.")
            input("Enter...")


def menu_inventario():
    while True:
        limpar_tela()
        print("===== MENU DO INVENTÁRIO =====")
        print("1 - Listar Estoque (ordenado por nome)")
        print("2 - Adicionar Produto")
        print("3 - Remover Produto")
        print("4 - Atualizar Produto")
        print("5 - Verificar Existência por Nome")
        print("6 - Buscar Produto por Nome (Linear)")
        print("7 - Buscar Produto por Nome (Binária)")
        print("8 - Buscar Produto por ID")
        print("9 - Estatísticas do Inventário")
        print("0 - Voltar")
        op = input("Escolha: ").strip()

        if op == "1":
            listar_itens_ordenados()
            input("Enter...")

        elif op == "2":
            try:
                ident = int(input("ID do produto (inteiro): "))
                nome = input("Nome: ").strip()
                qtd = int(input("Quantidade: "))
                preco = float(input("Preço unitário (R$): ").replace(",", "."))
                imp = input("Importado? (s/n): ").strip().lower() == "s"
                adicionar_produto(ident, nome, qtd, preco, imp)
            except ValueError:
                print("❌ Valores inválidos.")
            input("Enter...")

        elif op == "3":
            try:
                ident = int(input("ID do produto a remover: "))
                remover_produto(ident)
            except ValueError:
                print("❌ ID inválido.")
            input("Enter...")

        elif op == "4":
            try:
                ident = int(input("ID do produto: "))
                nome = input("Novo nome (ENTER p/ manter): ").strip()
                qtd = input("Nova quantidade (ENTER p/ manter): ").strip()
                preco = input("Novo preço (ENTER p/ manter): ").strip()
                imp = input("É importado? (s/n ou ENTER p/ manter): ").strip().lower()

                nome = nome if nome != "" else None
                qtd = int(qtd) if qtd != "" else None
                preco = float(preco.replace(",", ".")) if preco != "" else None
                if imp == "s":
                    imp_bool = True
                elif imp == "n":
                    imp_bool = False
                else:
                    imp_bool = None

                atualizar_produto(ident, nome, qtd, preco, imp_bool)
            except ValueError:
                print("❌ Valor inválido.")
            input("Enter...")

        elif op == "5":
            nome = input("Nome para verificar: ").strip()
            existe = verificar_existencia_nome(nome)
            print("\nExiste no inventário?", "Sim" if existe else "Não")
            input("Enter...")

        elif op == "6":
            nome = input("Nome para buscar (Linear): ").strip()
            res = busca_linear_por_nome(nome)
            if not res:
                print("❌ Nenhum produto encontrado.")
            else:
                print("\nResultado(s):")
                for item in res:
                    print(
                        f"ID: {item['id']} | Nome: {item['nome']} | "
                        f"Qtd: {item['quantidade']} | Preço: R$ {item['preco']:.2f}"
                    )
            input("Enter...")

        elif op == "7":
            nome = input("Nome para buscar (Binária): ").strip()
            res = busca_binaria_por_nome(nome)
            if not res:
                print("❌ Nenhum produto encontrado.")
            else:
                item = res[0]
                print(
                    f"\nID: {item['id']} | Nome: {item['nome']} | "
                    f"Qtd: {item['quantidade']} | Preço: R$ {item['preco']:.2f}"
                )
            input("Enter...")

        elif op == "8":
            try:
                ident = int(input("ID para buscar: "))
                if ident in inventario:
                    dados = inventario[ident]
                    print(
                        f"\nID: {ident} | Nome: {dados['nome']} | "
                        f"Qtd: {dados['quantidade']} | Preço: R$ {dados['preco']:.2f}"
                    )
                else:
                    print("❌ ID não encontrado.")
            except ValueError:
                print("❌ ID inválido.")
            input("Enter...")

        elif op == "9":
            estatisticas_inventario()
            input("Enter...")

        elif op == "0":
            break

        else:
            print("Opção inválida.")
            input("Enter...")


def menu_pedidos(cardapio, pedidos):
    while True:
        limpar_tela()
        print("===== MENU DE PEDIDOS =====")
        print("1 - Criar Pedido")
        print("2 - Listar Pedidos")
        print("3 - Ver Faturamento Total")
        print("0 - Voltar")
        op = input("Escolha: ").strip()

        if op == "1":
            idp = input("ID do prato: ").strip()
            try:
                qtd = int(input("Quantidade: "))
            except ValueError:
                print("❌ Quantidade inválida.")
                input("Enter...")
                continue

            pedido = criar_pedido(cardapio, pedidos, idp, qtd)
            if pedido:
                print("\n✔ Pedido criado com sucesso!")
                print(f"Total: R$ {pedido['total']:.2f}")
            input("Enter...")

        elif op == "2":
            listar_pedidos(pedidos)
            input("Enter para continuar...")

        elif op == "3":
            total = faturamento_total(pedidos)
            print(f"\nFaturamento total: R$ {total:.2f}")
            input("Enter...")

        elif op == "0":
            break
        else:
            print("Opção inválida.")
            input("Enter...")


def menu_estatisticas_gerais(cardapio, pedidos):
    limpar_tela()
    print("===== ESTATÍSTICAS GERAIS =====")
    print(f"Total de pratos no cardápio: {len(cardapio)}")
    print(f"Total de pedidos: {len(pedidos)}")
    print(f"Faturamento acumulado: R$ {faturamento_total(pedidos):.2f}")
    estatisticas_inventario()
    input("Enter para voltar...")


def menu_principal(cardapio, pedidos):
    while True:
        limpar_tela()
        print("===== SISTEMA DO RESTAURANTE =====")
        print("1 - Cardápio")
        print("2 - Inventário")
        print("3 - Pedidos")
        print("4 - Estatísticas Gerais")
        print("5 - Alterar Usuário/Senha")
        print("0 - Sair")
        op = input("Escolha: ").strip()

        if op == "1":
            menu_cardapio(cardapio)
        elif op == "2":
            menu_inventario()
        elif op == "3":
            menu_pedidos(cardapio, pedidos)
        elif op == "4":
            menu_estatisticas_gerais(cardapio, pedidos)
        elif op == "5":
            editar_usuario_senha()
            input("Enter...")
        elif op == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida.")
            input("Enter...")


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

def main():
    # 1) Se não há login configurado, registrar usuário inicial
    if not arquivo_login_valido():
        registrar_usuario_inicial()
        return

    # 2) Login
    if not login():
        return

    # 3) Carregar dados (processamento em lote)
    carregar_inventario()
    cardapio = carregar_cardapio()
    pedidos = carregar_pedidos()

    # 4) Menu principal
    menu_principal(cardapio, pedidos)

    # 5) Ao sair do menu, salvar tudo (lote)
    salvar_inventario()
    salvar_cardapio(cardapio)
    salvar_pedidos(pedidos)
    
    # 6) Salvar em csv
    exportar_cardapio_para_csv(cardapio)
    exportar_pedidos_para_csv(pedidos)
    
    print("✔ Dados salvos. Até logo!")

main()
