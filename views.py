import flet as ft
from database import *
from ui_components import *

import datetime

class ProductView(ft.Column):
    def __init__(self):
        super().__init__()
        self.expand = True
        self.search_field = NeonTextField(label="Buscar Produto", on_change=self.search_products)
        self.products_list = ft.ListView(expand=True, spacing=10)
        self.controls = [
            PageHeader("Gerenciar Produtos"),
            ft.Row([self.search_field, NeonButton("Novo Produto", self.open_add_dialog, icon=ft.Icons.ADD)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Divider(color=NEON_BLUE),
            self.products_list
        ]
        self.load_products()

    def load_products(self, search=""):
        print("Carregando produtos...")
        self.products_list.controls.clear()
        produtos = get_produtos(search)
        print(f"Produtos encontrados: {len(produtos)}")
        for p in produtos:
            self.products_list.controls.append(
                GlassCard(
                    ft.Row([
                        ft.Column([
                            ft.Text(p['nome'], size=18, weight=ft.FontWeight.BOLD, color=NEON_BLUE),
                            ft.Text(f"Cat: {p['categoria']} | Qtd: {p['quantidade']}", color=TEXT_COLOR),
                        ], expand=True),
                        ft.Text(f"R$ {p['preco_venda']:.2f}", size=20, color=NEON_GREEN, weight=ft.FontWeight.BOLD),
                        ft.IconButton(ft.Icons.EDIT, icon_color=NEON_PURPLE, on_click=lambda e, id=p['id']: self.open_edit_dialog(id)),
                        ft.IconButton(ft.Icons.DELETE, icon_color=ft.Colors.RED, on_click=lambda e, id=p['id']: self.delete_product(id)),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                )
            )
        if self.page:
            self.update()

    def search_products(self, e):
        self.load_products(e.control.value)

    def delete_product(self, id):
        delete_produto(id)
        self.load_products()

    def open_add_dialog(self, e):
        print("Abrindo diálogo de novo produto...")
        self.open_product_dialog()

    def open_edit_dialog(self, id):
        # Simplificação: Buscar dados do produto pelo ID (não implementado no DB helper individualmente, mas ok)
        # Para simplificar, vou recarregar a lista e filtrar aqui ou adicionar get_produto_by_id no db
        # Vou assumir criação de novo por enquanto para não complicar demais o snippet
        self.open_product_dialog(id)

    def open_product_dialog(self, product_id=None):
        # Dialog fields
        nome = NeonTextField(label="Nome")
        categoria = NeonTextField(label="Categoria")
        preco_venda = NeonTextField(label="Preço Venda", keyboard_type=ft.KeyboardType.NUMBER)
        preco_compra = NeonTextField(label="Preço Compra", keyboard_type=ft.KeyboardType.NUMBER)
        quantidade = NeonTextField(label="Quantidade", keyboard_type=ft.KeyboardType.NUMBER)

        def save(e):
            print("Tentando salvar produto...")
            try:
                pv = float(preco_venda.value)
                pc = float(preco_compra.value) if preco_compra.value else 0.0
                qtd = int(quantidade.value)
                if product_id:
                    update_produto(product_id, nome.value, categoria.value, pv, pc, qtd)
                else:
                    add_produto(nome.value, categoria.value, pv, pc, qtd)
                    add_produto(nome.value, categoria.value, pv, pc, qtd)
                self.page.close(dialog)
                self.page.update()
                self.load_products()
            except ValueError:
                # Show error (snack bar would be good)
                pass

        dialog = ft.AlertDialog(
            title=ft.Text("Produto", color=NEON_BLUE),
            content=ft.Column([nome, categoria, preco_venda, preco_compra, quantidade], tight=True),
            actions=[
                NeonButton("Salvar", save),
                ft.TextButton("Cancelar", on_click=lambda e: self.page.close(dialog))
            ],
            bgcolor=CARD_BG
        )
        # self.page.dialog = dialog
        # dialog.open = True
        # self.page.update()
        self.page.open(dialog)

class ClientView(ft.Column):
    def __init__(self):
        super().__init__()
        self.expand = True
        self.search_field = NeonTextField(label="Buscar Cliente", on_change=self.search_clients)
        self.clients_list = ft.ListView(expand=True, spacing=10)
        self.controls = [
            PageHeader("Gerenciar Clientes"),
            ft.Row([self.search_field, NeonButton("Novo Cliente", self.open_add_dialog, icon=ft.Icons.PERSON_ADD)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Divider(color=NEON_BLUE),
            self.clients_list
        ]
        self.load_clients()

    def load_clients(self, search=""):
        self.clients_list.controls.clear()
        clientes = get_clientes(search)
        for c in clientes:
            self.clients_list.controls.append(
                GlassCard(
                    ft.Row([
                        ft.Column([
                            ft.Text(c['nome'], size=18, weight=ft.FontWeight.BOLD, color=NEON_BLUE),
                            ft.Text(f"Tel: {c['telefone']} | CPF: {c['cpf']}", color=TEXT_COLOR),
                        ], expand=True),
                        ft.IconButton(ft.Icons.HISTORY, icon_color=NEON_PURPLE, on_click=lambda e, id=c['id']: self.open_history_dialog(id)),
                        ft.IconButton(ft.Icons.DELETE, icon_color=ft.Colors.RED, on_click=lambda e, id=c['id']: self.delete_client(id)),
                    ])
                )
            )
        if self.page:
            self.update()

    def search_clients(self, e):
        self.load_clients(e.control.value)

    def delete_client(self, id):
        delete_cliente(id)
        self.load_clients()

    def open_add_dialog(self, e):
        nome = NeonTextField(label="Nome")
        telefone = NeonTextField(label="Telefone")
        cpf = NeonTextField(label="CPF")
        email = NeonTextField(label="Email")

        def save(e):
            print("Tentando salvar cliente...")
            add_cliente(nome.value, telefone.value, cpf.value, email.value)
            self.page.close(dialog)
            self.page.update()
            self.load_clients()

        dialog = ft.AlertDialog(
            title=ft.Text("Novo Cliente", color=NEON_BLUE),
            content=ft.Column([nome, telefone, cpf, email], tight=True),
            actions=[NeonButton("Salvar", save)],
            bgcolor=CARD_BG
        )
        # self.page.dialog = dialog
        # dialog.open = True
        # self.page.update()
        self.page.open(dialog)

    def open_history_dialog(self, client_id):
        historico = get_historico_compras(client_id)
        
        items_list = ft.ListView(height=300, spacing=10)
        for compra in historico:
            # compra: (id, total, data, status, itens)
            items_list.controls.append(
                GlassCard(
                    ft.Column([
                        ft.Row([
                            ft.Text(f"Data: {compra[2]}", color=TEXT_COLOR),
                            ft.Text(f"Status: {compra[3]}", color=NEON_RED if compra[3] == 'PENDENTE' else NEON_GREEN)
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.Text(f"Itens: {compra[4]}", color=TEXT_COLOR),
                        ft.Text(f"Total: R$ {compra[1]:.2f}", size=16, weight=ft.FontWeight.BOLD, color=NEON_BLUE)
                    ])
                )
            )
            
        dialog = ft.AlertDialog(
            title=ft.Text("Histórico de Compras", color=NEON_BLUE),
            content=items_list,
            actions=[ft.TextButton("Fechar", on_click=lambda e: self.page.close(dialog))],
            bgcolor=CARD_BG
        )
        self.page.open(dialog)

class SalesView(ft.Column):
    def __init__(self):
        super().__init__()
        self.expand = True
        self.cart = []
        self.client_id = None
        
        # UI Elements
        self.product_search = NeonTextField(label="Buscar Produto (Nome)", on_change=self.search_product)
        self.product_results = ft.ListView(height=200, spacing=5)
        self.cart_list = ft.ListView(expand=True, spacing=5)
        self.total_text = ft.Text("Total: R$ 0.00", size=25, weight=ft.FontWeight.BOLD, color=NEON_GREEN)
        self.client_dropdown = ft.Dropdown(
            label="Selecione o Cliente",
            options=[],
            border_color=NEON_BLUE,
            text_style=ft.TextStyle(color=TEXT_COLOR),
            bgcolor=with_opacity(0.1, NEON_BLUE)
        )
        self.fiado_checkbox = ft.Checkbox(label="Venda Fiado (Pendente)", label_style=ft.TextStyle(color=NEON_RED), fill_color=NEON_RED)
        
        self.controls = [
            PageHeader("Caixa / Vendas"),
            ft.Row([self.client_dropdown], alignment=ft.MainAxisAlignment.CENTER),
            ft.Divider(),
            ft.Row([
                ft.Column([
                    ft.Text("Adicionar Produtos", size=18, color=NEON_PURPLE),
                    self.product_search,
                    self.product_results
                ], expand=1),
                ft.VerticalDivider(width=1, color=NEON_BLUE),
                ft.Column([
                    ft.Text("Carrinho", size=18, color=NEON_PURPLE),
                    self.cart_list,
                    self.total_text,
                    self.fiado_checkbox,
                    NeonButton("Finalizar Venda", self.finish_sale, icon=ft.Icons.CHECK)
                ], expand=1)
            ], expand=True)
        ]
        self.load_clients()

    def load_clients(self):
        clients = get_clientes()
        self.client_dropdown.options = [ft.dropdown.Option(key=c['id'], text=c['nome']) for c in clients]

    def search_product(self, e):
        term = e.control.value
        self.product_results.controls.clear()
        if len(term) > 0:
            products = get_produtos(term)
            for p in products:
                self.product_results.controls.append(
                    ft.ListTile(
                        title=ft.Text(p['nome'], color=TEXT_COLOR),
                        subtitle=ft.Text(f"R$ {p['preco_venda']:.2f} | Est: {p['quantidade']}", color=NEON_BLUE),
                        on_click=lambda e, prod=p: self.add_to_cart(prod)
                    )
                )
        if self.page:
            self.update()

    def add_to_cart(self, product):
        # Check if already in cart
        for item in self.cart:
            if item['produto_id'] == product['id']:
                item['quantidade'] += 1
                self.update_cart_ui()
                return
        
        self.cart.append({
            'produto_id': product['id'],
            'nome': product['nome'],
            'quantidade': 1,
            'preco_unitario': product['preco_venda']
        })
        self.update_cart_ui()

    def update_cart_ui(self):
        self.cart_list.controls.clear()
        total = 0
        for item in self.cart:
            subtotal = item['quantidade'] * item['preco_unitario']
            total += subtotal
            self.cart_list.controls.append(
                GlassCard(
                    ft.Row([
                        ft.Text(f"{item['nome']} x{item['quantidade']}", color=TEXT_COLOR),
                        ft.Text(f"R$ {subtotal:.2f}", color=NEON_GREEN),
                        ft.IconButton(ft.Icons.REMOVE, icon_color=ft.Colors.RED, on_click=lambda e, pid=item['produto_id']: self.remove_from_cart(pid))
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    padding=10
                )
            )
        self.total_text.value = f"Total: R$ {total:.2f}"
        if self.page:
            self.update()

    def remove_from_cart(self, product_id):
        self.cart = [item for item in self.cart if item['produto_id'] != product_id]
        self.update_cart_ui()

    def finish_sale(self, e):
        if not self.client_dropdown.value:
            self.page.snack_bar = ft.SnackBar(ft.Text("Selecione um cliente!"))
            self.page.snack_bar.open = True
            self.page.update()
            return
        
        if not self.cart:
            return

        status = 'PENDENTE' if self.fiado_checkbox.value else 'PAGO'
        success = registrar_venda(self.client_dropdown.value, self.cart, status)
        if success:
            self.cart = []
            self.update_cart_ui()
            self.page.snack_bar = ft.SnackBar(ft.Text("Venda realizada com sucesso!", color=ft.Colors.GREEN))
            self.page.snack_bar.open = True
            self.page.update()
        else:
            self.page.snack_bar = ft.SnackBar(ft.Text("Erro ao realizar venda.", color=ft.Colors.RED))
            self.page.snack_bar.open = True
            self.page.update()

class DashboardView(ft.Column):
    def __init__(self):
        super().__init__()
        self.expand = True
        self.total_sales_text = ft.Text("R$ 0.00", size=30, weight=ft.FontWeight.BOLD, color=NEON_GREEN)
        self.total_items_text = ft.Text("0", size=30, weight=ft.FontWeight.BOLD, color=NEON_BLUE)
        self.total_invested_text = ft.Text("R$ 0.00", size=30, weight=ft.FontWeight.BOLD, color=NEON_PURPLE)
        self.total_profit_text = ft.Text("R$ 0.00", size=30, weight=ft.FontWeight.BOLD, color=NEON_GREEN)
        self.total_pending_text = ft.Text("R$ 0.00", size=30, weight=ft.FontWeight.BOLD, color=NEON_RED)
        
        self.controls = [
            PageHeader("Dashboard Financeiro"),
            ft.Row([
                self.build_stat_card("Faturamento (Pago)", self.total_sales_text, ft.Icons.ATTACH_MONEY, NEON_GREEN),
                self.build_stat_card("Lucro Líquido", self.total_profit_text, ft.Icons.TRENDING_UP, NEON_GREEN),
                self.build_stat_card("A Receber (Fiado)", self.total_pending_text, ft.Icons.MONEY_OFF, NEON_RED),
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
            ft.Container(height=10),
            ft.Row([
                self.build_stat_card("Total Investido (Estoque)", self.total_invested_text, ft.Icons.INVENTORY, NEON_PURPLE),
                self.build_stat_card("Itens Vendidos", self.total_items_text, ft.Icons.SHOPPING_BAG, NEON_BLUE),
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
            ft.Container(height=20),
            NeonButton("Atualizar Dados", self.load_data, icon=ft.Icons.REFRESH)
        ]
        self.load_data()

    def build_stat_card(self, title, value_control, icon, color):
        return GlassCard(
            ft.Column([
                ft.Icon(icon, size=40, color=color),
                ft.Text(title, size=14, color=TEXT_COLOR),
                value_control
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20
        )

    def load_data(self, e=None):
        stats = get_dashboard_stats()
        self.total_sales_text.value = f"R$ {stats['total_vendido']:.2f}"
        self.total_items_text.value = str(stats['total_itens'])
        self.total_invested_text.value = f"R$ {stats['total_investido']:.2f}"
        self.total_profit_text.value = f"R$ {stats['lucro_liquido']:.2f}"
        self.total_pending_text.value = f"R$ {stats['total_pendente']:.2f}"
        if self.page:
            self.update()

class DebtorsView(ft.Column):
    def __init__(self):
        super().__init__()
        self.expand = True
        self.debtors_list = ft.ListView(expand=True, spacing=10)
        self.controls = [
            PageHeader("Clientes Devedores"),
            self.debtors_list
        ]
        self.load_debtors()

    def load_debtors(self):
        self.debtors_list.controls.clear()
        devedores = get_devedores()
        if not devedores:
            self.debtors_list.controls.append(ft.Text("Nenhum cliente com débito pendente.", color=TEXT_COLOR))
        
        for d in devedores:
            # d: (id, nome, telefone, total_divida)
            self.debtors_list.controls.append(
                GlassCard(
                    ft.Row([
                        ft.Column([
                            ft.Text(d[1], size=18, weight=ft.FontWeight.BOLD, color=NEON_BLUE),
                            ft.Text(f"Tel: {d[2]}", color=TEXT_COLOR),
                        ], expand=True),
                        ft.Text(f"R$ {d[3]:.2f}", size=20, color=NEON_RED, weight=ft.FontWeight.BOLD),
                        NeonButton("Quitar Dívida", lambda e, id=d[0]: self.pay_debt(id), icon=ft.Icons.MONEY_OFF, color=NEON_GREEN)
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                )
            )
        if self.page:
            self.update()

    def pay_debt(self, client_id):
        quitar_divida(client_id)
        self.page.snack_bar = ft.SnackBar(ft.Text("Dívida quitada com sucesso!", color=ft.Colors.GREEN))
        self.page.snack_bar.open = True
        self.page.update()
        self.load_debtors()
