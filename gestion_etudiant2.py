import sqlite3
connexion=sqlite3.connect("DataBase.db")
curseur = connexion.cursor()

#curseur.execute("""
#                      CREATE TABLE IF NOT EXISTS Etudiants(
#                        ID INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
#                        Nom VARCHAR(60),
#                        Code INTEGER,
#                        Note_devoir REAL,
#                        Note_examen REAL,
#                        Moyenne REAL,
#                        date_inscription TEXT DEFAULT (DATETIME('now','localtime'))
#                      )
#                      """)




etudiants = []

#fonction qui calcule la moyenne d'un étudiant
def calculer_moyenne(etudiant):
    moyenne =etudiant[4]*0.4 + etudiant[5]*0.6
    return moyenne

#fonction pour ajouter des etudiants
def ajouter_etudiant():
    nom=input("Nom:")
    while True:
        code=input("Code permanent:")
        if(len(code)==6):
            break
        else:
            print("Entrez un code à 6 chiffre!!!!")
    #Controle de saisie pour la note du devoir
    while True:
        try:
            note_devoir=float(input("Note du devoir: "))
            if(note_devoir>=0 and note_devoir<=20):
                break
            
            print("Erreur:la note est invalide.Veillez réessayer")
        except ValueError:
            print("Valeur saisi est invalide")
    #controle de saisi pour la note d'examen
    while True:
        try:
            note_examen=float(input("note examen: "))
            if(note_examen>=0 and note_examen<=20):
                break
            print("Erreur:la note est invalide.Veillez réessayer")
        except ValueError:
            print("Valeur saisir est invalide")
    moyenne=note_devoir*0.4 + note_examen*0.6
    infos_etudiant=( nom,code,note_devoir,note_examen,moyenne)
    
    etudiants.append(infos_etudiant)
    print(f"L'etudiant {nom} a été ajouter avec succés.")
    curseur.executemany("INSERT INTO Etudiants(Nom,Code,Note_devoir,Note_examen,Moyenne) VALUES(?,?,?,?,?)",etudiants)
    connexion.commit()
    etudiants.remove(infos_etudiant)
    
curseur.execute("SELECT * FROM Etudiants")
students=curseur.fetchall()
#fonction pour Afficher le meilleur etudiant et sa moyenne 
def meilleur_etudiant_uam():
    meilleur_etudiant=calculer_moyenne(students[0])
    nom_meilleur_etudiant=students[0][1]
    for etu in students:
        moyenne=calculer_moyenne(etu)
        if(meilleur_etudiant<moyenne):
            meilleur_etudiant=moyenne
            nom_meilleur_etudiant=etu[1]
            
    print(f"Meilleur etudiant: {nom_meilleur_etudiant}")
    print(f"Moyenne meilleur etudiant : {meilleur_etudiant:.1f}/20")

#Fonction pour calculer la moyenne general de la classe
def moyenne_general():
    somme_moyenne=0
    for etu in students:
        moyenne=calculer_moyenne(etu)
        somme_moyenne+=moyenne
    moyenne_general=somme_moyenne/len(students)
    print(f"Moyenne générale: {moyenne_general:.1f}/20")
    
#Fonction pour Afficher tous les etudiants, leur moyenne ainsi que leur appréciation en foncton de leur moyenne 
def Afficher_etudiant_Note():
    for etu in students:
        moyenne=calculer_moyenne(etu)
        if(moyenne>=10):
            print(f"{etu[1]}:{moyenne:.1f}/20 -Moyenne suffissante")
        else:
            print(f"{etu[1]}:{moyenne:.1f}/20 -Moyenne insuffissante")

#Fonction pour Afficher le nombre d'etudiant et le nombre d'etudiant admis
def  Nombre_etudiant_admis():
    admis=0
    nbre_etudiant=0
    for etu in students:
        nbre_etudiant+=1
        moyenne=calculer_moyenne(etu)
        if(moyenne>=10):
            admis+=1
    print(f"Nombre d'étudiant: {nbre_etudiant}")
    print(f"Etudiant ayant une moyenne >=10: {admis}")

def Bilan_classe():
    print("==================Bilan de la classe ========================")
    Nombre_etudiant_admis()
    moyenne_general()
    meilleur_etudiant_uam()
    
def Supprimer_etudinat(code):
    for etu in students:
        if(etu[2]==code):
            curseur.execute("DELETE FROM Etudiants WHERE Code=?",(code,))
            connexion.commit()
            print(f"L'étudiant {etu[1]} supprimer avec succés !!!")
            break

def Afficher_Etudiant():
    print("=========================Liste des etudiants MPI ===================")
    print("Nom_complet\tCode\tFilière")
    for etu in students:
        print(f"{etu[1]}\t{etu[2]}\tMPI")

def Verification():
    if(len(students)!=0):
        return True
        
        
while True:
    print("-----------------------------------------------------------------------")
    print("===================GESTION DES ETUDIANTS================================")
    print("-----------------------------------------------------------------------")
    print("===========================MENU PRINCIPALE==============================")

    print("1-Ajouter un etudiant\n2-Afficher tous les etudiant \n3-Supprimer un etudiant\n4-Meilleur etudiant de l'université\n5-Nombre etudiant de la classe et nombre admis\n6-Afficher etudiant et note\n7-Bilan de la classe\n8-Moyenne Generale de la classe \n9-Quitter")
    choix=int(input("Veiller entre le numéro de l'opération a effectuer:"))
    match(choix):
        case 1:
            ajouter_etudiant()
            print("\n")

        case 2:
           if(Verification()==True):
                Afficher_Etudiant()
                print("\n")
           else:
               print("Votre systeme est vide")
               print("\n")
        case 3:
            if(Verification()==True):
                code=int(input("Veillez saisir le code permanent de l'etudiant à supprimer: "))
                Supprimer_etudinat(code)
                print("\n")
            else:
                print("Votre système est vide")
                print("\n")
        case 4:
            if(Verification()==True):
                meilleur_etudiant_uam()
                print("\n")
            else:
                print("Votre système est vide")
                print("\n")
        case 5:
            if(Verification()==True):
                Nombre_etudiant_admis()
                print("\n")
            else:
                print("Votre système est vide")
                print("\n")
                
        case 6:
            if(Verification()==True):
                Afficher_etudiant_Note()
                print("\n")
            else:
                print("Votre système est vide")
                print("\n")
        case 7:
            if(Verification()==True):
                Bilan_classe()
                print("\n")
            else:
                print("Votre système est vide")
                print("\n")
        case 8:
            if(Verification()==True):
                moyenne_general()
                print("\n")
            else:
                print("Votre système est vide")
                print("\n")
        case 9:
            print("Merci d'avoir utiliser le systéme de Gestion des etudiant de Dieng_hi-tech")
            break
        
connexion.close()