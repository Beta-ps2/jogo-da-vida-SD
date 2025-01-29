import pygame
import numpy as np
import time
from concurrent.futures import ThreadPoolExecutor

# Jogo da vida com paralelismo

# Definindo as cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)

VERMELHO = (75, 0, 0)
AZUL = (0, 0, 75)
VERDE = (0, 75, 0)

# Tamanho da grade
LARGURA = 800
ALTURA_DA_JANELA = 670 # 70 de margem para inserir os botões

ALTURA = 600 # altura maxima do jogo da vida
TAM_CELULA = 10

print("tamanho da grade: ", LARGURA/TAM_CELULA, "x", ALTURA/TAM_CELULA)

LINHAS = ALTURA // TAM_CELULA
COLUNAS = LARGURA // TAM_CELULA

# Inicializando o pygame
pygame.init()
tela = pygame.display.set_mode((LARGURA, ALTURA_DA_JANELA))
pygame.display.set_caption("Jogo da Vida com paralelismo")

# Função para inicializar a grade
def inicializar_grade():
    return np.zeros((LINHAS, COLUNAS))  # uma grade vazia
    
# Função para desenhar a grade com fundo alternado na altura e células vivas preenchidas de branco
def desenhar_grade(grade):
    for y in range(LINHAS):
        for x in range(COLUNAS):
            # Determinar a cor do fundo a cada 15 células na altura (y)
            # 15 = 1/4 de 60
            # 150 = 1/4 de 600
            if (y // 15) % 4 == 0:
                cor_fundo = PRETO
            elif (y // 15) % 4 == 1:
                cor_fundo = VERMELHO
            elif (y // 15) % 4 == 2:
                cor_fundo = VERDE
            else:
                cor_fundo = AZUL

            # Desenha o fundo primeiro
            pygame.draw.rect(tela, cor_fundo, (x * TAM_CELULA, y * TAM_CELULA, TAM_CELULA, TAM_CELULA))

            # Se a célula estiver viva, desenha ela preenchida de branco
            if grade[y, x] == 1:
                pygame.draw.rect(tela, BRANCO, (x * TAM_CELULA, y * TAM_CELULA, TAM_CELULA, TAM_CELULA))

# Função para contar os vizinhos vivos
def contar_vizinhos(grade, y, x):
    vizinhos = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            y_vizinho, x_vizinho = (y + i) % LINHAS, (x + j) % COLUNAS
            vizinhos += grade[y_vizinho, x_vizinho]
    return vizinhos

def atualizar_bloco(grade, y_inicio, y_fim):
    nova_grade = np.zeros_like(grade)
    for y in range(y_inicio, y_fim):
        for x in range(COLUNAS):
            vizinhos = contar_vizinhos(grade, y, x)
            if grade[y, x] == 1 and (vizinhos == 2 or vizinhos == 3):
                nova_grade[y, x] = 1
            elif grade[y, x] == 0 and vizinhos == 3:
                nova_grade[y, x] = 1
    return nova_grade

def atualizar_grade(grade):
    num_blocos = LINHAS // 15
    blocos = []
    with ThreadPoolExecutor(max_workers=num_blocos) as executor:
        for i in range(num_blocos):
            y_inicio = i * 15
            y_fim = min((i + 1) * 15, LINHAS)
            blocos.append(executor.submit(atualizar_bloco, grade, y_inicio, y_fim))

        # Coletando os resultados das threads
        resultados = [bloco.result() for bloco in blocos]

        # Combinando os resultados
        nova_grade = np.zeros_like(grade)
        for i, resultado in enumerate(resultados):
            y_inicio = i * 15
            y_fim = min((i + 1) * 15, LINHAS)
            nova_grade[y_inicio:y_fim, :] = resultado[y_inicio:y_fim, :]

        return nova_grade

# Função para desenhar o botão parar/iniciar a simulação
def desenhar_botao_parar_e_iniciar(parado):
    cor_botao = BRANCO
    # Definir posição e tamanho do botão
    botao_x = LARGURA - 780
    botao_y = 610
    botao_largura = 120
    botao_altura = 50

    # Desenha o botão
    pygame.draw.rect(tela, cor_botao, (botao_x, botao_y, botao_largura, botao_altura))

    texto = "Iniciar" if parado else "Parar"
    fonte = pygame.font.Font(None, 36)
    texto_surf = fonte.render(texto, True, PRETO)

    # Calculando a posição para centralizar o texto dentro do botão
    largura_texto = texto_surf.get_width()
    altura_texto = texto_surf.get_height()

    pos_x = botao_x + (botao_largura - largura_texto) // 2  # Centraliza horizontalmente
    pos_y = botao_y + (botao_altura - altura_texto) // 2  # Centraliza verticalmente

    tela.blit(texto_surf, (pos_x, pos_y))

    return botao_x, botao_y, botao_largura, botao_altura  # Retorna as dimensões do botão para usar no evento

# Função que desenha o botão de + FPS
def desenhar_botao_mais_fps(frames):
    cor_botao = BRANCO
    # Definir posição e tamanho do botão +
    botao_x = LARGURA - 650
    botao_y = 610
    botao_largura = 30
    botao_altura = 50

    # Definir posição e tamanho do botão -

    # Desenha o botão
    pygame.draw.rect(tela, cor_botao, (botao_x, botao_y, botao_largura, botao_altura))

    texto = "+"
    fonte = pygame.font.Font(None, 36)
    texto_surf = fonte.render(texto, True, PRETO)

    # Calculando a posição para centralizar o texto dentro do botão
    largura_texto = texto_surf.get_width()
    altura_texto = texto_surf.get_height()

    pos_x = botao_x + (botao_largura - largura_texto) // 2  # Centraliza horizontalmente
    pos_y = botao_y + (botao_altura - altura_texto) // 2  # Centraliza verticalmente

    tela.blit(texto_surf, (pos_x, pos_y))

    return botao_x, botao_y, botao_largura, botao_altura  # Retorna as dimensões do botão para usar no evento

# Função que desenha o botão de - FPS
def desenhar_botao_menos_fps(frames):
    cor_botao = BRANCO
    # Definir posição e tamanho do botão -
    botao_x = LARGURA - 610
    botao_y = 610
    botao_largura = 30
    botao_altura = 50

    # Desenha o botão
    pygame.draw.rect(tela, cor_botao, (botao_x, botao_y, botao_largura, botao_altura))

    texto = "-"
    fonte = pygame.font.Font(None, 36)
    texto_surf = fonte.render(texto, True, PRETO)

    # Calculando a posição para centralizar o texto dentro do botão
    largura_texto = texto_surf.get_width()
    altura_texto = texto_surf.get_height()

    pos_x = botao_x + (botao_largura - largura_texto) // 2  # Centraliza horizontalmente
    pos_y = botao_y + (botao_altura - altura_texto) // 2  # Centraliza verticalmente

    tela.blit(texto_surf, (pos_x, pos_y))

    return botao_x, botao_y, botao_largura, botao_altura  # Retorna as dimensões do botão para usar no evento

# Função que desenha o FPS do programa
def desenhar_quant_fps(frames):
    # Texto do FPS
    texto = f"FPS: {frames}"
    fonte = pygame.font.Font(None, 36)
    texto_surf = fonte.render(texto, True, BRANCO)  # Desenha o texto em BRANCO

    # Calcula a posição para o canto inferior direito (com margem de 10px)
    largura_texto = texto_surf.get_width()
    altura_texto = texto_surf.get_height()

    pos_x = LARGURA - largura_texto - 10  # 10 pixels de margem da borda direita
    pos_y = ALTURA - altura_texto + 50  # 10 pixels de margem da borda inferior

    # Desenha o texto na tela
    tela.blit(texto_surf, (pos_x, pos_y))

# Função principal
def main():
    grade = inicializar_grade()
    rodando = True
    parado = True  # Define que a simulação começa parada
    frames = 10  # Velocidade da atualização inicial (10 frames por segundo)
    relogio = pygame.time.Clock()
    tempo_inicial = 0
    tempo_total = 0

    while rodando:
        # Disposição inicial do programa
        tela.fill(PRETO)
        desenhar_grade(grade)

        # Botões
        desenhar_botao_parar_e_iniciar(parado)
        desenhar_botao_mais_fps(frames)
        desenhar_botao_menos_fps(frames)
        desenhar_quant_fps(frames)

        # Evento de clique no botão
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            if not parado:
                if tempo_inicial == 0:  # Iniciar o cronômetro
                    tempo_inicial = time.time()

                grade = atualizar_grade(grade)
            else:
                if tempo_inicial != 0:  # A simulação foi pausada, calcular o tempo decorrido
                    tempo_total += time.time() - tempo_inicial
                    tempo_inicial = 0

            # Exibir o tempo de execução enquanto a simulação está rodando
            if tempo_inicial != 0:
                tempo_decorrido = time.time() - tempo_inicial
            else:
                tempo_decorrido = tempo_total

            # Exibindo o tempo
            if tempo_decorrido != 0 and not parado:
                print(f"Tempo de Execução: {tempo_decorrido:.5f} segundos")

            if evento.type == pygame.MOUSEBUTTONDOWN:
                # Obtém as dimensões do botão de iniciar e parar
                btn_start_stop_x, btn_start_stop_y, btn_start_stop_largura, btn_start_stop_altura = desenhar_botao_parar_e_iniciar(parado)

                # Obtém as dimensões do botão de +
                btn_mais_fps_x, btn_mais_fps_y, btn_mais_fps_largura, btn_mais_fps_altura = desenhar_botao_mais_fps(frames)

                # Obtém as dimensões do botão de -
                btn_menos_fps_x, btn_menos_fps_y, btn_menos_fps_largura, btn_menos_fps_altura = desenhar_botao_menos_fps(frames)

                # Verifica se o clique ocorreu dentro da área do botão de iniciar e parar
                if btn_start_stop_x <= evento.pos[0] <= btn_start_stop_x + btn_start_stop_largura and btn_start_stop_y <= evento.pos[1] <= btn_start_stop_y + btn_start_stop_altura:
                    # Alterna o estado de parado/rodando quando o botão for clicado
                    parado = not parado

                # Verifica se o clique ocorreu dentro da área do botão MAIS fps
                if btn_mais_fps_x <= evento.pos[0] <= btn_mais_fps_x + btn_mais_fps_largura and btn_mais_fps_y <= evento.pos[1] <= btn_mais_fps_y + btn_mais_fps_altura:
                    frames = frames + 1

                # Verifica se o clique ocorreu dentro da área do botão MENOS fps
                if btn_menos_fps_x <= evento.pos[0] <= btn_menos_fps_x + btn_menos_fps_largura and btn_menos_fps_y <= evento.pos[1] <= btn_menos_fps_y + btn_menos_fps_altura:
                    frames = max(1, frames - 1) # garante que o frame nao seja negativo

                # Verifica se a simulação está parada e se o clique ocorreu em uma célula
                if parado:
                    # Calcula a posição da célula clicada na grade
                    x_celula = min(evento.pos[0] // TAM_CELULA,
                                   COLUNAS - 1)  # Garante que o índice não ultrapasse COLUNAS-1
                    y_celula = min(evento.pos[1] // TAM_CELULA,
                                   LINHAS - 1)  # Garante que o índice não ultrapasse LINHAS-1

                    # Alterna o estado da célula clicada (morta ou viva)
                    grade[y_celula, x_celula] = 1 - grade[y_celula, x_celula]

        if not parado:  # Se a simulação não estiver parada, atualiza a grade
            grade = atualizar_grade(grade)

        pygame.display.flip()
        relogio.tick(frames)

    pygame.quit()

if __name__ == "__main__":
    main()
