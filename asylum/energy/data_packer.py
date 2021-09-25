from datetime import datetime, date, time

from asylum import create_sqlite3_connection

sql_select_energy = """SELECT
    id,
    time,
    production,
    import,
    export,
    power_production,
    power_import,
    power_export,
    production_deye,
    power_production_deye from energy where time > ?"""

sql_select_energy_daily = """SELECT
    day_ordinal,
    production_offset,
    import_offset,
    export_offset,
    production_deye_offset from energy_daily order by id desc limit 1"""

sql_insert_daily = """INSERT INTO energy_daily (
    day_ordinal,
    production,
    import,
    export,
    production_offset,
    import_offset,
    export_offset,
    max_power_production,
    max_power_import,
    max_power_export,
    max_power_consumption,
    max_power_use,
    max_power_store,
    production_deye,
    production_deye_offset) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""


def main():
    db_con = create_sqlite3_connection()
    last = db_con.execute(sql_select_energy_daily).fetchone()

    last_production_offset = last_production_deye_offset = last_import_offset = last_export_offset = 0
    if last is not None:
        start_day = last[0] + 1
        tajm = datetime.combine(date.fromordinal(start_day), time())
        energy_data = db_con.execute(sql_select_energy, (tajm.timestamp(), )).fetchall()
        last_production_offset = last[1]
        last_import_offset = last[2]
        last_export_offset = last[3]
        last_production_deye_offset = last[4]
    else:
        energy_data = db_con.execute(sql_select_energy, (0, )).fetchall()
        start_day = datetime.fromtimestamp(energy_data[0][1]).date().toordinal()

    print("Zaczynamy od ", str(date.fromordinal(start_day)))

    days = {}
    for x in range(start_day, date.today().toordinal()):
        days[x] = []

    for entry in energy_data:
        day_number = datetime.fromtimestamp(entry[1]).date().toordinal()
        if day_number in days:
            days[day_number].append(entry)

    for day, datas in sorted(days.items()):
        max_power_production = 0
        max_power_import = 0
        max_power_export = 0
        max_power_consumption = 0
        max_power_use = 0
        max_power_store = 0
        for entry in datas:
            id, dat, prod, imp, exp, power_production, power_import, power_export, production_deye, power_production_deye = entry
            total_power_prod = power_production + power_production_deye
            max_power_production = max(max_power_production, total_power_prod)
            max_power_import = max(max_power_import, power_import)
            max_power_export = max(max_power_export, power_export)
            max_power_consumption = max(max_power_consumption, power_import + total_power_prod - power_export)
            max_power_use = max(max_power_use, total_power_prod - power_export)
            max_power_store = int(max(max_power_store, power_export * 0.8 - power_import))

        production = production_deye = import_ = export = 0
        if datas:
            production = datas[-1][2] - datas[0][2]
            production_deye = datas[-1][8] - datas[0][8]
            import_ = datas[-1][3] - datas[0][3]
            export = datas[-1][4] - datas[0][4]
            last_production_offset = datas[-1][2]
            last_import_offset = datas[-1][3]
            last_export_offset = datas[-1][4]
            last_production_deye_offset = datas[-1][8]

        print("[Dzien {}] pomiarow: {}, produkcja: {}, produkcja deye: {}, import: {}, export: {}".format(
            str(date.fromordinal(day)), len(datas), production, production_deye, import_, export
        ))

        db_con.execute(sql_insert_daily, (
            day,
            production,
            import_,
            export,
            last_production_offset,
            last_import_offset,
            last_export_offset,
            max_power_production,
            max_power_import,
            max_power_export,
            max_power_consumption,
            max_power_use,
            max_power_store,
            production_deye,
            last_production_deye_offset
        ))

    db_con.commit()
    db_con.close()


if __name__ == '__main__':
    main()
