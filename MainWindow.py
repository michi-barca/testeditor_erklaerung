from PyQt6.QtCore import pyqtSlot, QFile, QIODevice, QTextStream, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QMainWindow, QMenu, QMenuBar, QFileDialog, QFontDialog, QStatusBar, QMessageBox
from PyQt6.uic.Compiler.qtproxies import QtCore

from CentralWidget import CentralWidget  # Importiert das CentralWidget (wo der Texteditor ist)


class MainWindow(QMainWindow):
    # Definiert benutzerdefinierte Signale, um Text und Schriftart zwischen den Objekten zu übertragen
    write_text = pyqtSignal(str)
    write_font = pyqtSignal(QFont)

    def __init__(self, parent=None):
        # Konstruktor der MainWindow-Klasse, ruft den Eltern-Konstruktor auf
        super(MainWindow, self).__init__(parent)

        # Initialisiert ein QFont-Objekt, das für die Schriftart verwendet wird
        self.__font = QFont()

        # Definiert Filter für den Dateidialog (zuerst Textdateien, dann alle Dateien)
        self.__initial_filter = "Default files (*.txt)"
        self.__filter = self.__initial_filter + ";;All files (*)"

        # Initialisiert das Verzeichnis für Dateioperationen
        self.__directory = ""

        # Erstellt das zentrale Widget, das den Texteditor enthält
        self.__central_widget = CentralWidget(self)
        # Verbindet das Signal zum Setzen des Textes im CentralWidget
        self.write_text.connect(self.__central_widget.set_text)
        # Verbindet das Signal zum Setzen der Schriftart im CentralWidget
        self.write_font.connect(self.__central_widget.set_font)

        # Setzt den Fenstertitel
        self.setWindowTitle("Mein Texteditor")

        # Erstellt eine Statusleiste für das Fenster
        self.setStatusBar(QStatusBar(self))

        # Erstellt die Menüleiste
        menu_bar = QMenuBar(self)

        # Erstelle das "Files"-Menü und fügt Aktionen hinzu
        files = QMenu("Files", menu_bar)

        # Aktion "Open" zum Öffnen einer Datei
        action_file_open = files.addAction("Open ...")
        action_file_open.triggered.connect(self.file_open)  # Ruft die Methode zum Öffnen einer Datei auf

        # Aktion "Save" zum Speichern einer Datei
        action_file_save = files.addAction("Save ...")
        action_file_save.triggered.connect(self.file_save)  # Ruft die Methode zum Speichern einer Datei auf

        # Platzhalteraktionen (noch nicht implementiert)
        action_file_copy = files.addAction("Copy ...")
        action_file_copy.triggered.connect(self.file_copy)

        action_file_move = files.addAction("Move ...")
        action_file_move.triggered.connect(self.file_move)

        # Fügt das "Files"-Menü der Menüleiste hinzu
        menu_bar.addMenu(files)

        # Erstelle das "Font"-Menü und fügt Aktionen hinzu
        font = QMenu("Font", menu_bar)

        # Aktion "Font" zum Öffnen des Schriftarten-Dialogs
        action_font = font.addAction("Font")
        action_font.triggered.connect(self.font)  # Ruft die Methode zum Auswählen einer Schriftart auf
        edit = QMenu("Edit", menu_bar)

        # Aktion "Undo" zum Rückgängigmachen der letzten Aktion
        action_undo = edit.addAction("Undo")
        action_undo.triggered.connect(self.__central_widget.undo)  # Verbindung zur Undo-Funktion im CentralWidget

        # Fügt das "Edit"-Menü der Menüleiste hinzu
        menu_bar.addMenu(edit)

        # Fügt das "Font"-Menü der Menüleiste hinzu
        menu_bar.addMenu(font)

        # Setzt die Menüleiste des Fensters
        self.setMenuBar(menu_bar)

        # Setzt das zentrale Widget auf das CentralWidget
        self.setCentralWidget(self.__central_widget)

    # Öffnet eine Datei
    @pyqtSlot()
    def file_open(self):
        # Öffnet den Dateidialog und erlaubt dem Benutzer, eine Datei auszuwählen
        (path, self.__initial_filter) = QFileDialog.getOpenFileName(self, "Open File", self.__directory, self.__filter, self.__initial_filter)

        # Wenn ein Pfad ausgewählt wurde
        if path:
            # Speichert das Verzeichnis der ausgewählten Datei
            self.__directory = path[:path.rfind("/")]
            # Zeigt eine Statusnachricht an
            self.statusBar().showMessage("File opened: " + path[path.rfind("/") + 1:])

            # Öffnet die Datei
            file = QFile(path)

            # Wenn die Datei nicht geöffnet werden konnte, zeigt eine Fehlermeldung an
            if not file.open(QIODevice.OpenModeFlag.ReadOnly):
                QMessageBox.information(self, "Unable to open file", file.errorString())
                return

            # Liest den gesamten Text aus der Datei
            stream = QTextStream(file)
            text_in_file = stream.readAll()

            # Sendet den Text an das CentralWidget
            self.write_text.emit(text_in_file)

            # Schließt die Datei
            file.close()

    # Speichert eine Datei
    @pyqtSlot()
    def file_save(self):
        # Öffnet den Dateispeicher-Dialog
        (path, self.__initial_filter) = QFileDialog.getSaveFileName(self, "Save File", self.__directory, self.__filter, self.__initial_filter)

        # Wenn ein Pfad ausgewählt wurde
        if path:
            # Speichert das Verzeichnis der ausgewählten Datei
            self.__directory = path[:path.rfind("/")]
            # Zeigt eine Statusnachricht an
            self.statusBar().showMessage("File saved: " + path[path.rfind("/") + 1:])

            # Öffnet die Datei im Schreibmodus
            file = QFile(path)

            # Wenn die Datei nicht geöffnet werden konnte, zeigt eine Fehlermeldung an
            if not file.open(QIODevice.OpenModeFlag.WriteOnly):
                QMessageBox.information(self, "Unable to save file", file.errorString())
                return

            # Schreibt den Text aus dem CentralWidget in die Datei
            stream = QTextStream(file)
            stream << self.__central_widget.get_text()

            # Schließt die Datei
            stream.flush()
            file.close()

    # Platzhalter für die Copy-Funktion (noch nicht implementiert)
    @pyqtSlot()
    def file_copy(self):
        pass

    # Platzhalter für die Move-Funktion (noch nicht implementiert)
    @pyqtSlot()
    def file_move(self):
        pass

    # Öffnet den Schriftarten-Dialog
    @pyqtSlot()
    def font(self):
        # Öffnet den Font-Dialog und erhält die ausgewählte Schriftart
        [changed_font, changed] = QFontDialog.getFont(self.__font, self, "Select your font")

        # Wenn eine Schriftart ausgewählt wurde
        if changed:
            # Setzt die neue Schriftart
            self.__font = changed_font
            # Sendet die neue Schriftart an das CentralWidget
            self.write_font.emit(self.__font)
