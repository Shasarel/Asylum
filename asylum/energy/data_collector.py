from sqlite3 import Error

from asylum import create_sqlite3_connection
from asylum.energy import energy_data


def main():
    db_conn = create_sqlite3_connection()
    cursor = db_conn.cursor()
    data = energy_data.get_data()

    if data is not None:
        try:
            sql = "INSERT INTO energy (production, import, export, power_production, power_import, power_export, production_deye, power_production_deye) \
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
            cursor.execute(sql, (
                data['energy_flara'],
                data['total_energy_import'],
                data['total_energy_export'],
                data['power_flara'],
                data['power_import'],
                data['power_export'],
                data['energy_deye'],
                data['power_deye'],
            ))
            db_conn.commit()
        except Error as e:
            print(e)

        cursor.close()
        db_conn.close()


if __name__ == '__main__':
    main()
