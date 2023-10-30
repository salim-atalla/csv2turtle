import csv
import os
from rdflib import Graph, Literal, Namespace, RDF, RDFS, XSD

# Créez un graph RDF vide
g = Graph()

# Définissez un espace de noms pour vos ressources RDF
ex = Namespace("http://example.org/pets#")

# Définissez les classes RDF
g.add((ex.Pet, RDF.type, RDFS.Class))
g.add((ex.Dog, RDF.type, RDFS.Class))
g.add((ex.Cat, RDF.type, RDFS.Class))
g.add((ex.Dog, RDFS.subClassOf, ex.Pet))
g.add((ex.Cat, RDFS.subClassOf, ex.Pet))

# Définissez les propriétés RDF
columns = [
    "url",
    "species",
    "breed_primary",
    "breed_secondary",
    "breed_mixed",
    "age",
    "sex",
    "size",
    "coat",
    "fixed",
    "house_trained",
    "declawed",
    "special_needs",
    "shots_current",
    "env_children",
    "env_dogs",
    "env_cats",
    "description",
]

# Chemin vers les dossiers d'entrée et de sortie
input_folder = "input"
output_folder = "output"

# Assurez-vous que le dossier de sortie existe
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Parcourez les fichiers .csv dans le dossier d'entrée
for filename in os.listdir(input_folder):
    if filename.endswith(".csv"):
        # Construisez le chemin complet des fichiers d'entrée et de sortie
        input_file = os.path.join(input_folder, filename)
        output_file = os.path.join(
            output_folder, os.path.splitext(filename)[0] + ".ttl"
        )

        # Ouvrez le fichier CSV contenant vos données
        with open(input_file, newline="") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=";")

            for index, row in enumerate(
                reader, start=1
            ):  # Utilisez un index de ligne comme identifiant unique
                # Générez un identifiant unique pour chaque animal en utilisant l'index de ligne
                pet_id = ex["pet_" + str(index)]

                # Associez l'individu à sa classe (Dog ou Cat)
                if row["species"] == "Dog":
                    g.add((pet_id, RDF.type, ex.Dog))
                elif row["species"] == "Cat":
                    g.add((pet_id, RDF.type, ex.Cat))
                else:
                    g.add((pet_id, RDF.type, ex.Pet))

                # Ajoutez les propriétés à l'individu animal
                for col in columns:
                    if row[col]:
                        if (
                            col == "breed_mixed"
                            or col == "fixed"
                            or col == "house_trained"
                            or col == "shots_current"
                            or col == "env_children"
                            or col == "env_dogs"
                        ):
                            # Si la colonne est booléenne, utilisez XSD.boolean
                            g.add(
                                (
                                    pet_id,
                                    ex[col],
                                    Literal(row[col], datatype=XSD.boolean),
                                )
                            )
                        else:
                            g.add(
                                (
                                    pet_id,
                                    ex[col],
                                    Literal(row[col], datatype=XSD.string),
                                )
                            )

        # Écrivez le graph RDF dans un fichier Turtle
        g.serialize(destination=output_file, format="turtle")
