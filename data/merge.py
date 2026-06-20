# Script generado automáticamente desde el notebook de desarrollo
import pandas as pd
import os
import urllib.request

def download_and_merge():
    owid_url = 'https://owid-public.owid.io/data/energy/owid-energy-data.csv'

    # Función para buscar archivos localmente
    def find_local_file(filename):
        if os.path.exists(filename):
            return filename
        parent = os.path.join('..', filename)
        if os.path.exists(parent):
            return parent
        return None

    owid_path = find_local_file('owid-energy-data.csv')
    kaggle_path = find_local_file('global-data-on-sustainable-energy.csv')

    # Descargar si no existen localmente
    if not owid_path:
        print('Descargando OWID Energy Data...')
        urllib.request.urlretrieve(owid_url, 'owid-energy-data.csv')
        owid_path = 'owid-energy-data.csv'

    if not kaggle_path:
        print('Error: global-data-on-sustainable-energy.csv no encontrado en CWD ni en el directorio superior.')
        return

    # Carga de datos
    owid = pd.read_csv(owid_path)
    kaggle = pd.read_csv(kaggle_path)

    # Normalización y merge
    kaggle_renamed = kaggle.rename(columns={
        'Entity': 'country',
        'Year': 'year',
        'Access to electricity (% of population)': 'access_to_electricity',
        'Renewable energy share in the total final energy consumption (%)': 'renewable_share_of_total_energy',
        'Energy intensity level of primary energy (MJ/$2017 PPP GDP)': 'energy_intensity_primary_energy',
        'gdp_per_capita': 'gdp_per_capita'
    })

    owid_cols = [
        'country', 'year', 'iso_code', 'population', 'gdp',
        'carbon_intensity_elec', 'energy_per_capita', 'fossil_share_energy',
        'coal_electricity', 'gas_electricity', 'nuclear_electricity',
        'solar_electricity', 'wind_electricity', 'hydro_electricity'
    ]
    owid_filtered = owid[owid_cols].rename(columns={
        'coal_electricity': 'coal_elec',
        'gas_electricity': 'gas_elec',
        'nuclear_electricity': 'nuclear_elec',
        'solar_electricity': 'solar_elec',
        'wind_electricity': 'wind_elec',
        'hydro_electricity': 'hydro_elec'
    })

    # Mapeo de continentes
    africa = ['Algeria', 'Angola', 'Benin', 'Botswana', 'Burkina Faso', 'Burundi', 'Cameroon', 'Central African Republic', 'Chad', 'Comoros', 'Congo', 'Djibouti', 'Egypt', 'Equatorial Guinea', 'Eritrea', 'Eswatini', 'Ethiopia', 'Gabon', 'Gambia', 'Ghana', 'Guinea', 'Guinea-Bissau', 'Kenya', 'Lesotho', 'Liberia', 'Libya', 'Madagascar', 'Malawi', 'Mali', 'Mauritania', 'Mauritius', 'Morocco', 'Mozambique', 'Namibia', 'Niger', 'Nigeria', 'Rwanda', 'Sao Tome and Principe', 'Senegal', 'Seychelles', 'Sierra Leone', 'Somalia', 'South Africa', 'South Sudan', 'Sudan', 'Togo', 'Tunisia', 'Uganda', 'Zambia', 'Zimbabwe']
    asia = ['Afghanistan', 'Armenia', 'Azerbaijan', 'Bahrain', 'Bangladesh', 'Bhutan', 'Cambodia', 'China', 'Cyprus', 'Georgia', 'India', 'Indonesia', 'Iraq', 'Israel', 'Japan', 'Jordan', 'Kazakhstan', 'Kuwait', 'Kyrgyzstan', 'Lebanon', 'Malaysia', 'Maldives', 'Mongolia', 'Myanmar', 'Nepal', 'Oman', 'Pakistan', 'Philippines', 'Qatar', 'Saudi Arabia', 'Singapore', 'Sri Lanka', 'Tajikistan', 'Thailand', 'Turkey', 'Turkmenistan', 'United Arab Emirates', 'Uzbekistan', 'Yemen']
    europe = ['Albania', 'Austria', 'Belarus', 'Belgium', 'Dosnia and Herzegovina', 'Bulgaria', 'Croatia', 'Czechia', 'Denmark', 'Estonia', 'Finland', 'France', 'Germany', 'Greece', 'Hungary', 'Iceland', 'Ireland', 'Italy', 'Latvia', 'Lithuania', 'Luxembourg', 'Malta', 'Montenegro', 'Netherlands', 'North Macedonia', 'Norway', 'Poland', 'Portugal', 'Romania', 'Serbia', 'Slovakia', 'Slovenia', 'Spain', 'Sweden', 'Switzerland', 'Ukraine', 'United Kingdom', 'Bosnia and Herzegovina']
    north_america = ['Antigua and Barbuda', 'Aruba', 'Bahamas', 'Barbados', 'Belize', 'Bermuda', 'Canada', 'Cayman Islands', 'Costa Rica', 'Cuba', 'Dominica', 'Dominican Republic', 'El Salvador', 'Grenada', 'Guatemala', 'Honduras', 'Jamaica', 'Mexico', 'Nicaragua', 'Panama', 'Puerto Rico', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines', 'Trinidad and Tobago', 'United States', 'Haiti']
    south_america = ['Argentina', 'Brazil', 'Chile', 'Colombia', 'Ecuador', 'French Guiana', 'Guyana', 'Paraguay', 'Peru', 'Suriname', 'Uruguay']
    oceania = ['Australia', 'Fiji', 'Kiribati', 'Nauru', 'New Caledonia', 'New Zealand', 'Papua New Guinea', 'Samoa', 'Solomon Islands', 'Tonga', 'Tuvalu', 'Vanuatu']

    c_map = {}
    for c in africa: c_map[c] = 'Africa'
    for c in asia: c_map[c] = 'Asia'
    for c in europe: c_map[c] = 'Europe'
    for c in north_america: c_map[c] = 'North America'
    for c in south_america: c_map[c] = 'South America'
    for c in oceania: c_map[c] = 'Oceania'

    merged_countries = pd.merge(kaggle_renamed, owid_filtered, on=['country', 'year'], how='inner')
    merged_countries['region'] = merged_countries['country'].map(c_map)
    merged_countries['is_region'] = False

    regions_list = ['Africa', 'Asia', 'Europe', 'North America', 'South America', 'Oceania']
    regions_owid = owid_filtered[owid_filtered['country'].isin(regions_list) & (owid_filtered['year'] >= 2000) & (owid_filtered['year'] <= 2020)].copy()
    regions_owid['region'] = regions_owid['country']
    regions_owid['is_region'] = True

    final_df = pd.concat([merged_countries, regions_owid], ignore_index=True)
    os.makedirs('data', exist_ok=True)
    final_df.to_csv('data/merged_dataset.csv', index=False)
    print('Merge completado exitosamente.')

if __name__ == '__main__':
    download_and_merge()
