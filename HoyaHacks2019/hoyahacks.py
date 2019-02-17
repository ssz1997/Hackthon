import sys
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget, QApplication, QLineEdit, QLabel, QVBoxLayout, QComboBox, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot
from html.parser import HTMLParser
import re
import urllib
from google.cloud import translate
import os
import time

class MyHTMLParser(HTMLParser):
    def __init__(self, known_words):
        HTMLParser.__init__(self)
        self.recording = 0
        self.data = []
        self.word_dict = dict()
        self.known_words = ['abcdefghijklmnopqrstuvwxyz']
        self.roman_pattern = '^M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$'

    def handle_starttag(self, tag, attrs):
        if attrs == [] and ( tag == 'title' or tag == 'p' ):
            self.recording = 1

    def handle_endtag(self, tag):
        if tag ==  'title' or tag == 'p':
            self.recording = 0

    def handle_data(self, data):
        data = re.findall(r"[\w']+", data)

        if self.recording:
            for word in data:
                word = word.strip().lower()
                if re.match(self.roman_pattern, word.upper()) != None or word.isdigit() or word == '':
                    continue
                if word not in self.known_words:
                    self.word_dict[word] = 1


class Flashcard(QWidget):
    def __init__(self):
        super().__init__()

        self.x = 0
        self.d = {'None':'','Afrikaans':'af','Albanian':'sq','Amharic':'am','Arabic':'ar','Armenian':'hy','Azerbaijani':'az','Basque':'eu','Belarusian':'be','Bengali':'bn','Bosnian':'bs','Bulgarian':'bg','Catalan':'ca','Cebuano':'ceb','Chinese (Simplified)':'zh-CN','Chinese (Traditional)':'zh-TW','Corsican':'co','Croatian':'hr','Czech':'cs','Danish':'da','Dutch':'nl','English':'en','Esperanto':'eo','Estonian':'et','Finnish':'fi','French':'fr','Frisian':'fy','Galician':'gl','Georgian':'ka','German':'de','Greek':'el','Gujarati':'gu','Haitian Creole':'ht','Hausa':'ha','Hawaiian':'haw','Hebrew':'he','Hindi':'hi','Hmong':'hmn','Hungarian':'hu','Icelandic':'is','Igbo':'ig','Indonesian':'id','Irish':'ga','Italian':'it','Japanese':'ja','Javanese':'jw','Kannada':'kn','Kazakh':'kk','Khmer':'km','Korean':'ko','Kurdish':'ku','Kyrgyz':'ky','Lao':'lo','Latin':'la','Latvian':'lv','Lithuanian':'lt','Luxembourgish':'lb','Macedonian':'mk','Malagasy':'mg','Malay':'ms','Malayalam':'ml','Maltese':'mt','Maori':'mi','Marathi':'mr','Mongolian':'mn','Myanmar (Burmese)':'my','Nepali':'ne','Norwegian':'no','Nyanja (Chichewa)':'ny','Pashto':'ps','Persian':'fa','Polish':'pl','Portuguese (Portugal, Brazil)':'pt','Punjabi':'pa','Romanian':'ro','Russian':'ru','Samoan':'sm','Scots Gaelic':'gd','Serbian':'sr','Sesotho':'st','Shona':'sn','Sindhi':'sd','Sinhala (Sinhalese)':'si','Slovak':'sk','Slovenian':'sl','Somali':'so','Spanish':'es','Sundanese':'su','Swahili':'sw','Swedish':'sv','Tagalog (Filipino)':'tl','Tajik':'tg','Tamil':'ta','Telugu':'te','Thai':'th','Turkish':'tr','Ukrainian':'uk','Urdu':'ur','Uzbek':'uz','Vietnamese':'vi','Welsh':'cy','Xhosa':'xh','Yiddish':'yi','Yoruba':'yo','Zulu':'zu'}

        self.initUI()
        layout = QVBoxLayout()
        self.show()
        self.updatesEnabled()

    def initUI(self):
        self.label0 = QLabel(self)
        self.label0.setText("By Yingxu Mu and Shouzhuo Sun from WM")
        self.label0.move(5, 5)
        self.label0.setStyleSheet("font: 15pt")

        self.setGeometry(300, 300, 550, 700)
        self.setWindowTitle('Flashcards Maker')
        self.textbox = QLineEdit(self)
        self.textbox.move(90, 60)
        self.textbox.resize(400,40)
        self.label1 = QLabel(self)
        self.label1.setText("url:")
        self.label1.move(30, 60)
        self.label1.setStyleSheet("font: 25pt")

        self.label2 = QLabel(self)
        self.label2.setText("Source Language:")
        self.label2.move(30, 150)
        self.label2.setStyleSheet("font: 17pt")
        self.dropbox1 = QComboBox(self)
        self.dropbox1.move(180, 150)

        self.label3 = QLabel(self)
        self.label3.setText("Target Language 1:")
        self.label3.move(30, 240)
        self.label3.setStyleSheet("font: 17pt")
        self.dropbox2 = QComboBox(self)
        self.dropbox2.move(190, 240)

        self.label4 = QLabel(self)
        self.label4.setText("Target Language 2:")
        self.label4.move(30, 330)
        self.label4.setStyleSheet("font: 17pt")
        self.dropbox3 = QComboBox(self)
        self.dropbox3.move(190, 330)

        self.label5 = QLabel(self)
        self.label5.setText("Target Language 3:")
        self.label5.move(30, 420)
        self.label5.setStyleSheet("font: 17pt")
        self.dropbox4 = QComboBox(self)
        self.dropbox4.move(190, 420)

        for key in self.d:
            self.dropbox1.addItem(key)
            self.dropbox2.addItem(key)
            self.dropbox3.addItem(key)
            self.dropbox4.addItem(key)

        self.label6 = QLabel(self)
        self.label6.setText("Output Format:")
        self.label6.move(30, 500)
        self.label6.setStyleSheet("font: 17pt")
        self.dropbox5 = QComboBox(self)
        self.dropbox5.addItem("Plain Text (.txt)")
        self.dropbox5.addItem("Comma-separated Values (.csv)")
        self.dropbox5.move(150, 500)

        self.label7 = QLabel(self)
        self.label7.setText("Default output Directory: same as this software")
        self.label7.move(30, 585)
        self.label7.setStyleSheet("font: 15pt")

        self.button = QPushButton('Generate!', self)
        self.button.move(180, 640)
        self.button.resize(180, 50)
        self.button.setStyleSheet("font: 15pt")
        self.button.clicked.connect(self.on_click)

    @pyqtSlot()
    def on_click(self):
        url = str(self.textbox.text())

        source = self.d[str(self.dropbox1.currentText())]
        target1 = self.d[str(self.dropbox2.currentText())]
        target2 = self.d[str(self.dropbox3.currentText())]
        target3 = self.d[str(self.dropbox4.currentText())]

        translate_client = translate.Client()

        try:
            f = urllib.request.urlopen(url)
            s = f.read()
            s = str(s,'utf-8')
            parser = MyHTMLParser(None)
            parser.feed(s)

        except:
            QMessageBox.question(self, "Error", "Please enter a valid url", QMessageBox.Ok, QMessageBox.Ok)
            return
        self.textbox.setText('')
        dictionary = parser.word_dict

        translated_dict = dict()



        if source == '':
            QMessageBox.question(self, "Error", "Please select source language", QMessageBox.Ok, QMessageBox.Ok)
        elif target1 == '' and target2 == '' and target3 == '':
            QMessageBox.question(self, "Error", "Please select one target language", QMessageBox.Ok, QMessageBox.Ok)
        elif target1 != '' and target2 == '' and target3 == '':
            for w in dictionary:
                translated_dict[w] = [translate_client.translate(w, target_language = target1,source_language = source)['translatedText']]
        elif target1 != '' and target2 != '' and target3 == '':
            for w in dictionary:
                translated_dict[w] = [translate_client.translate(w, target_language = target1,source_language = source)['translatedText'],translate_client.translate(w, target_language = target2,source_language = source)['translatedText']]
        elif target1 != '' and target2 != '' and target3 != '':
            for w in dictionary:
                translated_dict[w] = [translate_client.translate(w, target_language = target1,source_language = source)['translatedText'],translate_client.translate(w, target_language = target2,source_language = source)['translatedText'],translate_client.translate(w, target_language = target3,source_language = source)['translatedText']]
        else:
            QMessageBox.question(self, "Error", "Please select target languages in order", QMessageBox.Ok, QMessageBox.Ok)


        if str(self.dropbox5.currentText()) == "Plain Text (.txt)":
            f = open(str(int(time.time())) + ".txt", "w+")
            for w in sorted(dictionary, key=dictionary.get, reverse=True):
                f.write(w + "\t" + ','.join(translated_dict[w]) + "\n")
            f.close()
        else:
            f = open(str(int(time.time())) + ".csv", "w+")
            for w in sorted(dictionary, key=dictionary.get, reverse=True):
                f.write(w + "\t" + ','.join(translated_dict[w]) + "\n")
            f.close()



if __name__ == '__main__':
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/ssz/Documents/ssz.json"

    app = QApplication(sys.argv)
    ex = Flashcard()
    sys.exit(app.exec_())
