import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
from PIL import Image, ImageTk
import json
import datetime

# Função para salvar os dados
def salvar_dados():
    dados = {"estoque": estoque, "carrinho": carrinho, "vendas": vendas}
    with open("dados_petshop.json", "w") as f:
        json.dump(dados, f)

# Função para carregar os dados
def carregar_dados():
    global estoque, carrinho, vendas
    try:
        with open("dados_petshop.json", "r") as f:
            dados = json.load(f)
            estoque = dados["estoque"]
            carrinho = dados["carrinho"]
            vendas = dados["vendas"]
    except FileNotFoundError:
        estoque = {}
        carrinho = []
        vendas = []

# Função para carregar a imagem
def carregar_imagem():
    imagem = Image.open("C:/Users/assis/OneDrive/petshop/sao_francisco.jpg.jpg")
    imagem = imagem.resize((1000, 600))
    imagem_tk = ImageTk.PhotoImage(imagem)

    label_imagem = tk.Label(frame_body, image=imagem_tk)
    label_imagem.image = imagem_tk
    label_imagem.place(relwidth=1, relheight=1)

# Função para cadastrar produtos
def abrir_cadastrar_produtos():
    def salvar_produto():
        nome = entry_nome.get()
        preco = entry_preco.get()
        quantidade = entry_quantidade.get()
        unidade = unidade_var.get()

        if nome and preco and quantidade and unidade:
            try:
                preco = float(preco)
                quantidade = int(quantidade)
                estoque[nome] = {"nome": nome, "preco": preco, "quantidade": quantidade, "unidade": unidade}
                messagebox.showinfo("Sucesso", f"Produto '{nome}' cadastrado com sucesso!")
                salvar_dados()
                janela_cadastrar.destroy()
                atualizar_estoque()
            except ValueError:
                messagebox.showerror("Erro", "Preço ou quantidade inválidos.")
        else:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")

    janela_cadastrar = tk.Toplevel(root)
    janela_cadastrar.title("Cadastrar Produto")
    janela_cadastrar.geometry("300x350")

    tk.Label(janela_cadastrar, text="Nome do Produto:").pack(pady=5)
    entry_nome = tk.Entry(janela_cadastrar)
    entry_nome.pack(pady=5)

    tk.Label(janela_cadastrar, text="Preço:").pack(pady=5)
    entry_preco = tk.Entry(janela_cadastrar)
    entry_preco.pack(pady=5)

    tk.Label(janela_cadastrar, text="Quantidade:").pack(pady=5)
    entry_quantidade = tk.Entry(janela_cadastrar)
    entry_quantidade.pack(pady=5)

    tk.Label(janela_cadastrar, text="Unidade (ml ou kg):").pack(pady=5)
    unidade_var = tk.StringVar(value="ml")
    unidade_menu = ttk.Combobox(janela_cadastrar, textvariable=unidade_var, values=["ml", "kg"], state="readonly")
    unidade_menu.pack(pady=5)

    tk.Button(janela_cadastrar, text="Salvar", command=salvar_produto, height=2).pack(pady=10)

