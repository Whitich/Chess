import tkinter as tk

class ChessGameGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Chess")
        self.white_king_moved = False
        self.black_king_moved = False
        self.white_rook_moved = {'short': False, 'long': False}
        self.black_rook_moved = {'short': False, 'long': False}
        self.board = [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ]

        self.current_player = 'white'

        # Sütun etiketleri (a - h)
        for col, col_label in enumerate(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']):
            tk.Label(master, text=col_label, width=4, height=2).grid(row=8, column=col)

        # Satır etiketleri (1 - 8)
        for row_label in range(8, 0, -1):
            tk.Label(master, text=row_label, width=4, height=2).grid(row=8-row_label, column=8)



        self.buttons = [[None]*8 for _ in range(8)]
        for i in range(8):
            for j in range(8):
                # Dama desenini oluştur
                color = '#ffffff' if (i+j) % 2 == 0 else '#a9a9a9'
                self.buttons[i][j] = tk.Button(master, text=self.board[i][j], width=4, height=2,
                                               command=lambda i=i, j=j: self.on_square_click(i, j),
                                               bg=color)
                self.buttons[i][j].grid(row=i, column=j)

        self.selected_piece = None
        self.selected_row = None
        self.selected_col = None

    def on_square_click(self, row, col):
        piece = self.board[row][col]

        if self.selected_piece:
            # Eğer önceki bir taş seçilmişse, şu anki kareye taşı taşı
            self.move_piece(row, col)
        elif piece != ' ' and self.get_piece_color(piece) == self.current_player:
            # Eğer henüz taş seçilmemişse ve tıklanan taş oyun sırasındaki oyuncuya aitse, şu anki taşı seç
            self.select_piece(row, col)

    def select_piece(self, row, col):
        self.selected_piece = self.board[row][col]
        self.selected_row = row
        self.selected_col = col
        print(f"Seçilen taş: {self.selected_piece}")


    def is_valid_move(self, start_row, start_col, end_row, end_col):
        # Burada taşın hareket kurallarını kontrol etme mantığı eklenmelidir
        # Bu örnek sadece taşların hareketini kontrol etmez, aynı zamanda taş yeme durumunu da kontrol eder

        # Seçilen taşın türüne göre hareket kurallarını kontrol et
        if self.selected_piece.lower() == 'p':
            return self.valid_pawn_move(start_row, start_col, end_row, end_col)
        elif self.selected_piece.lower() == 'r':
            return self.valid_rook_move(start_row, start_col, end_row, end_col)
        elif self.selected_piece.lower() == 'n':
            return self.valid_knight_move(start_row, start_col, end_row, end_col)
        elif self.selected_piece.lower() == 'b':
            return self.valid_bishop_move(start_row, start_col, end_row, end_col)
        elif self.selected_piece.lower() == 'q':
            return self.valid_queen_move(start_row, start_col, end_row, end_col)
        elif self.selected_piece.lower() == 'k':
            return self.valid_king_move(start_row, start_col, end_row, end_col)

    def valid_pawn_move(self, start_row, start_col, end_row, end_col):
        direction = 1 if self.selected_piece.islower() else -1

        # İlk hamlede iki kare ileri hareket edebilme
        if start_row == 1 and end_row == start_row + 2 * direction and start_col == end_col and self.board[start_row + direction][end_col] == ' ' and self.board[start_row + 2 * direction][end_col] == ' ':
            return True

        # Diğer durumlarda bir kare ileri hareket etme
        if end_row == start_row + direction and start_col == end_col and self.board[end_row][end_col] == ' ':
            return True

        # Çapraz hareketle yeme durumu
        if end_col == start_col and self.board[end_row][end_col] != ' ':
            return False

        if abs(end_row - start_row) == 1 and abs(end_col - start_col) == 1:
            target_piece = self.board[end_row][end_col]
            if target_piece != ' ' and self.get_piece_color(target_piece) != self.current_player:
                return True

        # Geçerken alma durumu kontrolü
        if self.valid_pawn_en_passant(start_row, start_col, end_row, end_col):
            return True

        # İki kare ileri hareket edememe durumu
        if start_row == 6 and end_row == start_row + 2 * direction and start_col == end_col and self.board[start_row + direction][end_col] == ' ' and self.board[start_row + 2 * direction][end_col] == ' ':
            return True

        return False

    def valid_pawn_en_passant(self, start_row, start_col, end_row, end_col):
        direction = 1 if self.selected_piece.islower() else -1

        # Geçerken alma durumu
        if abs(end_row - start_row) == 1 and abs(end_col - start_col) == 1:
            target_row = start_row + direction
            target_col = end_col
            target_piece = self.board[target_row][target_col]

            if target_piece == ' ' or self.get_piece_color(target_piece) == self.current_player:
                return False

            # Geçişken almanın gerçekleşip gerçekleşmediğini kontrol et
            if target_piece.lower() == 'p' and target_row == (3 if direction == 1 else 4) and target_row == self.en_passant_target_row and target_col == self.en_passant_target_col:
                print("Geçerken alındı!")
                return True

        return False





    def make_move(self, start_row, start_col, end_row, end_col):
        # Diğer hareket türlerini kontrol et...

        # Geçerken alma durumu
        if self.valid_pawn_en_passant(start_row, start_col, end_row, end_col):
            self.board[start_row][end_col] = ' '  # Alınan piyonu sil
            self.move_piece(start_row, start_col, end_row, end_col)  # Piyonu taşı
            self.board[start_row][start_col] = ' '  # Başlangıç pozisyonunu boşalt
            self.switch_player()  # Oyuncu değiştir
            return True

        # Diğer durumları kontrol et...

        return False




    def get_opponent_color(self, player_color):
        return 'white' if player_color == 'black' else 'black'


    def valid_rook_move(self, start_row, start_col, end_row, end_col):
        # Sadece yatay veya dikey hareket
        if start_row != end_row and start_col != end_col:
            return False

        # Yatay hareket
        if start_row == end_row:
            direction_col = 1 if start_col < end_col else -1
            for col in range(start_col + direction_col, end_col, direction_col):
                if self.board[start_row][col] != ' ':
                    # Hedef konumda sadece rakip taşı varsa yiyebilir
                    if col == end_col and self.board[end_row][end_col] != ' ' and self.get_piece_color(self.board[end_row][end_col]) != self.current_player:
                        return True
                    return False

            # Hedef konumda rakip taşı varsa yiyebilir
            if self.board[end_row][end_col] != ' ' and self.get_piece_color(self.board[end_row][end_col]) != self.current_player:
                return True

        # Dikey hareket
        elif start_col == end_col:
            direction_row = 1 if start_row < end_row else -1
            for row in range(start_row + direction_row, end_row, direction_row):
                if self.board[row][start_col] != ' ':
                    # Hedef konumda sadece rakip taşı varsa yiyebilir
                    if row == end_row and self.board[end_row][end_col] != ' ' and self.get_piece_color(self.board[end_row][end_col]) != self.current_player:
                        return True
                    return False

            # Hedef konumda rakip taşı varsa yiyebilir
            if self.board[end_row][end_col] != ' ' and self.get_piece_color(self.board[end_row][end_col]) != self.current_player:
                return True

        # Dikine hareket
        elif start_row != end_row and start_col != end_col:
            direction_row = 1 if start_row < end_row else -1
            direction_col = 1 if start_col < end_col else -1
            row, col = start_row + direction_row, start_col + direction_col
            while row != end_row and col != end_col:
                if self.board[row][col] != ' ':
                    # Hedef konumda sadece rakip taşı varsa yiyebilir
                    if row == end_row and col == end_col and self.board[end_row][end_col] != ' ' and self.get_piece_color(self.board[end_row][end_col]) != self.current_player:
                        return True
                    return False
                row += direction_row
                col += direction_col

            # Hedef konumda rakip taşı varsa yiyebilir
            if self.board[end_row][end_col] != ' ' and self.get_piece_color(self.board[end_row][end_col]) != self.current_player:
                return True

        # Hedef konum boşsa hareket edebilir
        return self.board[end_row][end_col] == ' '


    def valid_knight_move(self, start_row, start_col, end_row, end_col):
        # Şahin L şeklinde hareketi
        if (abs(start_row - end_row) == 2 and abs(start_col - end_col) == 1) or \
        (abs(start_row - end_row) == 1 and abs(start_col - end_col) == 2):
            # Hedef konumda sadece rakip taşı varsa yiyebilir
            return self.board[end_row][end_col] == ' ' or self.get_piece_color(self.board[end_row][end_col]) != self.current_player
        return False


    def valid_queen_move(self, start_row, start_col, end_row, end_col):
        # Kraliçe, kale ve fil hareketini birleştirir
        return (self.valid_rook_move(start_row, start_col, end_row, end_col) or self.valid_bishop_move(start_row, start_col, end_row, end_col)) and self.is_path_clear(start_row, start_col, end_row, end_col)


    def valid_bishop_move(self, start_row, start_col, end_row, end_col):
        # Sadece çapraz hareket
        if abs(start_row - end_row) == abs(start_col - end_col) and self.is_path_clear(start_row, start_col, end_row, end_col):
            # Hedef konumda sadece rakip taşı varsa yiyebilir
            return self.board[end_row][end_col] == ' ' or self.get_piece_color(self.board[end_row][end_col]) != self.current_player
        return False


    def is_path_clear(self, start_row, start_col, end_row, end_col):
        # Yatay hareket
        if start_row == end_row:
            direction = 1 if start_col < end_col else -1
            for col in range(start_col + direction, end_col, direction):
                if self.board[start_row][col] != ' ':
                    return False

        # Dikey hareket
        elif start_col == end_col:
            direction = 1 if start_row < end_row else -1
            for row in range(start_row + direction, end_row, direction):
                if self.board[row][start_col] != ' ':
                    return False

        # Çapraz hareket
        elif abs(start_row - end_row) == abs(start_col - end_col):
            row_direction = 1 if start_row < end_row else -1
            col_direction = 1 if start_col < end_col else -1
            row, col = start_row + row_direction, start_col + col_direction
            while row != end_row and col != end_col:
                if self.board[row][col] != ' ':
                    return False
                row += row_direction
                col += col_direction

        return True


    def valid_king_move(self, start_row, start_col, end_row, end_col):
        # Şahın bir kare her yöne hareketi
        if abs(start_row - end_row) <= 1 and abs(start_col - end_col) <= 1 and self.is_path_clear(start_row, start_col, end_row, end_col):
            # Hedef konumda sadece rakip taşı varsa yiyebilir
            if self.board[end_row][end_col] == ' ' or self.get_piece_color(self.board[end_row][end_col]) != self.current_player:
                return True

        # Kısa rok durumu
        if start_row == 7 and start_col == 4 and end_row == 7 and end_col == 6 and \
                self.board[7][5] == ' ' and self.board[7][6] == ' ' and self.board[7][7] == 'R' and \
                self.board[7][4] == 'K' and not self.has_king_moved('white') and not self.has_rook_moved('white', 'short'):
            print("Kısa rok geçerli")
            return True

        elif start_row == 0 and start_col == 4 and end_row == 0 and end_col == 6 and \
                self.board[0][5] == ' ' and self.board[0][6] == ' ' and self.board[0][7] == 'r' and \
                self.board[0][4] == 'k' and not self.has_king_moved('black') and not self.has_rook_moved('black', 'short'):
            print("Kısa rok geçerli")
            return True

        # Uzun rok durumu
        if start_row == 7 and start_col == 4 and end_row == 7 and end_col == 2 and \
                self.board[7][1] == ' ' and self.board[7][2] == ' ' and self.board[7][3] == ' ' and self.board[7][0] == 'R' and \
                self.board[7][4] == 'K' and not self.has_king_moved('white') and not self.has_rook_moved('white', 'long'):
            print("Uzun rok geçerli")
            return True

        elif start_row == 0 and start_col == 4 and end_row == 0 and end_col == 2 and \
                self.board[0][1] == ' ' and self.board[0][2] == ' ' and self.board[0][3] == ' ' and self.board[0][0] == 'r' and \
                self.board[0][4] == 'k' and not self.has_king_moved('black') and not self.has_rook_moved('black', 'long'):
            print("Uzun rok geçerli")
            return True

        return False

    def has_king_moved(self, color):
        if color == 'white':
            return self.white_king_moved
        elif color == 'black':
            return self.black_king_moved

    def has_rook_moved(self, color, rook_type):
        if color == 'white':
            return self.white_rook_moved[rook_type]
        elif color == 'black':
            return self.black_rook_moved[rook_type]

    def move_piece(self, row, col):
        if self.is_valid_move(self.selected_row, self.selected_col, row, col):
            # Geçerli bir hamle yapıldıysa taşı hareket ettir
            self.board[row][col] = self.selected_piece
            self.board[self.selected_row][self.selected_col] = ' '

            # Rok durumunu kontrol et
            if self.selected_piece.lower() == 'k' and abs(self.selected_col - col) == 2:
                # Kısa rok
                if col == 6:
                    self.board[row][5] = self.board[row][7]
                    self.board[row][7] = ' '
                # Uzun rok
                elif col == 2:
                    self.board[row][3] = self.board[row][0]
                    self.board[row][0] = ' '

            print(f"{self.selected_piece} taşı {chr(ord('a')+self.selected_col)}{8-self.selected_row} -> {chr(ord('a')+col)}{8-row}")
            
            # Sıradaki oyuncuyu değiştir
            self.switch_player()

            # Kralın veya kalelerin hareket ettiğini kaydet
            if self.selected_piece.lower() == 'k':
                if self.get_piece_color(self.selected_piece) == 'white':
                    self.white_king_moved = True
                else:
                    self.black_king_moved = True
            elif self.selected_piece.lower() == 'r':
                if self.get_piece_color(self.selected_piece) == 'white':
                    if self.selected_col == 0:
                        self.white_rook_moved['long'] = True
                    elif self.selected_col == 7:
                        self.white_rook_moved['short'] = True
                else:
                    if self.selected_col == 0:
                        self.black_rook_moved['long'] = True
                    elif self.selected_col == 7:
                        self.black_rook_moved['short'] = True

        else:
            print("Geçersiz hamle!")

        self.update_board()
        self.clear_selection()


    def switch_player(self):
        # Sıradaki oyuncuyu değiştir
        self.current_player = 'white' if self.current_player == 'black' else 'black'

    def get_piece_color(self, piece):
        # Taşın rengini belirle
        return 'white' if piece.isupper() else 'black'

    def clear_selection(self):
        self.selected_piece = None
        self.selected_row = None
        self.selected_col = None

    def update_board(self):
        for i in range(8):
            for j in range(8):
                self.buttons[i][j].configure(text=self.board[i][j])

if __name__ == "__main__":
    root = tk.Tk()
    chess_game_gui = ChessGameGUI(root)
    root.mainloop()
