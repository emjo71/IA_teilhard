from docx import Document
from nltk.tokenize import sent_tokenize
import string
import re

from sentence_transformers import SentenceTransformer, util
from deep_translator import GoogleTranslator

folder_path = "C:/Users/Louis/Documents/CTDC/Projet Geek/T4-"
book_name = "Milieu_divin"



def getPath(folder_path, book_name):
    return folder_path + book_name + "-Test.docx"

def getText(filepath):
    """return text as list of raw paragraphs to process"""
    doc = Document(filepath)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return fullText

def checkMilieuDivin(fullText, para_nb):
    return fullText[para_nb] == "LE MILIEU DIVIN." and fullText[para_nb+1] == "Essai de vie intérieure"

def checkCommentJeCrois():
    return fullText[para_nb] == "COMMENT JE CROIS" 

    
def chaptDetection(fullText, book_name):
    """return dictionary of chapters with chapt_nb as key"""
    fullText = [para for para in fullText if len(para)!=0] #enlève les lignes vides

    dict_chapters={} 
    chapt_start_index = []

    for para_nb in range(len(fullText)):
        if book_name == "Milieu_divin":
            if checkMilieuDivin(fullText, para_nb):
                chapt_start_index.append(para_nb)
        elif book_name == "Comment_je_crois":       
            if checkCommentJeCrois(fullText, para_nb):
                chapt_start_index.append(para_nb)
        else : 
            print("error")
                    
    #print(chapt_start_index) #print les indices de paragraphe de début de chaque chapitre
        
    for chapt_nb in range(len(chapt_start_index)):
        if chapt_nb < len(chapt_start_index)-1:
            dict_chapters[chapt_nb] = fullText[chapt_start_index[chapt_nb]:chapt_start_index[chapt_nb+1]-1]
        else:
            dict_chapters[chapt_nb] = fullText[chapt_start_index[chapt_nb]:]
    
    return dict_chapters
    
    
    #attribution à chaque phrase d'un chapitre, paragraphe, numéro de phrase

def createDict(dict_chapters):
    
    dict_sentences = {}
    dict_chapters_titles = {}

    for chapt_nb in dict_chapters.keys():
        chapter = dict_chapters[chapt_nb]
        partie = chapter[2]
        numéro_chapitre = chapter[3]
        titre_chapitre = chapter[4]

        titre_chapitre.translate(str.maketrans('', '', string.punctuation)) #remove punctuation
        pattern = r'[0-9]'
        titre_chapitre = re.sub(pattern, '', titre_chapitre).replace('[','').replace(']','') #remove number & brackets

        dict_chapters_titles[chapt_nb] = (partie, numéro_chapitre, titre_chapitre) #extract partie, numéro de chapitre, chapitre
        chapter = chapter[5:] 

        for para_nb in range(len(chapter)):
            para = chapter[para_nb]
            sentences = [sentence for sentence in sent_tokenize(para) if len(sentence.split())>1] #on conserve seulement les phrases dont le nombre de mots est superieur à 1

            for sent_nb in range(len(sentences)):
                dict_sentences[(chapt_nb, para_nb, sent_nb)] = sentences[sent_nb]
                
    return dict_sentences, dict_chapters_titles
    
    
#Test
filepath = getPath(folder_path, book_name)
fullText = getText(filepath)
dict_chapters = chaptDetection(fullText, book_name)

dict_sentences = createDict(dict_chapters)[0]
dict_chapters_titles = createDict(dict_chapters)[1]
