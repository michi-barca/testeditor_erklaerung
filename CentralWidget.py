from PyQt6.QtCore import pyqtSlot  # Import für pyqtSlot, um Funktionen als Reaktion auf Signale zu verbinden
from PyQt6.QtGui import QFont  # Import für QFont, um Schriftarten und -stile zu ändern
from PyQt6.QtWidgets import QWidget, QTextEdit, QVBoxLayout, QHBoxLayout, QPushButton  # Widgets für die GUI

class CentralWidget(QWidget):  # Unsere Hauptklasse, die von QWidget erbt
    def __init__(self, parent=None):  # Konstruktor der Klasse
        super(CentralWidget, self).__init__(parent)  # Konstruktor der Basisklasse aufrufen

        # --- Layout für die Buttons erstellen ---
        bar_layout = QHBoxLayout()  # Horizontal ausgerichtetes Layout für die Buttons

        # --- Buttons erstellen ---
        self.__pushbutton_bold = QPushButton('Bold')  # Button für Fettschrift
        self.__pushbutton_calibri = QPushButton('Calibri')  # Button für die Schriftart "Calibri"
        self.__pushbutton_underline = QPushButton('Underline')  # Button für Unterstreichen

        # --- Buttons mit Funktionen verbinden ---
        self.__pushbutton_bold.pressed.connect(self.__bold)  # Verbindet den Bold-Button mit der Funktion __bold
        self.__pushbutton_calibri.pressed.connect(self.__set_calibri)  # Verbindet den Calibri-Button mit der Funktion __set_calibri
        self.__pushbutton_underline.pressed.connect(self.__underline)  # Verbindet den Underline-Button mit der Funktion __underline

        # --- Buttons zum Layout hinzufügen ---
        bar_layout.addWidget(self.__pushbutton_bold)  # Bold-Button in das Layout einfügen
        bar_layout.addWidget(self.__pushbutton_calibri)  # Calibri-Button in das Layout einfügen
        bar_layout.addWidget(self.__pushbutton_underline)  # Underline-Button in das Layout einfügen

        # --- Textfeld erstellen ---
        self.__text_edit = QTextEdit()  # Ein Textfeld, in dem der Benutzer Text eingeben kann

        # --- Hauptlayout erstellen ---
        layout = QVBoxLayout()  # Vertikal ausgerichtetes Layout für das gesamte Widget
        layout.addLayout(bar_layout)  # Button-Leiste (bar_layout) hinzufügen
        layout.addWidget(self.__text_edit)  # Textfeld hinzufügen

        # --- Layout setzen ---
        self.setLayout(layout)  # Das Hauptlayout als Layout für das Widget festlegen

    # --- Funktion, um den Text im Textfeld zu setzen ---
    @pyqtSlot(str)  # Slot, der einen Textstring erwartet
    def set_text(self, text):
        self.__text_edit.setText(text)  # Den übergebenen Text in das Textfeld einfügen

    # --- Funktion, um den Text aus dem Textfeld zu holen ---
    def get_text(self):
        return self.__text_edit.toPlainText()  # Gibt den reinen Text (ohne Formatierung) zurück

    # --- Funktion, um die Schriftart des gesamten Textes zu setzen ---
    @pyqtSlot(QFont)  # Slot, der eine Schriftart erwartet
    def set_font(self, font):
        self.__text_edit.setFont(font)  # Setzt die Schriftart des Textfelds

    # --- Funktion für Fettschrift ---
    @pyqtSlot()
    def __bold(self):
        cursor = self.__text_edit.textCursor()  # Den aktuellen Textcursor holen
        format = cursor.charFormat()  # Format des markierten Texts holen
        font = self.__pushbutton_bold.font()  # Aktuelle Schriftart des Bold-Buttons holen

        if self.__pushbutton_bold.font().bold():  # Wenn der Button fett ist:
            format.setFontWeight(QFont.Weight.Normal)  # Normale Schriftart einstellen
            font.setBold(False)  # Button-Schriftart ebenfalls auf normal setzen
        else:  # Wenn der Button nicht fett ist:
            format.setFontWeight(QFont.Weight.Bold)  # Fettschrift einstellen
            font.setBold(True)  # Button-Schriftart auf fett setzen

        cursor.setCharFormat(format)  # Neues Format auf den Text anwenden
        self.__text_edit.setTextCursor(cursor)  # Den Cursor im Textfeld aktualisieren
        self.__pushbutton_bold.setFont(font)  # Die Schriftart des Bold-Buttons aktualisieren

    # --- Funktion, um die Schriftart auf "Calibri" zu setzen ---
    @pyqtSlot()
    def __set_calibri(self):
        cursor = self.__text_edit.textCursor()  # Den aktuellen Textcursor holen
        format = cursor.charFormat()  # Format des markierten Texts holen
        format.setFontFamily("Calibri")  # Die Schriftart auf "Calibri" setzen
        cursor.setCharFormat(format)  # Neues Format auf den Text anwenden
        self.__text_edit.setTextCursor(cursor)  # Den Cursor im Textfeld aktualisieren

    # --- Funktion für Unterstreichen ---
    @pyqtSlot()
    def __underline(self):
        cursor = self.__text_edit.textCursor()  # Den aktuellen Textcursor holen
        format = cursor.charFormat()  # Format des markierten Texts holen
        font = self.__pushbutton_underline.font()  # Aktuelle Schriftart des Underline-Buttons holen

        if self.__pushbutton_underline.font().underline():  # Wenn der Button unterstrichen ist:
            format.setFontUnderline(False)  # Unterstreichen deaktivieren
            font.setUnderline(False)  # Button-Schriftart ebenfalls aktualisieren
        else:  # Wenn der Button nicht unterstrichen ist:
            format.setFontUnderline(True)  # Unterstreichen aktivieren
            font.setUnderline(True)  # Button-Schriftart ebenfalls aktualisieren

        cursor.setCharFormat(format)  # Neues Format auf den Text anwenden
        self.__text_edit.setTextCursor(cursor)  # Den Cursor im Textfeld aktualisieren
        self.__pushbutton_underline.setFont(font)  # Die Schriftart des Underline-Buttons aktualisieren