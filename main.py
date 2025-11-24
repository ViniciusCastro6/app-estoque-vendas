import flet as ft
from database import init_db
from ui_components import get_theme, NEON_BLUE, NEON_RED, DARK_BG, TEXT_COLOR, with_opacity
from views import ProductView, ClientView, SalesView, DashboardView, DebtorsView

def main(page: ft.Page):
    # Inicializar Banco de Dados
    init_db()

    # Configuração da Página
    page.title = "Sistema de Estoque e Vendas Futurista"
    page.theme = get_theme()
    page.bgcolor = DARK_BG
    page.padding = 0
    page.window_icon = "icon.jpg"
    
    # Views
    product_view = ProductView()
    client_view = ClientView()
    sales_view = SalesView()
    dashboard_view = DashboardView()
    debtors_view = DebtorsView()

    # Container principal que mudará de conteúdo
    main_content = ft.Container(
        content=dashboard_view,
        expand=True,
        padding=20
    )

    def change_view(e, view_name):
        print(f"Navegando para: {view_name}")
        if view_name == "dashboard":
            main_content.content = dashboard_view
            dashboard_view.load_data() # Atualiza dados ao entrar
        elif view_name == "produtos":
            main_content.content = product_view
            product_view.load_products()
        elif view_name == "clientes":
            main_content.content = client_view
            client_view.load_clients()
        elif view_name == "vendas":
            main_content.content = sales_view
            sales_view.load_clients() # Recarrega clientes no dropdown
        elif view_name == "devedores":
            main_content.content = debtors_view
            debtors_view.load_debtors()
        
        page.update()
        print("Page updated")

    # Sidebar de Navegação
    sidebar = ft.Container(
        width=250,
        bgcolor=with_opacity(0.05, NEON_BLUE),
        padding=20,
        content=ft.Column([
            ft.Text("Castro Mobile\nEstoque e Vendas", size=20, weight=ft.FontWeight.BOLD, color=NEON_BLUE, text_align=ft.TextAlign.CENTER),
            ft.Divider(color=NEON_BLUE),
            ft.Container(height=20),
            ft.ListTile(leading=ft.Icon(ft.Icons.DASHBOARD, color=NEON_BLUE), title=ft.Text("Dashboard", color=TEXT_COLOR), on_click=lambda e: change_view(e, "dashboard")),
            ft.ListTile(leading=ft.Icon(ft.Icons.INVENTORY_2, color=NEON_BLUE), title=ft.Text("Produtos", color=TEXT_COLOR), on_click=lambda e: change_view(e, "produtos")),
            ft.ListTile(leading=ft.Icon(ft.Icons.PEOPLE, color=NEON_BLUE), title=ft.Text("Clientes", color=TEXT_COLOR), on_click=lambda e: change_view(e, "clientes")),
            ft.ListTile(leading=ft.Icon(ft.Icons.POINT_OF_SALE, color=NEON_BLUE), title=ft.Text("Caixa", color=TEXT_COLOR), on_click=lambda e: change_view(e, "vendas")),
            ft.ListTile(leading=ft.Icon(ft.Icons.MONEY_OFF, color=NEON_RED), title=ft.Text("Devedores", color=TEXT_COLOR), on_click=lambda e: change_view(e, "devedores")),
        ])
    )

    # Layout Principal
    page.add(
        ft.Row(
            [
                sidebar,
                ft.VerticalDivider(width=1, color=NEON_BLUE),
                main_content
            ],
            expand=True
        )
    )

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
