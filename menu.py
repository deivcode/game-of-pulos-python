from pgzero.builtins import Rect, Actor

# -----------------------------------------------
# Menu
# -----------------------------------------------
class Button:
    """
    Uma classe para criar botões clicáveis e desenháveis para o nosso menu.
    Cada botão tem um texto, uma ação e sua própria aparência.
    """
    def __init__(self, text, action, pos, size=(200, 50)):
        self.rect = Rect(0, 0, size[0], size[1])
        self.rect.center = pos
        self.text = text
        self.action = action
        
        self.color = (54, 111, 77)
        self.hover_color = (74, 131, 97)
        self.text_color = (255, 255, 255)

    def draw(self, screen, mouse_pos):
        """
        Desenha o botão na tela, mudando de cor se o mouse estiver sobre ele.
        É assim que o jogador sabe que pode interagir com o botão. Pensando mais na UX
        """
        if self.rect.collidepoint(mouse_pos):
            screen.draw.filled_rect(self.rect, self.hover_color)
        else:
            screen.draw.filled_rect(self.rect, self.color)
        
        screen.draw.text(
            self.text,
            center=self.rect.center,
            color=self.text_color,
            fontsize=32
        )

    def is_clicked(self, pos):
        """
        Verifica se uma posição  está dentro da área do botão.
        Retorna True em caso afirmativo, False caso contrário.
        """
        return self.rect.collidepoint(pos)

class Menu:
    """
    Esta classe é responsável por gerenciar nosso menu principal.
    Ele lida com o título, o fundo e todos os botões com os quais o jogador pode interagir.
    """
    def __init__(self, width, height):
        self.background = Actor('background_menu.png')
        self.background.pos = width // 2, height // 2

        self.is_music_on = True # Adiciona o estado da música

        # Posições dos botões foram abaixadas
        self.buttons = [
            Button("Iniciar Jogo", "start_game", (width / 2, height / 2 + 50)),
            Button("Música/Sons ON", "toggle_music", (width / 2, height / 2 + 120)),
            Button("Sair", "exit", (width / 2, height / 2 + 190))
        ]

    def draw(self, screen, mouse_pos):
        """
        Desenha o fundo, o título e todos os botões do menu na tela.
        """
        self.background.draw()
        # O título de texto foi removido
        
        # Atualiza o texto do botão de música antes de desenhar
        for button in self.buttons:
            if button.action == "toggle_music":
                button.text = "Música ON" if self.is_music_on else "Música OFF"
            button.draw(screen, mouse_pos)

    def handle_click(self, pos):
        """
        Este método é chamado quando o jogador clica com o mouse no menu.
        Ele verifica qual botão foi clicado e retorna a ação associada.
        """
        for button in self.buttons:
            if button.is_clicked(pos):
                if button.action == "toggle_music":
                    self.is_music_on = not self.is_music_on # Alterna o estado da música
                return button.action
        return None
