import tkinter as tk
from tkinter import messagebox
from conexao import conectar  # Certifique-se de que esse módulo existe

def formatar_preco(valor_str):
    try:
        valor = float(valor_str)
        return round(valor, 2)
    except ValueError:
        return None

def abrir_produtos():
    janela_produtos = tk.Toplevel()
    janela_produtos.title("Gerenciar Produtos")

    def cadastrar():
        nome = entry_nome.get().strip()
        preco = formatar_preco(entry_preco.get())
        if nome and preco is not None:
            try:
                conn = conectar()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO produtos (nome, preco) VALUES (%s, %s)", (nome, preco))
                conn.commit()
                conn.close()
                messagebox.showinfo("Sucesso", "Produto cadastrado!")
                entry_nome.delete(0, tk.END)
                entry_preco.delete(0, tk.END)
                listar()
            except Exception as e:
                messagebox.showerror("Erro", str(e))
        else:
            messagebox.showwarning("Campos inválidos", "Preencha todos os campos corretamente.")

    def listar():
        lista.delete(0, tk.END)
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM produtos")
            for produto in cursor.fetchall():
                lista.insert(tk.END, f"{produto[0]} | {produto[1]} | R$ {produto[2]:.2f}")
            conn.close()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def deletar():
        item = lista.get(tk.ACTIVE)
        if item:
            pid = item.split(" | ")[0]
            try:
                conn = conectar()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM produtos WHERE id = %s", (pid,))
                conn.commit()
                conn.close()
                messagebox.showinfo("Removido", "Produto deletado.")
                listar()
            except Exception as e:
                messagebox.showerror("Erro", str(e))

    def atualizar():
        item = lista.get(tk.ACTIVE)
        if item:
            pid = item.split(" | ")[0]
            novo_nome = entry_nome.get().strip()
            novo_preco = formatar_preco(entry_preco.get())
            if novo_nome and novo_preco is not None:
                try:
                    conn = conectar()
                    cursor = conn.cursor()
                    cursor.execute("UPDATE produtos SET nome=%s, preco=%s WHERE id=%s", (novo_nome, novo_preco, pid))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Atualizado", "Produto alterado.")
                    listar()
                except Exception as e:
                    messagebox.showerror("Erro", str(e))
            else:
                messagebox.showwarning("Campos inválidos", "Informe nome e preço válidos para atualizar.")

    tk.Label(janela_produtos, text="Nome do produto").grid(row=0, column=0)
    entry_nome = tk.Entry(janela_produtos)
    entry_nome.grid(row=0, column=1)

    tk.Label(janela_produtos, text="Preço (ex: 9.90)").grid(row=1, column=0)
    entry_preco = tk.Entry(janela_produtos)
    entry_preco.grid(row=1, column=1)

    tk.Button(janela_produtos, text="Cadastrar", command=cadastrar).grid(row=2, column=0)
    tk.Button(janela_produtos, text="Atualizar", command=atualizar).grid(row=2, column=1)
    tk.Button(janela_produtos, text="Deletar", command=deletar).grid(row=3, column=0, columnspan=2)

    lista = tk.Listbox(janela_produtos, width=50)
    lista.grid(row=4, column=0, columnspan=2)

    listar()

