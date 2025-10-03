from pgzero.builtins import Rect, Actor

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
        
        self.color = (0, 80, 150)
        self.hover_color = (0, 120, 220)
        self.text_color = (255, 255, 255)

    def draw(self, screen, mouse_pos):
        """
        Desenha o botão na tela, mudando de cor se o mouse estiver sobre ele.
        É assim que o jogador sabe que pode interagir com o botão.
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
        Verifica se uma posição (geralmente o clique do mouse) está dentro da área do botão.
        Retorna True em caso afirmativo, False caso contrário.
        """
        return self.rect.collidepoint(pos)

class Menu:
    """
    Esta classe é responsável por gerenciar nosso menu principal.
    Ele lida com o título, o fundo e todos os botões com os quais o jogador pode interagir.
    """
    def __init__(self, width, height):
        self.title_text = "Game Of Jumps"
        self.title_pos = (width / 2, height / 4)
        
        self.background = Actor('menu_background.jpg')
        self.background.pos = width // 2, height // 2

        self.buttons = [
            Button("Iniciar Jogo", "start_game", (width / 2, height / 2)),
            Button("Música ON/OFF", "toggle_music", (width / 2, height / 2 + 70)),
            Button("Sair", "exit", (width / 2, height / 2 + 140))
        ]

    def draw(self, screen, mouse_pos):
        """
        Desenha o fundo, o título e todos os botões do menu na tela.
        """
        self.background.draw()
        screen.draw.text(
            self.title_text,
            center=self.title_pos,
            fontsize=60,
            color="yellow"
        )
        
        for button in self.buttons:
            button.draw(screen, mouse_pos)

    def handle_click(self, pos):
        """
        Este método é chamado quando o jogador clica com o mouse no menu.
        Ele verifica qual botão foi clicado e retorna a ação associada.
        """
        for button in self.buttons:
            if button.is_clicked(pos):
                return button.action
        return None
