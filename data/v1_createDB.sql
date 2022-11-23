-- DONETODO 1.3a : Créer les tables manquantes et modifier celles ci-dessous
CREATE TABLE LesSportifs
(
  numSp NUMBER(4),
  nomSp VARCHAR2(20),
  prenomSp VARCHAR2(20),
  pays VARCHAR2(20),
  categorieSp VARCHAR2(10),
  dateNaisSp DATE,
  CONSTRAINT SP_PK PRIMARY KEY (numSp),
  CONSTRAINT SP_CK1 CHECK(numSp > 999),
  CONSTRAINT SP_CK2 CHECK(numSp < 1500),
  CONSTRAINT SP_CK3 CHECK(categorieSp IN ('feminin','masculin'))
);

CREATE TABLE LesEquipes
(
  numSp NUMBER(4),
  numEq NUMBER(3),
  CONSTRAINT EQ_PK PRIMARY KEY (numSp, numEq),
  CONSTRAINT EQ_CK1 CHECK(numEq > 0),
  CONSTRAINT EQ_CK2 CHECK(numEq < 101),
  FOREIGN KEY (numSp) REFERENCES LesSportifs(numSp)
);

CREATE TABLE LesParticipants
(
  numIns NUMBER(4),
  numEp NUMBER(4),
  CONSTRAINT PA_PK PRIMARY KEY (numIns, numEp),
  FOREIGN KEY (numIns) REFERENCES LesSportifs(numSp),
  FOREIGN KEY (numIns) REFERENCES LesEquipes(numEq),
  FOREIGN KEY (numEp) REFERENCES LesEpreuves(numEp),
);

CREATE TABLE LesEpreuves
(
  numEp NUMBER(3),
  nomEp VARCHAR2(20),
  formeEp VARCHAR2(13),
  nomDi VARCHAR2(25),
  categorieEp VARCHAR2(10),
  nbSportifsEp NUMBER(2),
  dateEp DATE,
  res_or NUMBER(4),
  res_argent NUMBER(4),
  res_bronze NUMBER(4),
  CONSTRAINT EP_PK PRIMARY KEY (numEp),
  CONSTRAINT EP_CK1 CHECK (formeEp IN ('individuelle','par equipe','par couple')),
  CONSTRAINT EP_CK2 CHECK (categorieEp IN ('feminin','masculin','mixte')),
  CONSTRAINT EP_CK3 CHECK (numEp > 0),
  CONSTRAINT EP_CK4 CHECK (nbSportifsEp > 0),
  FOREIGN KEY (res_or) REFERENCES LesParticipants(numIns),
  FOREIGN KEY (res_argent) REFERENCES LesParticipants(numIns),
  FOREIGN KEY (res_bronze) REFERENCES LesParticipants(numIns)
);

-- DONETODO 1.4a : ajouter la définition de la vue LesAgesSportifs

CREATE VIEW IF NOT EXISTS LesAgesSportifs(numSp, age)
AS
   SELECT numSp, strftime('%Y', 'now') - strftime('%Y', dateNaisSp)
   FROM LesSportifs
   WHERE strftime('%m', 'now') > strftime('%m', dateNaisSp) OR
         strftime('%m', 'now') = strftime('%m', dateNaisSp) AND strftime('%d', 'now') = strftime('%d', dateNaisSp)
   UNION
   SELECT numSp, strftime('%Y', 'now') - strftime('%Y', dateNaisSp) - 1
   FROM LesSportifs
   WHERE NOT(strftime('%m', 'now') > strftime('%m', dateNaisSp) OR
         strftime('%m', 'now') = strftime('%m', dateNaisSp) AND strftime('%d', 'now') = strftime('%d', dateNaisSp));

-- DONETODO 1.5a : ajouter la définition de la vue LesNbsEquipiers

CREATE VIEW IF NOT EXISTS LesNbsEquipiers(numSp, nbEquipiers, numEq)
AS
    WITH nbPerEq as(
        SELECT COUNT(numEq)-1 nbEquipiers, numEq
        FROM LesEquipes
        GROUP BY numEq
    )
    SELECT numSp, nbEquipiers, numEq
    FROM LesSportifs JOIN LesEquipes USING(numSp)
                     JOIN nbPerEq USING(numEq);

-- TODO 3.3 : ajouter les éléments nécessaires pour créer le trigger (attention, syntaxe SQLite différent qu'Oracle)
