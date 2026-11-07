from database.DB_connect import DBConnect
from model.distributore_DTO import Distributore

"""
    DISTRIBUTORE DAO
    Gestisce le operazioni di accesso al database.
"""

class DistributoreDAO:
    @staticmethod
    def get_distributori() -> list[Distributore] | None:
        """
        Restituisce tutti i distributori presenti nel database
        :return: lista di tutti i Distributori
        """
        cnx = DBConnect.get_connection()
        result = []

        if cnx is None:
            print("❌ Errore di connessione al database.")
            return None

        cursor = cnx.cursor(dictionary=True)
        query = """ SELECT * FROM distributore """
        try:
            cursor.execute(query)
            for row in cursor:
                distributore = Distributore(
                    id=row["id"],
                    nome=row["nome"],
                    indirizzo=row["indirizzo"],
                )
                result.append(distributore)
        except Exception as e:
            print(f"Errore durante la query get_distributori: {e}")
            result = None
        finally:
            cursor.close()
            cnx.close()

        return result
