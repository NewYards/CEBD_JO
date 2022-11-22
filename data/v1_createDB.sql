-- TODO 1.3a : Créer les tables manquantes et modifier celles ci-dessous
CREATE TABLE LesSportifsEQ
(
  numSp NUMBER(4),
  nomSp VARCHAR2(20),
  prenomSp VARCHAR2(20),
  pays VARCHAR2(20),
  categorieSp VARCHAR2(10),
  dateNaisSp DATE,
  numEq NUMBER(4),
  CONSTRAINT SP_CK1 CHECK(numSp > 0),
  CONSTRAINT SP_CK2 CHECK(categorieSp IN ('feminin','masculin')),
  CONSTRAINT SP_CK3 CHECK(numEq > 0)
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
  CONSTRAINT EP_PK PRIMARY KEY (numEp),
  CONSTRAINT EP_CK1 CHECK (formeEp IN ('individuelle','par equipe','par couple')),
  CONSTRAINT EP_CK2 CHECK (categorieEp IN ('feminin','masculin','mixte')),
  CONSTRAINT EP_CK3 CHECK (numEp > 0),
  CONSTRAINT EP_CK4 CHECK (nbSportifsEp > 0)
);

-- DONETODO 1.4a : ajouter la définition de la vue LesAgesSportifs

CREATE VIEW IF NOT EXISTS LesAgesSportifs(numSp, age)
AS
   SELECT numSp, strftime('%Y', 'now') - strftime('%Y', dateNaisSp)
   FROM LesSportifsEQ
   WHERE strftime('%m', 'now') > strftime('%m', dateNaisSp) OR
         strftime('%m', 'now') = strftime('%m', dateNaisSp) AND strftime('%d', 'now') = strftime('%d', dateNaisSp)
   UNION
   SELECT numSp, strftime('%Y', 'now') - strftime('%Y', dateNaisSp) - 1
   FROM LesSportifsEQ
   WHERE NOT(strftime('%m', 'now') > strftime('%m', dateNaisSp) OR
         strftime('%m', 'now') = strftime('%m', dateNaisSp) AND strftime('%d', 'now') = strftime('%d', dateNaisSp));

-- DONETODO 1.5a : ajouter la définition de la vue LesNbsEquipiers

CREATE VIEW IF NOT EXISTS LesNbsEquipiers(numSp, nbEquipiers, numEq)
AS
    WITH nbPerEq as(
        SELECT COUNT(numEq)-1 nbEquipiers, numEq
        FROM LesSportifsEQ
        GROUP BY numEq
    )
    SELECT numSp, nbEquipiers, numEq
    FROM LesSportifsEQ JOIN nbPerEq USING(numEq);

-- TODO 3.3 : ajouter les éléments nécessaires pour créer le trigger (attention, syntaxe SQLite différent qu'Oracle)
