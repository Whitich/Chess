import chess
import numpy as np
from tensorflow import keras
from tensorflow.keras import layers

# Satranç tahtasını temsil etmek için bir fonksiyon
def board_to_input(board):
    # Satranç tahtasını numpy dizisine dönüştür
    board_array = np.array(str(board).split()).reshape(8, 8)

    # Dizi elemanlarını bir sayı dizisine dönüştür
    mapping = {'r': -1, 'n': -2, 'b': -3, 'q': -4, 'k': -5, 'p': -6,
               'R': 1, 'N': 2, 'B': 3, 'Q': 4, 'K': 5, 'P': 6, '.': 0}
    input_array = np.vectorize(mapping.get)(board_array)

    # Giriş dizisini yeniden şekillendir ve boyut ekleyerek döndür
    return input_array.reshape(1, 8, 8, 1).astype(np.float32)  # 4 boyutlu hale getirildi ve veri tipi belirtildi



# Modeli oluştur
model = keras.Sequential([
    layers.Conv2D(64, (3, 3), activation='relu', input_shape=(8, 8, 1)),
    layers.Flatten(),
    layers.Dense(512, activation='relu'),
    layers.Dense(256, activation='relu'),
    layers.Dense(128, activation='relu'),
    layers.Dense(1, activation='sigmoid')  # "sigmoid" kullanıldı
])

# Modeli derle
model.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])

# Siyahlar için ayrı model oluşturun
model_black = keras.Sequential([
    layers.Conv2D(64, (3, 3), activation='relu', input_shape=(8, 8, 1)),
    layers.Flatten(),
    layers.Dense(512, activation='relu'),
    layers.Dense(256, activation='relu'),
    layers.Dense(128, activation='relu'),
    layers.Dense(1, activation='sigmoid')
])

# Modeli derleyin
model_black.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])


# Modeli kaydetme ve yükleme fonksiyonları
def save_model(model, filename):
    model.save(filename)

def load_model(filename):
    return keras.models.load_model(filename)

def self_play_and_train(model, num_games=100, epsilon=0.0):
    X_train, y_train = [], []
    X_train_black, y_train_black = [], []

    for game_num in range(num_games):
        board = chess.Board()
        states, results = [], []

        while not board.is_game_over():
            # Beyaz tarafın hamlesi (model tarafından)
            input_array_white = board_to_input(board)
            states.append(input_array_white)

            input_array_white_reshaped = input_array_white.reshape(1, 8, 8, 1)
            prediction_white = model.predict(input_array_white_reshaped)
            legal_moves_white = [str(move) for move in board.legal_moves]

            # Modelin tahmin ettiği değerleri kullanma
            values_white = prediction_white[0]
            probs_white = np.exp(values_white) / np.sum(np.exp(values_white))

            # Epsilon-Greedy stratejisi
            if np.random.rand() < epsilon:
                # en iyi tahmin edilen hareketi seç
                selected_move_white = legal_moves_white[np.argmax(values_white)]
            else:
                selected_move_white = np.random.choice(legal_moves_white)

            board.push(chess.Move.from_uci(selected_move_white))

            # Siyah tarafın hamlesi (model tarafından)
            input_array_black = board_to_input(board)
            states.append(input_array_black)

            input_array_black_reshaped = input_array_black.reshape(1, 8, 8, 1)
            prediction_black = model.predict(input_array_black_reshaped)
            legal_moves_black = [str(move) for move in board.legal_moves]

            # Modelin tahmin ettiği değerleri kullanma
            values_black = prediction_black[0]

            if not legal_moves_black:
                # Eğer legal_moves_black boşsa, rasgele bir hamle seç
                selected_move_black = np.random.choice(chess.Move.uci(chess.Move.null()))
            else:
                # Eğer legal_moves_black doluysa, Epsilon-Greedy stratejisi ile hamle seç
                if np.random.rand() < epsilon:
                    # en iyi tahmin edilen hareketi seç
                    selected_move_black = legal_moves_black[np.argmax(values_black)]
                else:
                    selected_move_black = np.random.choice(legal_moves_black)

            board.push(chess.Move.from_uci(selected_move_black))

        # Oyun sonucunu kaydetme
        if board.result() == "1-0":
            results.extend([1.0, 0.0])  # Beyaz kazandı, siyah kaybetti
        elif board.result() == "0-1":
            results.extend([0.0, 1.0])  # Beyaz kaybetti, siyah kazandı
        else:
            results.extend([0.5, 0.5])  # Berabere

        # Eğitim verilerini güncelleme
        X_train.extend(states)
        y_train.extend(results)

        #siyahlar için
        X_train_black.extend(states)
        y_train_black.extend(results)
        
        # Oyun sonucunu ekrana yazdırma
        print(f"Game {game_num + 1} Result: {board.result()}")

    # NumPy dizisine çevirme
    X_train, y_train = np.vstack(X_train), np.array(y_train)

    # Modeli eğitme
    history = model.fit(X_train, y_train, epochs=5, batch_size=32, validation_split=0.2)

    # NumPy dizisine çevirme
    X_train_black, y_train_black = np.vstack(X_train_black), np.array(y_train_black)

    # Modeli eğitme
    history_black = model_black.fit(X_train_black, y_train_black, epochs=5, batch_size=32, validation_split=0.2)

    return model



# Modeli kaydet
save_model(model, "chess_model.h5")

# Siyahlar için modeli eğitin
model_black = self_play_and_train(model_black, num_games=5, epsilon=0.1)

# Siyahlar için modeli kaydedin
save_model(model_black, "chess_model_black.h5")


# Modeli yükle
loaded_model = load_model("chess_model.h5")

# Kendi kendine oynayarak eğitim ve modeli güncelleme
loaded_model = self_play_and_train(loaded_model, num_games=5, epsilon=0.1)  # Değerleri düşürdüm sadece test için