# Função para editar produto
def editar_produto(nome_produto):
    produto = estoque[nome_produto]
    
    def salvar_edicao():
        novo_nome = entry_nome.get()
        novo_preco = entry_preco.get()
        nova_quantidade = entry_quantidade.get()
        nova_unidade = unidade_var.get()

        if novo_nome and novo_preco and nova_quantidade and nova_unidade:
            try:
                novo_preco = float(novo_preco)
                nova_quantidade = int(nova_quantidade)
                # Remover o produto antigo e adicionar o editado
                del estoque[nome_produto]
                estoque[novo_nome] = {
                    "nome": novo_nome,
                    "preco": novo_preco,
                    "quantidade": nova_quantidade,
                    "unidade": nova_unidade
                }
                messagebox.showinfo("Sucesso", f"Produto '{novo_nome}' editado com sucesso!")
                salvar_dados()
                janela_editar.destroy()
                atualizar_estoque()
            except ValueError:
                messagebox.showerror("Erro", "Preço ou quantidade inválidos.")
        else:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")

    janela_editar = tk.Toplevel(root)
    janela_editar.title("Editar Produto")
    janela_editar.geometry("300x350")

    tk.Label(janela_editar, text="Nome do Produto:").pack(pady=5)
    entry_nome = tk.Entry(janela_editar)
    entry_nome.insert(0, produto["nome"])
    entry_nome.pack(pady=5)

    tk.Label(janela_editar, text="Preço:").pack(pady=5)
    entry_preco = tk.Entry(janela_editar)
    entry_preco.insert(0, produto["preco"])
    entry_preco.pack(pady=5)

    tk.Label(janela_editar, text="Quantidade:").pack(pady=5)
    entry_quantidade = tk.Entry(janela_editar)
    entry_quantidade.insert(0, produto["quantidade"])
    entry_quantidade.pack(pady=5)

    tk.Label(janela_editar, text="Unidade (ml ou kg):").pack(pady=5)
    unidade_var = tk.StringVar(value=produto["unidade"])
    unidade_menu = ttk.Combobox(janela_editar, textvariable=unidade_var, values=["ml", "kg"], state="readonly")
    unidade_menu.pack(pady=5)

    tk.Button(janela_editar, text="Salvar", command=salvar_edicao, height=2).pack(pady=10)

# Função para atualizar a lista de estoque
def atualizar_estoque():
    for item in tree.get_children():
        tree.delete(item)
    for produto, info in estoque.items():
        if "nome" in info:  # Verifica se a chave "nome" existe
            tree.insert("", tk.END, values=(info["nome"], f"R${info['preco']:.2f}", info["quantidade"], info["unidade"]))
        else:
            print(f"Produto sem nome encontrado: {produto}")  # Adiciona uma mensagem de erro se o nome não for encontrado

# Função para visualizar o estoque
def abrir_lista_estoque():
    janela_estoque = tk.Toplevel(root)
    janela_estoque.title("Estoque")
    janela_estoque.geometry("400x300")

    if not estoque:
        tk.Label(janela_estoque, text="Estoque vazio.", font=("Arial", 14)).pack(pady=20)
    else:
        global tree
        tree = ttk.Treeview(janela_estoque, columns=("Nome", "Preço", "Quantidade", "Unidade"), show="headings")
        tree.heading("Nome", text="Nome")
        tree.heading("Preço", text="Preço")
        tree.heading("Quantidade", text="Quantidade")
        tree.heading("Unidade", text="Unidade")
        tree.pack(fill=tk.BOTH, expand=True)

        for produto, info in estoque.items():
            item_id = tree.insert("", tk.END, values=(info["nome"], f"R${info['preco']:.2f}", info["quantidade"], info["unidade"]))
            tree.bind("<Double-1>", lambda event, item_id=item_id: editar_produto(estoque[tree.item(item_id)['values'][0]]["nome"]))

# Função para pesquisar produtos
def abrir_pesquisar_produto():
    def realizar_pesquisa():
        nome = entry_pesquisa.get()
        if nome in estoque:
            produto = estoque[nome]
            resultado = f"Nome: {produto['nome']}\nPreço: R${produto['preco']:.2f}\nQuantidade: {produto['quantidade']}\nUnidade: {produto['unidade']}"
            messagebox.showinfo("Resultado da Pesquisa", resultado)

            def adicionar_ao_carrinho():
                quantidade = simpledialog.askinteger("Quantidade", f"Quantos de '{nome}' deseja adicionar ao carrinho?", minvalue=1, maxvalue=produto["quantidade"])
                if quantidade:
                    carrinho.append({
                        "nome": nome,
                        "preco": produto["preco"],
                        "quantidade": quantidade,
                        "unidade": produto["unidade"]
                    })
                    # Atualizar o estoque ao adicionar o produto ao carrinho
                    estoque[nome]["quantidade"] -= quantidade
                    messagebox.showinfo("Sucesso", f"{quantidade} de '{nome}' adicionado ao carrinho.")
                    salvar_dados()

            tk.Button(janela_pesquisar, text="Adicionar ao Carrinho", command=adicionar_ao_carrinho).pack(pady=10)
        else:
            messagebox.showerror("Erro", "Produto não encontrado no estoque.")

    janela_pesquisar = tk.Toplevel(root)
    janela_pesquisar.title("Pesquisar Produto")
    janela_pesquisar.geometry("300x200")

    tk.Label(janela_pesquisar, text="Digite o nome do produto:").pack(pady=5)
    entry_pesquisa = tk.Entry(janela_pesquisar)
    entry_pesquisa.pack(pady=5)
    tk.Button(janela_pesquisar, text="Pesquisar", command=realizar_pesquisa).pack(pady=10)

