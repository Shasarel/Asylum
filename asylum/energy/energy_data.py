import re
import requests

from asylum import config

def get_data():
    try:
        data = requests.get(config['SUBSYSTEMS']['iotchief_url']+"energy", timeout=1).json()

        if not data['has_data']:
            return None

        power_prod = data['energy_data']['flara_data']['power'] + data['energy_data']['deye_data']['power']
        energy_prod = data['energy_data']['flara_data']['total_energy'] + data['energy_data']['deye_data']['total_energy']

        power_import = data['energy_data']['power_import']
        power_export = data['energy_data']['power_export']
        energy_import = data['energy_data']['energy_import']
        energy_export = data['energy_data']['energy_export']

        return {
            'power_consumption': max(0, power_import + power_prod - power_export),
            'power_production': power_prod,
            'power_use': max(0, power_prod - power_export),
            'power_import': power_import,
            'power_export': power_export,
            'power_store': int(power_export * 0.8 - power_import),
            'total_energy_production': energy_prod,
            'total_energy_import': energy_import,
            'total_energy_export': energy_export,
        }
    except (requests.exceptions.RequestException, ValueError) as e:
        return None


def test_flara_connection():
    data = get_flara_data()
    return data is not None

def test_emeter_connection():
    data = get_emeter_data()
    return data is not None
