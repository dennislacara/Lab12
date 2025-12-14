from database.DB_connect import DBConnect
from model.dto.connessione_DTO import ConnessioneDTO
from model.dto.rifugio_DTO import RifugioDTO

class DAO:
    """
    Implementare tutte le funzioni necessarie a interrogare il database.
    """
    @staticmethod
    def get_all_connessioni(year: int):
        try:
            conn = DBConnect.get_connection()
        except Exception as e:
            conn = None
            print(e)

        if conn is None:
            print('Connessione al database fallita!')

        cursor = conn.cursor(dictionary=True)
        query = '''
                SELECT id, id_rifugio1, id_rifugio2, distanza, difficolta, anno
                from connessione c
                where anno <= %s
                '''
        cursor.execute(query, (year,))
        result = []
        for row in cursor:
            oggetto_connessione = ConnessioneDTO(**row)
            #print(oggetto_connessione)
            result.append(oggetto_connessione)
        print('Database interrogato attraverso la funzione della classe DAO: get_all_connessioni(*)')

        conn.close()
        cursor.close()

        return result

    @staticmethod
    def get_all_rifugi():
        try:
            conn = DBConnect.get_connection()
        except Exception as e:
            print(e)

        result = {}
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT *
            FROM rifugio r
            """
        cursor.execute(query)

        for row in cursor:
            oggetto_rifugio = RifugioDTO(**row)
            result[row['id']] = oggetto_rifugio
            #print(oggetto_rifugio)

        cursor.close()
        conn.close()
        print('Database interrogato attraverso la funzione della classe DAO: get_all_rifugi()')

        return result

    # TODO