def abrir_estoque():
    janela_estoque = tk.Toplevel()
    janela_estoque.title("Controle de Estoque")

    tk.Label(janela_estoque, text="Produto | Estoque").grid(row=0, column=0, columnspan=2)

    lista_estoque = tk.Listbox(janela_estoque, width=50)
    lista_estoque.grid(row=1, column=0, columnspan=2)

    def listar_estoque():
        lista_estoque.delete(0, tk.END)  # Limpar lista antes de adicionar
        try:
            conn = conectar()  # Conectando ao banco
            cursor = conn.cursor()
            cursor.execute("""
                SELECT p.nome, e.quantidade 
                FROM produtos p 
                LEFT JOIN estoque e ON p.id = e.produto_id
            """)  # Relacionando produtos com estoque
            for produto in cursor.fetchall():
                lista_estoque.insert(tk.END, f"{produto[0]} | {produto[1]} unidades")
            conn.close()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    listar_estoque()

    tk.Label(janela_estoque, text="Produto").grid(row=2, column=0)
    entry_produto_estoque = tk.Entry(janela_estoque)
    entry_produto_estoque.grid(row=2, column=1)

    tk.Label(janela_estoque, text="Estoque").grid(row=3, column=0)
    entry_estoque = tk.Entry(janela_estoque)
    entry_estoque.grid(row=3, column=1)

    def atualizar_estoque():
        produto = entry_produto_estoque.get().strip()
        estoque = entry_estoque.get().strip()
        if produto and estoque.isdigit():
            try:
                conn = conectar()
                cursor = conn.cursor()
                
                # Verifica se o produto já existe no estoque
                cursor.execute("SELECT id FROM produtos WHERE nome = %s", (produto,))
                produto_id = cursor.fetchone()
                
                if produto_id:
                    produto_id = produto_id[0]
                    # Atualiza a quantidade no estoque
                    cursor.execute("""
                        INSERT INTO estoque (produto_id, quantidade)
                        VALUES (%s, %s)
                        ON DUPLICATE KEY UPDATE quantidade = %s
                    """, (produto_id, estoque, estoque))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Atualizado", "Estoque atualizado!")
                    listar_estoque()  # Atualiza a lista
                else:
                    messagebox.showwarning("Produto não encontrado", "Produto não existe no sistema.")
                    
            except Exception as e:
                messagebox.showerror("Erro", str(e))
        else:
            messagebox.showwarning("Entrada inválida", "Informe produto e quantidade válidos.")

    tk.Button(janela_estoque, text="Atualizar Estoque", command=atualizar_estoque).grid(row=4, column=0, columnspan=2)

def abrir_clientes():
    janela_clientes = tk.Toplevel()
    janela_clientes.title("Cadastro de Clientes")

    tk.Label(janela_clientes, text="Nome do Cliente | Telefone").grid(row=0, column=0, columnspan=2)

    lista_clientes = tk.Listbox(janela_clientes, width=50)
    lista_clientes.grid(row=1, column=0, columnspan=2)

    def listar_clientes():
        lista_clientes.delete(0, tk.END)  # Limpar lista antes de adicionar
        try:
            conn = conectar()  # Conectando ao banco
            cursor = conn.cursor()
            cursor.execute("SELECT nome, telefone FROM clientes")  # Ajuste conforme sua tabela
            for cliente in cursor.fetchall():
                lista_clientes.insert(tk.END, f"{cliente[0]} | {cliente[1]}")
            conn.close()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    listar_clientes()

    tk.Label(janela_clientes, text="Nome do Cliente").grid(row=2, column=0)
    entry_nome_cliente = tk.Entry(janela_clientes)
    entry_nome_cliente.grid(row=2, column=1)

    tk.Label(janela_clientes, text="Telefone").grid(row=3, column=0)
    entry_telefone_cliente = tk.Entry(janela_clientes)
    entry_telefone_cliente.grid(row=3, column=1)

    def cadastrar_cliente():
        nome_cliente = entry_nome_cliente.get().strip()
        telefone_cliente = entry_telefone_cliente.get().strip()
        if nome_cliente and telefone_cliente:
            try:
                conn = conectar()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO clientes (nome, telefone) VALUES (%s, %s)", (nome_cliente, telefone_cliente))
                conn.commit()
                conn.close()
                messagebox.showinfo("Sucesso", "Cliente cadastrado!")
                listar_clientes()  # Atualiza a lista
            except Exception as e:
                messagebox.showerror("Erro", str(e))
        else:
            messagebox.showwarning("Campos inválidos", "Preencha todos os campos.")

    tk.Button(janela_clientes, text="Cadastrar Cliente", command=cadastrar_cliente).grid(row=4, column=0, columnspan=2)

# Janela principal
janela = tk.Tk()
janela.title("Sistema de Padaria - Menu Principal")

tk.Label(janela, text="Bem-vindo ao Sistema de Padaria", font=("Arial", 14)).pack(pady=10)

tk.Button(janela, text="Gerenciar Produtos", width=30, command=abrir_produtos).pack(pady=5)
tk.Button(janela, text="Controle de Estoque", width=30, command=abrir_estoque).pack(pady=5)
tk.Button(janela, text="Cadastro de Clientes", width=30, command=abrir_clientes).pack(pady=5)

janela.mainloop()
