
import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic

# Classe permettant d'afficher la fenêtre de visualisation des données
class AppFctDemande2(QDialog):

    # Constructeur
    def __init__(self, data: sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/fct_demande_2.ui", self)
        self.data = data
        self.refreshResult()

    # Fonction de mise à jour de l'affichage
    @pyqtSlot()
    def refreshResult(self):

        display.refreshLabel(self.ui.label_fct_fournie_1, "")
        try:
            cursor = self.data.cursor()
            result = cursor.execute("WITH ind_or AS (SELECT pays,COUNT(res_or) nb_or FROM LesSportifs JOIN LesEpreuves ON(res_or = numSp) GROUP BY pays),"
                                    "ind_argent AS (SELECT pays,COUNT(res_argent) argent FROM LesSportifs JOIN LesEpreuves ON(res_argent = numSp) GROUP BY pays),"
                                    "ind_bronze AS (SELECT pays,COUNT(res_bronze) bronze FROM LesSportifs JOIN LesEpreuves ON(res_bronze = numSp) GROUP BY pays),"
                                    "ind_or_argent AS (SELECT pays, nb_or,argent FROM ind_or LEFT JOIN ind_argent USING(pays) UNION ALL SELECT pays, nb_or,argent FROM ind_argent LEFT JOIN ind_or USING(pays)),"
                                    "ind AS (SELECT distinct pays, nb_or, argent, bronze FROM ind_or_argent LEFT JOIN ind_bronze USING(PAYS) UNION ALL SELECT pays, nb_or, argent, bronze FROM ind_bronze LEFT JOIN ind_or_argent USING(PAYS)),"
                                    "paysPerEquipe AS (SELECT distinct numEq, pays FROM LesEquipes JOIN LesSportifs USING(numSp)),"
                                    "eq_or AS (SELECT pays, COUNT(res_or) nb_or FROM paysPerEquipe JOIN LesEpreuves ON(res_or = numEq)),"
                                    "eq_argent AS (SELECT pays, COUNT(res_argent) argent FROM paysPerEquipe JOIN LesEpreuves ON(res_argent = numEq)),"
                                    "eq_bronze AS (SELECT pays, COUNT(res_bronze) bronze FROM paysPerEquipe JOIN LesEpreuves ON(res_bronze = numEq)),"
                                    "eq_or_argent AS (SELECT pays, nb_or, argent FROM eq_or LEFT JOIN eq_argent USING(pays) UNION ALL SELECT pays, nb_or, argent FROM eq_argent LEFT JOIN eq_or USING(pays)),"
                                    "eq AS (SELECT pays, nb_or, argent,bronze FROM eq_or_argent LEFT JOIN eq_bronze USING(pays) UNION ALL SELECT pays, nb_or, argent,bronze FROM eq_bronze LEFT JOIN eq_or_argent USING(pays)),"
                                    "res AS (SELECT pays, COALESCE(ind.nb_or, 0)+eq.nb_or nb_or,COALESCE(ind.argent, 0)+eq.argent argent,COALESCE(ind.bronze, 0)+eq.bronze bronze FROM ind LEFT JOIN eq USING(pays) UNION ALL SELECT pays, ind.nb_or+eq.nb_or,ind.argent+eq.argent,ind.bronze+eq.bronze FROM eq LEFT JOIN ind USING(pays))"
                                    "SELECT pays, nb_or,argent,bronze FROM res")
        except Exception as e:
            self.ui.table_fct_fournie_1.setRowCount(0)
            display.refreshLabel(self.ui.label_fct_fournie_1, "Impossible d'afficher les résultats : " + repr(e))
        else:
            display.refreshGenericData(self.ui.table_fct_fournie_1, result)
