import flet as ft

# Cores do Tema Futurista
NEON_BLUE = "#00F3FF"
NEON_PURPLE = "#BC13FE"
NEON_GREEN = "#00FF94"
NEON_RED = "#FF0055"
DARK_BG = "#0A0A12"
CARD_BG = "#161622"
TEXT_COLOR = "#FFFFFF"

def with_opacity(opacity, color):
    return f"#{int(opacity * 255):02x}{color.lstrip('#')}"


def get_theme():
    return ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=NEON_BLUE,
            secondary=NEON_PURPLE,
            background=DARK_BG,
            surface=CARD_BG,
            on_background=TEXT_COLOR,
            on_surface=TEXT_COLOR,
        ),
        font_family="Roboto", # Ou uma fonte mais futurista se disponível
        # visual_density=ft.ThemeVisualDensity.COMFORTABLE,
    )

class NeonButton(ft.ElevatedButton):
    def __init__(self, text, on_click, icon=None, color=NEON_BLUE, **kwargs):
        super().__init__(text=text, on_click=on_click, **kwargs)
        # self.text = text # Already handled by super
        # self.on_click = on_click # Already handled by super
        self.icon = icon
        self.style = ft.ButtonStyle(
            color=ft.Colors.BLACK,
            bgcolor=color,
            shape=ft.RoundedRectangleBorder(radius=8),
            elevation=10,
            shadow_color=color,
            animation_duration=300,
        )

class GlassCard(ft.Container):
    def __init__(self, content, padding=20):
        super().__init__()
        self.content = content
        self.padding = padding
        self.bgcolor = with_opacity(0.7, CARD_BG)
        self.border_radius = 15
        self.border = ft.border.all(1, with_opacity(0.3, NEON_BLUE))
        self.blur = ft.Blur(10, 10, ft.BlurTileMode.MIRROR)
        self.shadow = ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=with_opacity(0.2, NEON_BLUE),
        )

class NeonTextField(ft.TextField):
    def __init__(self, label, **kwargs):
        super().__init__(**kwargs)
        self.label = label
        self.border_color = NEON_BLUE
        self.focused_border_color = NEON_PURPLE
        self.text_style = ft.TextStyle(color=TEXT_COLOR)
        self.label_style = ft.TextStyle(color=NEON_BLUE)
        self.bgcolor = with_opacity(0.1, NEON_BLUE)
        self.border_radius = 8

def PageHeader(title):
    return ft.Container(
        content=ft.Text(
            title, 
            size=30, 
            weight=ft.FontWeight.BOLD, 
            color=NEON_BLUE,
            font_family="Consolas" # Fonte monospaced dá um ar mais tech
        ),
        padding=ft.padding.only(bottom=20)
    )
