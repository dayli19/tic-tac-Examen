import random
import json
import os
import time
from datetime import datetime 

KB_FILE = 'tic_tac_toe_kb.json'
GAME_HISTORY_FILE = 'game_history.json' #Historial de partida 

class KnowledgeBase:
    def __init__(self, filename=KB_FILE):
        self.filename = filename
        self.knowledge = {}
        self.load_knowledge()

    def load_knowledge(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    self.knowledge = json.load(f)
                print(f"Base de conocimiento cargada desde {self.filename}.")
            except json.JSONDecodeError:
                print(f"Error al decodificar JSON en {self.filename}. Iniciando KB vacía.")
                self.knowledge = {}
            except Exception as e:
                print(f"Error inesperado al cargar KB: {e}. Iniciando KB vacía.")
                self.knowledge = {}
        else:
            print(f"Archivo de base de conocimiento {self.filename} no encontrado. Creando nueva KB.")
            self.knowledge = {}

    def save_knowledge(self):
        try:
            with open(self.filename, 'w') as f:
                json.dump(self.knowledge, f, indent=4)
            print(f"Base de conocimiento guardada en {self.filename}.")
        except Exception as e:
            print(f"Error al guardar KB: {e}")

    def get_best_move(self, board_state_str):
        return self.knowledge.get(board_state_str)

    def add_new_knowledge(self, board_state_str, move_index):
        if board_state_str not in self.knowledge:
            self.knowledge[board_state_str] = move_index

class GameHistory:
    def __init__(self, filename=GAME_HISTORY_FILE):
        self.filename = filename
        self.history = []
        self.load_history()

    def load_history(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    loaded_data = json.load(f)
                    if isinstance(loaded_data, list):
                        self.history = loaded_data
                    else:
                        print(f"Advertencia: El archivo {self.filename} no contiene una lista válida. Iniciando historial vacío.")
                        self.history = []
                print(f"Historial de partidas cargado desde {self.filename}.")
            except json.JSONDecodeError:
                print(f"Error al decodificar JSON en {self.filename}. Iniciando historial vacío.")
                self.history = []
            except Exception as e:
                print(f"Error inesperado al cargar historial: {e}. Iniciando historial vacío.")
                self.history = []
        else:
            print(f"Archivo de historial de partidas {self.filename} no encontrado. Creando nuevo historial.")
            self.history = []

    def save_history(self):
        try:
            with open(self.filename, 'w') as f:
                json.dump(self.history, f, indent=4)
            print(f"Historial de partidas guardado en {self.filename}.")
        except Exception as e:
            print(f"Error al guardar historial: {e}")

    def add_game_record(self, record):
        self.history.append(record) 

class TicTacToe:
    def __init__(self):
        self.board = ['_' for _ in range(9)]  #representa una casilla vacia 
        self.current_player = 'X' #Que el jugador puede ser X o O 
        self.game_over = False
        self.winner = None

    def display_board(self): #limpia y muestra el tablero actual 
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n--- Tres en Raya ---")
        print("  0 | 1 | 2")
        print(f" {self.board[0]} | {self.board[1]} | {self.board[2]}")
        print(" ---+---+---")
        print("  3 | 4 | 5")
        print(f" {self.board[3]} | {self.board[4]} | {self.board[5]}")
        print(" ---+---+---")
        print("  6 | 7 | 8")
        print(f" {self.board[6]} | {self.board[7]} | {self.board[8]}")
        print("--------------------\n")

    def get_board_state_str(self): #convierte a un cadena 
        return "".join(self.board)

    def is_valid_move(self, position): 
        return 0 <= position <= 8 and self.board[position] == '_'

    def make_move(self, position, player):
        if self.is_valid_move(position):
            self.board[position] = player
            return True
        return False

    def check_win(self, player):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8], 
            [0, 3, 6], [1, 4, 7], [2, 5, 8], 
            [0, 4, 8], [2, 4, 6]             
        ]
        for combo in winning_combinations:
            if all(self.board[i] == player for i in combo):
                self.game_over = True
                self.winner = player
                return True
        return False

    def check_draw(self):
        if '_' not in self.board and not self.winner:
            self.game_over = True
            return True
        return False

    def reset_game(self):
        self.board = ['_' for _ in range(9)]
        self.current_player = 'X'
        self.game_over = False
        self.winner = None