# Função para visualizar o carrinho
def abrir_lista_carrinho():
    def finalizar_compra():
        if not carrinho:
            messagebox.showinfo("Carrinho Vazio", "Não há itens no carrinho para finalizar a compra.")
        else:
            total = sum(item["preco"] * item["quantidade"] for item in carrinho)
            vendas.append({"data": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "itens": carrinho.copy(), "total": total})
            carrinho.clear()
            salvar_dados()
            messagebox.showinfo("Compra Finalizada", f"Compra finalizada com sucesso! Total: R${total:.2f}")

    janela_carrinho = tk.Toplevel(root)
    janela_carrinho.title("Carrinho")
    janela_carrinho.geometry("400x300")

    if not carrinho:
        tk.Label(janela_carrinho, text="Carrinho vazio.", font=("Arial", 14)).pack(pady=20)
    else:
        tree = ttk.Treeview(janela_carrinho, columns=("Nome", "Preço", "Quantidade", "Unidade"), show="headings")
        tree.heading("Nome", text="Nome")
        tree.heading("Preço", text="Preço")
        tree.heading("Quantidade", text="Quantidade")
        tree.heading("Unidade", text="Unidade")
        tree.pack(fill=tk.BOTH, expand=True)

        for item in carrinho:
            tree.insert("", tk.END, values=(item["nome"], f"R${item['preco']:.2f}", item["quantidade"], item["unidade"]))

        tk.Button(janela_carrinho, text="Finalizar Compra", command=finalizar_compra).pack(pady=10)

# Carregar os dados ao iniciar o aplicativo
carregar_dados()

# Tela principal
root = tk.Tk()
root.title("Petshop Luz do Campo")
root.geometry("1000x600")
root.configure(bg="#f5f5f5")

# Cabeçalho
header = tk.Frame(root, bg="#388E3C", height=100)
header.pack(fill=tk.X)

tk.Label(
    header,
    text="Petshop Luz do Campo",
    font=("Arial", 28, "bold"),
    bg="#388E3C",
    fg="white"
).pack(pady=20)

# Barra lateral
barra_lateral = tk.Frame(root, bg="#388E3C", width=250)
barra_lateral.pack(side=tk.LEFT, fill=tk.Y)

# Funções dos botões
def criar_botao(nome, comando):
    btn = tk.Button(barra_lateral, text=nome, command=comando)
    btn.config(
        width=20,
        height=2,
        font=("Arial", 12, "bold"),
        bg="#388E3C",
        fg="white",
        relief="flat",
        activebackground="#28a745",
        activeforeground="white"
    )
    return btn

btn_produto = criar_botao("Cadastrar Produto", abrir_cadastrar_produtos)
btn_produto.pack(pady=10)

btn_estoque = criar_botao("Estoque", abrir_lista_estoque)
btn_estoque.pack(pady=10)

btn_pesquisar = criar_botao("Pesquisar Produto", abrir_pesquisar_produto)
btn_pesquisar.pack(pady=10)

btn_carrinho = criar_botao("Carrinho", abrir_lista_carrinho)
btn_carrinho.pack(pady=10)

# Corpo principal
frame_body = tk.Frame(root, bg="#ffffff", padx=20, pady=20)
frame_body.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

carregar_imagem()

root.mainloop()