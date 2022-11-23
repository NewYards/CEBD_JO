
import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic

# Classe permettant d'afficher la fenêtre de visualisation des données
class AppTablesDataV1(QDialog):

    # Constructeur
    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/v1_tablesData.ui", self)
        self.data = data

        # On met à jour l'affichage avec les données actuellement présentes dans la base
        self.refreshAllTablesV1()

    ####################################################################################################################
    # Méthodes permettant de rafraichir les différentes tables
    ####################################################################################################################

    # Fonction de mise à jour de l'affichage d'une seule table
    def refreshTable(self, label, table, query):
        display.refreshLabel(label, "")
        try:
            cursor = self.data.cursor()
            result = cursor.execute(query)
        except Exception as e:
            table.setRowCount(0)
            display.refreshLabel(label, "Impossible d'afficher les données de la table : " + repr(e))
        else:
            display.refreshGenericData(table, result)


    # Fonction permettant de mettre à jour toutes les tables
    @pyqtSlot()
    def refreshAllTablesV1(self):
        # DONETODO 1.3 : modifier pour afficher les nouveaux éléments (il faut aussi changer le fichier .ui correspondant)
        self.refreshTable(self.ui.label_epreuves, self.ui.tableEpreuves,
                          "SELECT numEp, nomEp, formeEp, nomDi, categorieEp, nbSportifsEp, dateEp, res_or, res_argent, res_bronze FROM LesEpreuves")
        self.refreshTable(self.ui.label_sportifs, self.ui.tableSportifs,
                          "SELECT numSp, nomSp, prenomSp, pays, categorieSp, dateNaisSp FROM LesSportifs")
        self.refreshTable(self.ui.label_equipes, self.ui.tableEquipes,
                          "SELECT numSp, numEq FROM LesEquipes")
        self.refreshTable(self.ui.label_participants, self.ui.tableParticipants,
                          "SELECT numIns, numEp FROM LesParticipants")
        # DONETODO 1.4b : ajouter l'affichage des éléments de la vue LesAgesSportifs après l'avoir créée
        self.refreshTable(self.ui.label_lesAgesSportifs, self.ui.tableLesAgesSportifs,
                          "SELECT numSp, age FROM LesAgesSportifs")
        # DONETODO 1.5b : ajouter l'affichage des éléments de la vue LesNbsEquipiers après l'avoir créée
        self.refreshTable(self.ui.label_lesNbsEquipiers, self.ui.tableLesNbsEquipiers,
                          "SELECT nbEquipiers, numEq FROM LesNbsEquipiers")
