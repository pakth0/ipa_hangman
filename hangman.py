import random
import sys
from nltk.corpus import cmudict, webtext
from arpa2ipa import arpa2ipa, _MAP_ARPA_IPA
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QGridLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from syllabifier import syllabifyARPA


def get_word():
    g2p = cmudict.dict()  # Initialize CMU dict
    wordlist = webtext.words()  # Webtext corpus for more everyday words
    # Get random word
    word_length = random.randint(5, 12)
    filtered = [word for word in list(wordlist) if (len(word) == word_length and (not "'" in word) and word[len(word) - 1] != "s")]
    
    word = ""
    phonemes = ""
    while phonemes == "":
        try:
            word = (random.sample(filtered, 1)[0]).lower()
            phonemes = g2p[word][0]
        except:
            pass

    ipa = [arpa2ipa(l) for l in phonemes]
    syllabified_list = syllabifyARPA(phonemes)
    syllabified = [s.split(" ") for s in syllabified_list]
    return word, ipa, syllabified


class HangmanGame(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IPA Hangman Game")
        self.setGeometry(100, 100, 600, 500)

        # Initialize globals
        self.word = ""
        self.ipa = []
        self.guessed_symbols = set()
        self.ipa_set = set()
        self.attempts = 6
        self.display_ipa = []

        # Set up UI
        self.initUI()
        self.new_game()

    def initUI(self):
        # Layouts
        main_layout = QVBoxLayout()
        top_layout = QVBoxLayout()
        button_layout = QGridLayout()

        # Set DejaVu Sans font
        font = QFont("DejaVu Sans", 14)

        # Labels
        self.word_label = QLabel("", self)
        self.word_label.setAlignment(Qt.AlignCenter)
        self.word_label.setFont(QFont("DejaVu Sans", 24))

        self.guessed_label = QLabel("Guessed IPA: ", self)
        self.guessed_label.setAlignment(Qt.AlignCenter)
        self.guessed_label.setFont(font)

        self.attempts_label = QLabel("Attempts left: 6", self)
        self.attempts_label.setAlignment(Qt.AlignCenter)
        self.attempts_label.setFont(font)

        self.result_label = QLabel("", self)
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setFont(QFont("DejaVu Sans", 16))

        top_layout.addWidget(self.word_label)
        top_layout.addWidget(self.guessed_label)
        top_layout.addWidget(self.attempts_label)
        top_layout.addWidget(self.result_label)

        # Add the top layout to the main layout
        main_layout.addLayout(top_layout)

        # Letter buttons (A-Z)
        self.letter_buttons = {}
        for i, letter in enumerate(list(_MAP_ARPA_IPA.values())):
            btn = QPushButton(letter, self)
            btn.setFixedSize(40, 40)
            btn.setFont(font)
            btn.clicked.connect(lambda checked, letter=letter: self.guess_symbol(letter))
            self.letter_buttons[letter] = btn
            button_layout.addWidget(btn, i // 8, i % 8)

        main_layout.addLayout(button_layout)

        # New Game button
        new_game_button = QPushButton("New Game", self)
        new_game_button.setFont(font)
        new_game_button.clicked.connect(self.new_game)
        main_layout.addWidget(new_game_button)

        # Set the main layout
        self.setLayout(main_layout)

    def update_display(self):
        # Update display text for word, guessed letters, attempts
        self.word_label.setText(" ".join(self.display_ipa))
        self.guessed_label.setText(f"Guessed IPA: {' '.join(self.guessed_symbols)}")
        self.attempts_label.setText(f"Attempts left: {self.attempts}")

        if self.attempts == 0:
            self.result_label.setText(f"Game Over! :( \nthe word was: {self.word}\n the ipa was {' '.join(self.ipa)}")
        elif "_" not in self.display_ipa:
            self.result_label.setText(f"Congrats! You've guessed the word: {self.word}\n the ipa was {' '.join(self.ipa)}")
        else:
            self.result_label.setText("")

    def guess_symbol(self, symbol):
        if symbol in self.guessed_symbols:
            return
        self.guessed_symbols.add(symbol)

        if symbol in self.ipa_set:
            display_index = 0
            for i, char in enumerate(self.ipa):
                if self.display_ipa[display_index] == '|' or self.display_ipa[display_index] == ',' or self.display_ipa[display_index] == "'":  display_index += 1;
                if char == symbol: 
                    self.display_ipa[display_index] = symbol
                display_index += 1
        else:
            self.attempts -= 1

        self.update_display()

    def new_game(self):
        self.word, self.ipa, self.syllabified = get_word()
        print(self.word)
        print(self.ipa)
        print(self.syllabified)

        for i, char in enumerate(self.ipa):
            if (char[len(char)-1].isdigit()): self.ipa[i] = char[:len(char)-1]

        self.ipa_set = set(self.ipa)
        self.guessed_symbols = set()
        self.display_ipa = ["_"] * len(self.ipa)
        self.stress_dict = dict()
        index = 0
        for i, syllable in enumerate(self.syllabified):
            stress = False;
            stressLevel = 0
            for j, phone in enumerate(syllable):
                index += 1
                if phone[len(phone)-1].isdigit(): 
                    stress = True
                    stressLevel = phone[len(phone)-1]
            if stress == True:
                self.stress_dict[i] = stressLevel
            # print(index)
            if i != len(self.syllabified)-1: self.display_ipa.insert(index, "|")
            index += 1
        print(self.stress_dict)

        index = 0
        for i, syllable in enumerate(self.syllabified): 
            if(self.stress_dict[i] == '1'): 
                self.display_ipa.insert(index, "'")
                index += 1
            if(self.stress_dict[i] == '2'): 
                self.display_ipa.insert(index, ",")
                index += 1
            index += len(syllable) + 1

        self.attempts = 6

        self.update_display()


def main():
    app = QApplication(sys.argv)
    game = HangmanGame()
    game.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
