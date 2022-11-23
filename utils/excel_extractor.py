import sqlite3
from sqlite3 import IntegrityError

import pandas

def read_excel_file_V0(data:sqlite3.Connection, file):
    # Lecture de l'onglet du fichier excel LesSportifsEQ, en interprétant toutes les colonnes comme des strings
    # pour construire uniformement la requête
    df_sportifs = pandas.read_excel(file, sheet_name='LesSportifsEQ', dtype=str)
    df_sportifs = df_sportifs.where(pandas.notnull(df_sportifs), 'null')

    cursor = data.cursor()
    for ix, row in df_sportifs.iterrows():
        try:
            query = "insert into V0_LesSportifsEQ values ({},'{}','{}','{}','{}','{}',{})".format(
                row['numSp'], row['nomSp'], row['prenomSp'], row['pays'], row['categorieSp'], row['dateNaisSp'], row['numEq'])
            # On affiche la requête pour comprendre la construction. A enlever une fois compris.
            print(query)
            cursor.execute(query)
        except IntegrityError as err:
            print(err)

    # Lecture de l'onglet LesEpreuves du fichier excel, en interprétant toutes les colonnes comme des string
    # pour construire uniformement la requête
    df_epreuves = pandas.read_excel(file, sheet_name='LesEpreuves', dtype=str)
    df_epreuves = df_epreuves.where(pandas.notnull(df_epreuves), 'null')

    cursor = data.cursor()
    for ix, row in df_epreuves.iterrows():
        try:
            query = "insert into V0_LesEpreuves values ({},'{}','{}','{}','{}',{},".format(
                row['numEp'], row['nomEp'], row['formeEp'], row['nomDi'], row['categorieEp'], row['nbSportifsEp'])

            if (row['dateEp'] != 'null'):
                query = query + "'{}')".format(row['dateEp'])
            else:
                query = query + "null)"
            # On affiche la requête pour comprendre la construction. A enlever une fois compris.
            print(query)
            cursor.execute(query)
        except IntegrityError as err:
            print(f"{err} : \n{row}")

#DONETODO 1.3a : modifier la lecture du fichier Excel pour lire l'ensemble des données et les intégrer dans le schéma de la BD V1
def read_excel_file_V1(data:sqlite3.Connection, file):
    # Lecture de l'onglet du fichier excel LesSportifsEQ, en interprétant toutes les colonnes comme des strings
    # pour construire uniformement la requête
    df_sportifs = pandas.read_excel(file, sheet_name='LesSportifsEQ', dtype=str)
    df_sportifs = df_sportifs.where(pandas.notnull(df_sportifs), 'null')

    cursor = data.cursor()
    for ix, row in df_sportifs.iterrows():
        try:
            query_sp = "insert into LesSportifs values ({},'{}','{}','{}','{}','{}')".format(
                row['numSp'], row['nomSp'], row['prenomSp'], row['pays'], row['categorieSp'], row['dateNaisSp'])
            if(row['numEq'] != 'null'):
                query_eq = "insert into LesEquipes values ({},{})".format(
                row['numSp'], row['numEq'])
                print(query_eq)
                cursor.execute(query_eq)
            # On affiche la requête pour comprendre la construction. A enlever une fois compris.
            print(query_sp)
            cursor.execute(query_sp)
        except IntegrityError as err:
            print(err)
    # Lecture de l'onglet du fichier excel LesEpreuves, en interprétant toutes les colonnes comme des string
    # pour construire uniformement la requête
    df_epreuves = pandas.read_excel(file, sheet_name='LesEpreuves', dtype=str)
    df_epreuves = df_epreuves.where(pandas.notnull(df_epreuves), 'null')

    df_resultats = pandas.read_excel(file, sheet_name='LesResultats', dtype=str)
    df_resultats = df_resultats.where(pandas.notnull(df_resultats), 'null')

    cursor = data.cursor()
    for ix, row in df_epreuves.iterrows():
        try:
            query = "insert into LesEpreuves values ({},'{}','{}','{}','{}',{},".format(
                row['numEp'], row['nomEp'], row['formeEp'], row['nomDi'], row['categorieEp'], row['nbSportifsEp'])

            if (row['dateEp'] != 'null'):
                query = query + "'{}',".format(row['dateEp'])
            else:
                query = query + "null,"
            resultat = True
            for ix_res, row_res in df_resultats.iterrows():
                if (row_res['numEp'] == row['numEp']):
                    query = query + "{},{},{})".format(row_res['gold'],row_res['silver'],row_res['bronze'])
                    resultat = False
            if resultat:
                query = query + "null,null,null)"
            # On affiche la requête pour comprendre la construction. A enlever une fois compris.
            print(query)
            cursor.execute(query)
        except IntegrityError as err:
            print(f"{err} : \n{row}")

    df_inscriptions = pandas.read_excel(file, sheet_name='LesInscriptions', dtype=str)
    df_inscriptions = df_inscriptions.where(pandas.notnull(df_inscriptions), 'null')

    cursor = data.cursor()
    for ix, row in df_inscriptions.iterrows():
        try:
            query = "insert into LesParticipants values ({},{})".format(
                row['numIn'], row['numEp'])
            # On affiche la requête pour comprendre la construction. A enlever une fois compris.
            print(query)
            cursor.execute(query)
        except IntegrityError as err:
            print(err)