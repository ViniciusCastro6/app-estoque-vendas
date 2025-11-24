import flet as ft
from database import *
from ui_components import *

import datetime

class ProductView(ft.Column):
    def __init__(self):
        super().__init__()
        self.expand = True
        self.search_field = NeonTextField(label="Buscar Produto", on_change=self.search_products)
        
        # Filter Controls
        self.category_filter = ft.Dropdown(label="Categoria", options=[], width=200, border_color=NEON_BLUE, text_style=ft.TextStyle(color=TEXT_COLOR), bgcolor=with_opacity(0.1, NEON_BLUE), on_change=self.apply_filters)
        self.min_price = NeonTextField(label="Min R$", width=100, keyboard_type=ft.KeyboardType.NUMBER, on_change=self.apply_filters)
        self.max_price = NeonTextField(label="Max R$", width=100, keyboard_type=ft.KeyboardType.NUMBER, on_change=self.apply_filters)
        self.low_stock_filter = ft.Checkbox(label="Baixo Estoque", label_style=ft.TextStyle(color=TEXT_COLOR), on_change=self.apply_filters)
        self.out_of_stock_filter = ft.Checkbox(label="Esgotado", label_style=ft.TextStyle(color=TEXT_COLOR), on_change=self.apply_filters)
        self.best_sellers_filter = ft.Checkbox(label="Mais Vendidos", label_style=ft.TextStyle(color=TEXT_COLOR), on_change=self.apply_filters)
        self.inactive_filter = ft.Checkbox(label="Inativos", label_style=ft.TextStyle(color=TEXT_COLOR), on_change=self.apply_filters)
        
        # Sorting Controls
        self.sort_option = None # Default
        self.sort_buttons = ft.Row([
            ft.Text("Ordenar por:", color=NEON_BLUE),
            NeonButton("A-Z", lambda e: self.set_sort("name_asc"), icon=ft.Icons.SORT_BY_ALPHA, width=100),
            NeonButton("Preço", lambda e: self.set_sort("price_asc"), icon=ft.Icons.ATTACH_MONEY, width=100),
            NeonButton("Estoque", lambda e: self.set_sort("stock_desc"), icon=ft.Icons.INVENTORY, width=110),
            NeonButton("Recentes", lambda e: self.set_sort("date_desc"), icon=ft.Icons.NEW_RELEASES, width=120),
        ], scroll=ft.ScrollMode.AUTO)

        self.products_list = ft.ListView(expand=True, spacing=10)
        self.controls = [
            PageHeader("Gerenciar Produtos"),
            ft.Row([self.search_field, NeonButton("Novo Produto", self.open_add_dialog, icon=ft.Icons.ADD)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.ExpansionTile(
                title=ft.Text("Filtros Avançados", color=NEON_BLUE),
                controls=[
                    ft.Column([
                        ft.Row([self.category_filter, self.min_price, self.max_price], wrap=True),
                        ft.Row([self.low_stock_filter, self.out_of_stock_filter, self.best_sellers_filter, self.inactive_filter], wrap=True),
                        ft.Divider(color=with_opacity(0.5, NEON_BLUE)),
                        self.sort_buttons,
                        ft.Container(height=10),
                        NeonButton("Limpar Filtros", self.clear_filters, icon=ft.Icons.CLEAR_ALL)
                    ], scroll=ft.ScrollMode.AUTO)
                ]
            ),
            ft.Divider(color=NEON_BLUE),
            self.products_list
        ]
        self.load_products()

    def set_sort(self, sort_value):
        self.sort_option = sort_value
        self.load_products()

    def clear_filters(self, e):
        self.search_field.value = ""
        self.category_filter.value = None
        self.min_price.value = ""
        self.max_price.value = ""
        self.low_stock_filter.value = False
        self.out_of_stock_filter.value = False
        self.best_sellers_filter.value = False
        self.inactive_filter.value = False
        self.sort_option = None
        self.update()
        self.load_products()

    def apply_filters(self, e):
        self.load_products()

    def load_products(self, search=""):
        print("Carregando produtos...")
        # Update categories dropdown
        categories = get_unique_categories()
        self.category_filter.options = [ft.dropdown.Option(c) for c in categories]
        
        self.products_list.controls.clear()
        
        # Get filter values
        cat = self.category_filter.value
        min_p = self.min_price.value
        max_p = self.max_price.value
        low_s = self.low_stock_filter.value
        out_s = self.out_of_stock_filter.value
        best_s = self.best_sellers_filter.value
        show_inactive = self.inactive_filter.value
        
        # Determine inactive logic: if checked, show ALL (or maybe just inactive? User said "Filtrar por produtos inativos")
        # Usually "Filter by inactive" means SHOW inactive. 
        # If I want to show ONLY inactive, I might need a different logic.
        # Let's assume:
        # - Default: Active only
        # - "Inativos" checked: Show Inactive (or All?)
        # Let's implement: "Inativos" checked -> Show ONLY inactive (to act as a filter). 
        # Wait, usually "Show Inactive" toggle means "Include Inactive". 
        # But the user said "Filtrar por...", implying narrowing down.
        # Let's make it a tri-state or just assume if checked, we show inactive. 
        # Actually, let's stick to: If checked, show ONLY inactive. If unchecked, show ONLY active.
        # Or maybe: If checked, show ALL. 
        # Let's look at the user request: "Filtrar por produtos inativos". This sounds like "Show me the inactive ones".
        # So:
        # - Unchecked: Active Only (default)
        # - Checked: Inactive Only
        
        inactive_mode = "only_inactive" if show_inactive else False

        produtos = get_produtos(
            search_term=self.search_field.value,
            category=cat,
            min_price=min_p,
            max_price=max_p,
            low_stock=low_s,
            out_of_stock=out_s,
            best_sellers=best_s,
            show_inactive=inactive_mode,
            sort_by=self.sort_option
        )
        
        print(f"Produtos encontrados: {len(produtos)}")
        for p in produtos:
            status_color = TEXT_COLOR
            if p['quantidade'] == 0:
                status_color = NEON_RED
            
            name_style = ft.TextStyle(size=18, weight=ft.FontWeight.BOLD, color=NEON_BLUE)
            if p['ativo'] == 0:
                name_style.decoration = ft.TextDecoration.LINE_THROUGH
                name_style.color = ft.Colors.GREY
            
            # Quick View Trigger (Clickable Card)
            card_content = ft.Container(
                content=ft.Row([
                    ft.Column([
                        ft.Text(p['nome'], style=name_style),
                        ft.Text(f"Cat: {p['categoria']} | Qtd: {p['quantidade']}", color=status_color),
                        ft.Text("INATIVO" if p['ativo'] == 0 else "ATIVO", size=10, color=ft.Colors.GREY if p['ativo'] == 0 else NEON_GREEN)
                    ], expand=True),
                    ft.Text(f"R$ {p['preco_venda']:.2f}", size=20, color=NEON_GREEN, weight=ft.FontWeight.BOLD),
                    # Edit/Delete buttons moved to Quick View or kept here? 
                    # User said "Ao clicar no card, abrir um popup". 
                    # Keeping quick actions here is good UX, but let's make the whole card clickable for Quick View.
                    # But if I click the buttons, it shouldn't open Quick View.
                    # Flet's Container on_click covers everything unless children handle clicks.
                    # So buttons will still work.
                    ft.Row([
                        ft.IconButton(ft.Icons.EDIT, icon_color=NEON_PURPLE, on_click=lambda e, id=p['id'], p_data=p: self.open_edit_dialog(id, p_data)),
                        ft.IconButton(ft.Icons.DELETE, icon_color=ft.Colors.RED, on_click=lambda e, id=p['id']: self.delete_product(id)),
                    ])
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                on_click=lambda e, p_data=p: self.open_quick_view(p_data)
            )

            self.products_list.controls.append(
                GlassCard(
                    card_content
                )
            )
        if self.page:
            self.update()

    def open_quick_view(self, p):
        # p is a Row object from sqlite3, behaves like dict
        
        # Content for Quick View
        # Foto (Placeholder if empty)
        foto_url = p['foto'] if p['foto'] else "https://via.placeholder.com/150"
        img = ft.Image(src=foto_url, width=150, height=150, fit=ft.ImageFit.COVER, border_radius=10)
        
        details = ft.Column([
            ft.Text(p['nome'], size=24, weight=ft.FontWeight.BOLD, color=NEON_BLUE),
            ft.Text(f"Categoria: {p['categoria']}", color=TEXT_COLOR),
            ft.Text(f"Preço Venda: R$ {p['preco_venda']:.2f}", color=NEON_GREEN, size=18, weight=ft.FontWeight.BOLD),
            ft.Text(f"Preço Compra: R$ {p['preco_compra']:.2f}", color=TEXT_COLOR),
            ft.Text(f"Estoque: {p['quantidade']}", color=NEON_BLUE if p['quantidade'] > 5 else NEON_RED, weight=ft.FontWeight.BOLD),
            ft.Divider(color=NEON_BLUE),
            ft.Text(f"Código de Barras: {p['codigo_barras'] or 'N/A'}", color=TEXT_COLOR),
            ft.Text(f"Fornecedor: {p['fornecedor'] or 'N/A'}", color=TEXT_COLOR),
            ft.Text("Descrição:", color=NEON_PURPLE),
            ft.Text(p['descricao'] or "Sem descrição.", color=TEXT_COLOR, italic=True),
        ], expand=True, scroll=ft.ScrollMode.AUTO)
        
        content = ft.Row([
            ft.Column([img], alignment=ft.MainAxisAlignment.START),
            ft.VerticalDivider(width=20, color=with_opacity(0.2, NEON_BLUE)),
            details
        ], height=400, width=600)
        
        def close_dialog(e):
            self.page.close(dialog)

        dialog = ft.AlertDialog(
            content=content,
            actions=[
                NeonButton("Editar", lambda e: [close_dialog(e), self.open_edit_dialog(p['id'], p)], icon=ft.Icons.EDIT),
                NeonButton("Movimentações", lambda e: self.show_movements(p['id'], p['nome']), icon=ft.Icons.HISTORY),
                ft.TextButton("Fechar", on_click=close_dialog)
            ],
            bgcolor=CARD_BG,
            title=ft.Text("Detalhes do Produto", color=NEON_BLUE)
        )
        self.page.open(dialog)

    def show_movements(self, product_id, product_name):
        movements = get_produto_movimentacoes(product_id)
        
        list_view = ft.ListView(expand=True, spacing=10)
        if not movements:
            list_view.controls.append(ft.Text("Nenhuma movimentação registrada.", color=TEXT_COLOR))
        else:
            for m in movements:
                # m: (data, id, nome_cliente, quantidade, preco_unitario, status)
                list_view.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Text(f"{m[0]}", color=TEXT_COLOR, size=12),
                            ft.Text(f"Venda #{m[1]} - {m[2] or 'Cliente não ident.'}", color=NEON_BLUE),
                            ft.Text(f"Qtd: {m[3]}", color=TEXT_COLOR),
                            ft.Text(f"R$ {m[4]:.2f}", color=NEON_GREEN),
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        padding=10,
                        border=ft.border.only(bottom=ft.BorderSide(1, with_opacity(0.2, NEON_BLUE)))
                    )
                )

        dialog = ft.AlertDialog(
            title=ft.Text(f"Movimentações: {product_name}", color=NEON_BLUE),
            content=ft.Container(list_view, height=300, width=500),
            actions=[ft.TextButton("Fechar", on_click=lambda e: self.page.close(dialog))],
            bgcolor=CARD_BG
        )
        self.page.open(dialog)

    def search_products(self, e):
        self.load_products(e.control.value)

    def delete_product(self, id):
        delete_produto(id)
        self.load_products()

    def open_add_dialog(self, e):
        print("Abrindo diálogo de novo produto...")
        self.open_product_dialog()

    def open_edit_dialog(self, id, p_data=None):
        # Se p_data for passado, usamos ele. Se não, idealmente buscaríamos do DB.
        # Como simplificação, vou assumir que p_data é passado ou recarregar tudo.
        # Mas para editar corretamente, preciso dos dados.
        # Vou modificar a chamada no load_products para passar o objeto produto.
        self.open_product_dialog(id, p_data)

    def open_product_dialog(self, product_id=None, product_data=None):
        # Dialog fields
        nome = NeonTextField(label="Nome", value=product_data['nome'] if product_data else "")
        categoria = NeonTextField(label="Categoria", value=product_data['categoria'] if product_data else "", expand=True)
        preco_venda = NeonTextField(label="Preço Venda", keyboard_type=ft.KeyboardType.NUMBER, value=str(product_data['preco_venda']) if product_data else "", expand=True)
        preco_compra = NeonTextField(label="Preço Compra", keyboard_type=ft.KeyboardType.NUMBER, value=str(product_data['preco_compra']) if product_data and product_data['preco_compra'] else "", expand=True)
        quantidade = NeonTextField(label="Quantidade", keyboard_type=ft.KeyboardType.NUMBER, value=str(product_data['quantidade']) if product_data else "", expand=True)
        
        # New Fields
        codigo_barras = NeonTextField(label="Cód. Barras", value=product_data['codigo_barras'] if product_data and product_data['codigo_barras'] else "", expand=True)
        fornecedor = NeonTextField(label="Fornecedor", value=product_data['fornecedor'] if product_data and product_data['fornecedor'] else "")
        foto = NeonTextField(label="URL Foto", value=product_data['foto'] if product_data and product_data['foto'] else "")
        descricao = NeonTextField(label="Descrição", multiline=True, value=product_data['descricao'] if product_data and product_data['descricao'] else "")
        
        ativo_switch = ft.Switch(label="Ativo", value=bool(product_data['ativo']) if product_data else True, active_color=NEON_GREEN)

        def save(e):
            print("Tentando salvar produto...")
            try:
                pv = float(preco_venda.value)
                pc = float(preco_compra.value) if preco_compra.value else 0.0
                qtd = int(quantidade.value)
                ativo = 1 if ativo_switch.value else 0
                
                if product_id:
                    update_produto(product_id, nome.value, categoria.value, pv, pc, qtd, ativo, foto.value, codigo_barras.value, descricao.value, fornecedor.value)
                else:
                    add_produto(nome.value, categoria.value, pv, pc, qtd, ativo, foto.value, codigo_barras.value, descricao.value, fornecedor.value)
                
                self.page.close(dialog)
                self.page.update()
                self.load_products()
            except ValueError:
                # Show error (snack bar would be good)
                pass

        content_col = ft.Column([
            nome, 
            ft.Row([categoria, codigo_barras]),
            ft.Row([preco_venda, preco_compra, quantidade]),
            fornecedor,
            foto,
            descricao,
            ativo_switch
        ], tight=True, scroll=ft.ScrollMode.AUTO)

        dialog = ft.AlertDialog(
            title=ft.Text("Editar Produto" if product_id else "Novo Produto", color=NEON_BLUE),
            content=ft.Container(content_col, width=600, height=500),
            actions=[
                NeonButton("Salvar", save),
                ft.TextButton("Cancelar", on_click=lambda e: self.page.close(dialog))
            ],
            bgcolor=CARD_BG
        )
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