class AIPlayer:
    def __init__(self, kb: KnowledgeBase, ai_symbol='O'):
        self.kb = kb
        self.ai_symbol = ai_symbol
        self.moves_history = []

    def get_move(self, game: TicTacToe):
        board_state = game.get_board_state_str()
        recommended_move = self.kb.get_best_move(board_state)

        if recommended_move is not None and game.is_valid_move(recommended_move):
            move = recommended_move
        else:
            available_moves = [i for i, cell in enumerate(game.board) if cell == '_']
            if available_moves:
                move = random.choice(available_moves)
            else:
                return -1 
        self.moves_history.append((board_state, move))
        return move

    def reset_history(self):
        self.moves_history = []

    def learn_from_game(self, game_result):
        if game_result == 'win':
            print("Máquina: ¡He ganado! Aprendiendo de mis movimientos...")
            for board_state_str, move_index in self.moves_history:
                self.kb.add_new_knowledge(board_state_str, move_index)
        elif game_result == 'lose':
            print("Máquina: He perdido. Necesito mejorar! FELICDADES PARA TI!")
            pass 
        else: 
            print("Máquina: Empate. Seguiremos aprendiendo y mejorando.")
            pass 
def play_game():
    kb = KnowledgeBase() 
    game_history_manager = GameHistory() 
    game = TicTacToe()
    ai_player = AIPlayer(kb)

    play_again = True
    while play_again:
        game.reset_game()
        ai_player.reset_history() 

        # Variables para registrar la partida
        user_symbol = ''
        ai_symbol = ''
        first_player_choice = ''
        moves_in_this_game = [] 
        current_winner = 'draw' 

        while True:
            first_player_choice = input("¿Quién tira primero? (usuario/máquina): ").lower()
            if first_player_choice in ['usuario', 'máquina']:
                break
            else:
                print("Opción incorrecta. Por favor, escribe 'usuario' o 'máquina'.")
        
        if first_player_choice == 'usuario':
            while True:
                user_symbol = input("¿Qué ficha quieres usar? (X/O): ").upper()
                if user_symbol in ['X', 'O']:
                    ai_symbol = 'O' if user_symbol == 'X' else 'X'
                    print(f"¡Empieza el usuario ({user_symbol})!")
                    break
                else:
                    print("Ficha incorrecta. Por favor, elige 'X' o 'O'.")
        else: 
            ai_symbol = random.choice(['X', 'O'])
            user_symbol = 'O' if ai_symbol == 'X' else 'X'
            print(f"¡Empieza la máquina ({ai_symbol})!")
            print(f"Tu ficha será: {user_symbol}")

        current_turn_player = user_symbol if first_player_choice == 'usuario' else ai_symbol
        game.current_player = current_turn_player 
        ai_player.ai_symbol = ai_symbol 

        while not game.game_over:
            game.display_board()

            if game.current_player == user_symbol:
                while True:
                    try:
                        user_move = int(input(f"Turno del usuario ({user_symbol}). Ingresa tu tiro (0-8): "))
                        if game.is_valid_move(user_move):
                            game.make_move(user_move, user_symbol)
                            moves_in_this_game.append(f"Usuario({user_symbol}) tiró en {user_move}")
                            break
                        else:
                            print("Jugada incorrecta. Esa casilla ya está ocupada o fuera de rango. Intenta de nuevo.")
                    except ValueError:
                        print("Entrada incorrecta. Por favor, ingresa un número entre 0 y 8.")
            else: # Turno de la IA
                print(f"Turno de la máquina ({ai_symbol})...")
                time.sleep(1) 
                ai_move = ai_player.get_move(game)
                game.make_move(ai_move, ai_symbol)
                moves_in_this_game.append(f"Máquina({ai_symbol}) tiró en {ai_move}")

        
            if game.check_win(game.current_player):
                game.display_board()
                print(f"¡{game.winner} ha ganado!")
                current_winner = 'usuario' if game.winner == user_symbol else 'máquina'
                if game.winner == ai_symbol:
                    ai_player.learn_from_game('win')
                else:
                    ai_player.learn_from_game('lose')
                break # Salir del bucle del juego

            if game.check_draw():
                game.display_board()
                print("¡Es un empate!")
                current_winner = 'empate'
                ai_player.learn_from_game('draw')
                break # Salir del bucle del juego

            # Cambiar de jugador
            game.current_player = user_symbol if game.current_player == ai_symbol else ai_symbol
        
        game_record = {
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
            "jugador_usuario": user_symbol,
            "jugador_maquina": ai_symbol,
            "primero_en_tirar": first_player_choice,
            "ganador": current_winner,
            "movimientos": moves_in_this_game
        }
        game_history_manager.add_game_record(game_record)
        game_history_manager.save_history()
        
        kb.save_knowledge() # Guardar la base de conocimiento de la IA (si hubo victorias de la IA)

        respuesta = input("¿Quieres jugar de nuevo? (si/no): ").lower()
        if respuesta != 's':
            play_again = False
            print("¡Gracias por jugar, Me diverti mucho! La base de conocimiento y el historial de partidas han sido actualizados.")

# Iniciar el juego
if __name__ == "__main__":
    play_game()
