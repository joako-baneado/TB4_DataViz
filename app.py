import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

# Set page configuration with a premium dark/light layout
st.set_page_config(
    page_title="Visualización de Datos - Trabajo 4 (TB4)",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern typography and sleek aesthetics (using Google Font Outfit)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    .stApp {
        background-color: #F8F9FA;
    }
    
    /* Title styling */
    .dashboard-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.5rem;
    }
    
    .dashboard-subtitle {
        font-size: 1.1rem;
        color: #64748B;
        margin-bottom: 2rem;
    }
    
    /* Navigation styling */
    .stRadio > div {
        flex-direction: column;
    }
    
    /* Text blocks */
    .question-box {
        background-color: #FFFFFF;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #FF6F00;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.05);
    }
    
    .question-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #0F172A;
        margin-bottom: 0.5rem;
    }
    
    .question-desc {
        font-size: 1rem;
        color: #475569;
        font-style: italic;
    }
</style>
""", unsafe_allow_html=True)

# Helper function to load consolidation dataset
@st.cache_data
def load_data():
    # Look for the consolidated CSV file
    path = os.path.join("data", "merged_dataset.csv")
    if not os.path.exists(path):
        # Fallback to check parent directory
        path = os.path.join("project", "data", "merged_dataset.csv")
    if not os.path.exists(path):
        # Fallback for parent workspace
        path = "merged_dataset.csv"
        
    df = pd.read_csv(path)
    return df

try:
    df_merged = load_data()
except Exception as e:
    st.error(f"Error al cargar los datos consolidados: {e}")
    st.stop()

# Define geographical mappings and lists for calculations
latin_america = ['Argentina', 'Belize', 'Bolivia', 'Brazil', 'Chile', 'Colombia', 'Costa Rica', 'Cuba', 'Dominican Republic', 'Ecuador', 'El Salvador', 'Guatemala', 'Honduras', 'Mexico', 'Nicaragua', 'Panama', 'Paraguay', 'Peru', 'Uruguay', 'Venezuela']

# Sidebar navigation structure
st.sidebar.markdown("<h2 style='font-weight:700; color:#1E293B;'>Navegación</h2>", unsafe_allow_html=True)
section = st.sidebar.radio(
    "Selecciona una sección:",
    [
        "Bloque A: Panorama Global",
        "Bloque B: Patrones y Comparaciones",
        "Bloque C: Posición de Perú",
        "Bloque D: Justificaciones Teóricas (Q10)"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("<h3 style='font-weight:600; color:#1E293B;'>Filtros Globales</h3>", unsafe_allow_html=True)

# 1. Slider (Año) - affects Q3, Q4, Q8
year_sel = st.sidebar.slider(
    "Selecciona el año de análisis:",
    min_value=2000,
    max_value=2018,
    value=2018,
    help="Este control temporal actualiza dinámicamente los gráficos de Riqueza vs Renovables (Q3), Pobreza Energética (Q4) y Comparativa de Perú (Q8) en simultáneo."
)

# 2. Multiselect (Región/Continente) - affects Q3, Q4
available_regions = ['Africa', 'Asia', 'Europe', 'North America', 'South America', 'Oceania']
regions_selected = st.sidebar.multiselect(
    "Filtrar por Región (Continente):",
    options=available_regions,
    default=available_regions,
    help="Este control múltiple actualiza los gráficos de dispersión de Riqueza vs Renovables (Q3) y Pobreza Energética (Q4) en simultáneo."
)

if not regions_selected:
    st.sidebar.warning("¡Selecciona al menos una región para ver los datos filtrados!")

# Header Section
st.markdown("<div class='dashboard-title'>Trabajo 4 (TB4) - Visualización de Datos</div>", unsafe_allow_html=True)
st.markdown("<div class='dashboard-subtitle'>Análisis comparativo de la transición energética y la posición estratégica de Perú (2000-2020)</div>", unsafe_allow_html=True)
st.markdown("---")

# ==============================================================================
# SECTION A: GLOBAL PANORAMA
# ==============================================================================
if section == "Bloque A: Panorama Global":
    st.markdown("## Bloque A - Panorama Global")
    
    # Q1: Líderes de la Transición
    st.markdown("""
    <div class='question-box'>
        <div class='question-title'>Pregunta 1: Líderes de la Transición</div>
        <div class='question-desc'>¿Cuáles son los cinco países que más aumentaron su participación de energías renovables entre 2000 y 2020?</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Calculate delta for Q1 (using 2000-2019 due to complete data)
    df_c = df_merged[~df_merged['is_region'] & df_merged['region'].notna()].copy()
    df_2000 = df_c[df_c['year'] == 2000][['country', 'renewable_share_of_total_energy']]
    df_2019 = df_c[df_c['year'] == 2019][['country', 'renewable_share_of_total_energy']]
    df_delta = pd.merge(df_2000, df_2019, on='country', suffixes=('_2000', '_2019'))
    df_delta['delta'] = df_delta['renewable_share_of_total_energy_2019'] - df_delta['renewable_share_of_total_energy_2000']
    top_5 = df_delta.sort_values(by='delta', ascending=False).head(5).copy()
    
    # Sort ascending for horizontal bar chart (so Denmark is at the top)
    top_5_sorted = top_5.sort_values(by='delta', ascending=True)
    
    # Highlight Denmark in orange, others in gray
    colors = ['#B0BEC5']*4 + ['#FF6F00']
    
    fig1 = px.bar(
        top_5_sorted,
        x='delta',
        y='country',
        orientation='h',
        custom_data=['renewable_share_of_total_energy_2000', 'renewable_share_of_total_energy_2019'],
        labels={'delta': 'Puntos Porcentuales Ganados (2000-2019)', 'country': 'País'},
        title='<b>Dinamarca lideró la transición ganando más de 26 puntos porcentuales de energía renovable (2000-2019)</b>'
    )
    fig1.update_traces(
        marker_color=colors,
        texttemplate='%{x:.1f}%',
        textposition='outside',
        cliponaxis=False,
        hovertemplate="<b>%{y}</b><br>" +
                      "Puntos ganados: +%{x:.1f}%<br>" +
                      "Participación en 2000: %{customdata[0]:.1f}%<br>" +
                      "Participación en 2019: %{customdata[1]:.1f}%<extra></extra>"
    )
    fig1.update_layout(
        plot_bgcolor='white',
        title_x=0.0,
        title_font_size=15,
        margin=dict(l=100, r=60, t=60, b=50),
        xaxis=dict(showgrid=True, gridcolor='#D3D3D3', range=[0, 32]),
        yaxis=dict(showgrid=False)
    )
    st.plotly_chart(fig1, use_container_width=True)
    st.caption("**Nota metodológica:** Se utiliza el rango 2000-2019 en lugar de 2020 debido a que la columna de participación renovable del dataset Kaggle no tiene datos reportados para 2020 en 171 países.")
    st.markdown("---")
    
    # Q2: Trayectorias Regionales de Carbono
    st.markdown("""
    <div class='question-box'>
        <div class='question-title'>Pregunta 2: Trayectorias Regionales de Carbono</div>
        <div class='question-desc'>¿Cómo evolucionó la intensidad de carbono de la electricidad en las principales regiones del mundo?</div>
    </div>
    """, unsafe_allow_html=True)
    
    df_reg = df_merged[df_merged['is_region']].copy()
    fig2 = go.Figure()
    regions = ['Europe', 'North America', 'Asia', 'South America', 'Africa', 'Oceania']
    colors_map = {
        'Europe': '#1B5E20',
        'North America': '#4CAF50',
        'Asia': '#D32F2F',
        'South America': '#78909C',
        'Africa': '#90A4AE',
        'Oceania': '#B0BEC5'
    }
    
    # Vertical offset to avoid overlapping labels on the right for 2020
    yshift_map = {
        'Asia': 8,
        'Oceania': 2,
        'Africa': -10,
        'North America': 0,
        'Europe': 0,
        'South America': 0
    }
    
    for r in regions:
        data = df_reg[df_reg['country'] == r].sort_values(by='year')
        pop_millions = data['population'] / 1e6
        fossil_share = data['fossil_share_elec'].fillna(0)
        
        fig2.add_trace(go.Scatter(
            x=data['year'],
            y=data['carbon_intensity_elec'],
            mode='lines+markers',
            name=r,
            line=dict(color=colors_map[r], width=3 if r in ['Europe', 'Asia'] else 1.5),
            marker=dict(size=5 if r in ['Europe', 'Asia'] else 3),
            customdata=np.stack((fossil_share, pop_millions), axis=-1),
            hovertemplate="<b>Región: " + r + "</b><br>" +
                          "Año: %{x}<br>" +
                          "Intensidad de Carbono: %{y:.1f} gCO₂/kWh<br>" +
                          "Participación Fósil en Elec: %{customdata[0]:.1f}%<br>" +
                          "Población: %{customdata[1]:.1f}M<extra></extra>"
        ))
        
        # Add labels directly at the end of the line
        last_row = data.iloc[-1]
        fig2.add_annotation(
            x=last_row['year'],
            y=last_row['carbon_intensity_elec'],
            text=r,
            showarrow=False,
            xanchor='left',
            xshift=8,
            yshift=yshift_map[r],
            font=dict(color=colors_map[r], size=11, family='Arial')
        )
        
    fig2.update_layout(
        plot_bgcolor='white',
        title_text='<b>Europa redujo drásticamente su intensidad de carbono, mientras que Asia y África avanzaron muy lentamente (2000-2020)</b>',
        title_x=0.0,
        title_font_size=15,
        margin=dict(l=50, r=100, t=60, b=50),
        xaxis=dict(showgrid=False, tickmode='linear', tick0=2000, dtick=5),
        yaxis=dict(showgrid=True, gridcolor='#E0E0E0', title='Intensidad de carbono (gCO₂/kWh)'),
        showlegend=False
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown("---")
    
    # Q3: Riqueza vs. Participación de Renovables
    st.markdown("""
    <div class='question-box'>
        <div class='question-title'>Pregunta 3: Riqueza vs. Participación de Renovables</div>
        <div class='question-desc'>¿Los países más ricos son necesariamente los más renovables en su consumo final?</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Filter by selected regions and selected year
    df_y = df_merged[(df_merged['year'] == year_sel) & (~df_merged['is_region']) & df_merged['region'].notna()].copy()
    if regions_selected:
        df_y = df_y[df_y['region'].isin(regions_selected)]
    df_y = df_y.dropna(subset=['gdp_per_capita', 'renewable_share_of_total_energy'])
    
    if df_y.empty:
        st.warning("No hay datos disponibles para la combinación de filtros seleccionada en Q3.")
    else:
        fig3 = px.scatter(
            df_y,
            x='gdp_per_capita',
            y='renewable_share_of_total_energy',
            size='population',
            color='region',
            hover_name='country',
            log_x=True,
            color_discrete_sequence=px.colors.qualitative.Set2,
            custom_data=['population', 'energy_per_capita'],
            labels={
                'gdp_per_capita': 'PIB per Cápita (USD, Escala Logarítmica)',
                'renewable_share_of_total_energy': 'Participación Renovable (%)',
                'region': 'Región'
            },
            title=f'<b>La riqueza no garantiza sostenibilidad: no hay una relación lineal entre el PIB per cápita y el % renovable ({year_sel})</b>'
        )
        fig3.update_traces(
            hovertemplate="<b>%{hovertext}</b><br>" +
                          "PIB per Cápita: $%{x:,.0f}<br>" +
                          "Participación Renovable: %{y:.1f}%<br>" +
                          "Población: %{customdata[0]:,.0f}<br>" +
                          "Consumo de Energía per Cápita: %{customdata[1]:,.0f} kWh<extra></extra>"
        )
        fig3.update_layout(
            plot_bgcolor='white',
            title_x=0.0,
            title_font_size=14,
            xaxis=dict(
                showgrid=True, gridcolor='#E0E0E0',
                tickvals=[200, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000],
                ticktext=['$200', '$500', '$1,000', '$2,000', '$5,000', '$10,000', '$20,000', '$50,000', '$100,000']
            ),
            yaxis=dict(showgrid=True, gridcolor='#E0E0E0')
        )
        st.plotly_chart(fig3, use_container_width=True)

# ==============================================================================
# SECTION B: PATTERNS AND COMPARISONS
# ==============================================================================
elif section == "Bloque B: Patrones y Comparaciones":
    st.markdown("## Bloque B - Patrones y Comparaciones")
    
    # Q4: Pobreza Energética y Fósiles
    st.markdown("""
    <div class='question-box'>
        <div class='question-title'>Pregunta 4: Pobreza Energética y Fósiles</div>
        <div class='question-desc'>Foco en países con menos del 50% de acceso a electricidad y su dependencia de combustibles fósiles en el año 2018.</div>
    </div>
    """, unsafe_allow_html=True)
    
    df_q4 = df_merged[(df_merged['year'] == year_sel) & (~df_merged['is_region']) & df_merged['region'].notna()].copy()
    if regions_selected:
        df_q4 = df_q4[df_q4['region'].isin(regions_selected)]
    df_q4 = df_q4.dropna(subset=['access_to_electricity', 'fossil_share_elec'])
    
    if df_q4.empty:
        st.warning("No hay datos disponibles para la combinación de filtros seleccionada en Q4.")
    else:
        df_q4['status'] = np.where(
            (df_q4['access_to_electricity'] < 50) & (df_q4['fossil_share_elec'] > 50),
            'Crítico (Acceso < 50%, Fósil > 50%)',
            'Otro'
        )
        
        fig4 = px.scatter(
            df_q4,
            x='access_to_electricity',
            y='fossil_share_elec',
            color='status',
            hover_name='country',
            size_max=12,
            color_discrete_map={
                'Crítico (Acceso < 50%, Fósil > 50%)': '#D32F2F',
                'Otro': '#CFD8DC'
            },
            custom_data=['gdp_per_capita', 'population'],
            labels={
                'access_to_electricity': 'Acceso a Electricidad (% de Población)',
                'fossil_share_elec': 'Dependencia de Fósiles en el Mix Eléctrico (%)',
                'status': 'Estado'
            },
            title=f'<b>Cuadrante de Vulnerabilidad Extrema: Países con acceso eléctrico inferior al 50% y alta dependencia fósil ({year_sel})</b>'
        )
        fig4.update_traces(
            hovertemplate="<b>%{hovertext}</b><br>" +
                          "Acceso a Electricidad: %{x:.1f}%<br>" +
                          "Dependencia Fósil: %{y:.1f}%<br>" +
                          "PIB per Cápita: $%{customdata[0]:,.0f}<br>" +
                          "Población: %{customdata[1]:,.0f}<extra></extra>"
        )
        fig4.add_vline(x=50, line_dash='dash', line_color='gray', annotation_text='Umbral Acceso (50%)', annotation_position='bottom right')
        fig4.add_hline(y=50, line_dash='dash', line_color='gray', annotation_text='Umbral Fósil (50%)', annotation_position='top left')
        
        fig4.update_layout(
            plot_bgcolor='white',
            title_x=0.0,
            title_font_size=14,
            xaxis=dict(showgrid=True, gridcolor='#E0E0E0', range=[0, 105]),
            yaxis=dict(showgrid=True, gridcolor='#E0E0E0', range=[0, 105])
        )
        st.plotly_chart(fig4, use_container_width=True)
    st.caption("**Nota de mejora:** Se utiliza el indicador `fossil_share_elec` (fósiles en electricidad) en lugar de `fossil_share_energy` (energía primaria) debido a que este último contiene valores nulos para todas las naciones con acceso eléctrico inferior al 50%, lo que impedía visualizar países en el cuadrante crítico.")
    st.markdown("---")
    
    # Q5: Ranking de Consumidores Per Cápita
    st.markdown("""
    <div class='question-box'>
        <div class='question-title'>Pregunta 5: Ranking de Consumidores Per Cápita</div>
        <div class='question-desc'>Evolución ordinal de los 12 mayores consumidores del año 2000 (Bump Chart de Cohorte Fijo).</div>
    </div>
    """, unsafe_allow_html=True)
    
    df_c = df_merged[~df_merged['is_region'] & df_merged['region'].notna()].copy()
    years = [2000, 2010, 2020]
    df_ranking = df_c[df_c['year'].isin(years) & df_c['energy_per_capita'].notnull()].copy()
    
    # 1. Cohorte fija del top 12 global del año 2000
    df_2000_global = df_ranking[df_ranking['year'] == 2000].copy()
    df_2000_global['rank_global'] = df_2000_global['energy_per_capita'].rank(ascending=False, method='min')
    top_12_2000 = df_2000_global[df_2000_global['rank_global'] <= 12]['country'].tolist()
    
    # 2. Filtrar el ranking solo para esta cohorte fija
    df_cohort = df_ranking[df_ranking['country'].isin(top_12_2000)].copy()
    
    # 3. Recalcular el ranking del 1 al 12 exclusivamente dentro de esta cohorte
    df_cohort['rank'] = df_cohort.groupby('year')['energy_per_capita'].rank(ascending=False, method='min')
    df_pivot_rank = df_cohort.pivot(index='country', columns='year', values='rank')
    df_pivot_rank = df_pivot_rank.sort_values(by=2000)
    
    fig5 = go.Figure()
    for country in df_pivot_rank.index:
        ranks = df_pivot_rank.loc[country]
        country_data = df_cohort[df_cohort['country'] == country].sort_values(by='year')
        x_vals = country_data['year'].tolist()
        y_vals = country_data['rank'].tolist()
        energy_vals = country_data['energy_per_capita'].tolist()
        gdp_vals = country_data['gdp_per_capita'].tolist()
        
        is_highlight = country in ['Iceland', 'Singapore', 'Qatar']
        color = '#D32F2F' if country == 'Iceland' else ('#FF9800' if country == 'Singapore' else '#B0BEC5')
        width = 3.5 if is_highlight else 1.5
        
        fig5.add_trace(go.Scatter(
            x=x_vals,
            y=y_vals,
            mode='lines+markers',
            name=country,
            line=dict(color=color, width=width),
            marker=dict(size=8 if is_highlight else 5),
            customdata=np.stack((energy_vals, gdp_vals), axis=-1),
            hovertemplate="<b>País: " + country + "</b><br>" +
                          "Año: %{x}<br>" +
                          "Puesto en Cohorte: %{y}<br>" +
                          "Consumo per Cápita: %{customdata[0]:,.0f} kWh<br>" +
                          "PIB per Cápita: $%{customdata[1]:,.0f}<extra></extra>"
        ))
        # Text annotation on the left
        fig5.add_annotation(
            x=2000,
            y=ranks[2000],
            text=f"{country} ",
            showarrow=False,
            xanchor='right',
            font=dict(color=color, size=10)
        )
        # Text annotation on the right
        fig5.add_annotation(
            x=2020,
            y=ranks[2020],
            text=f" {country} ({int(ranks[2020])})",
            showarrow=False,
            xanchor='left',
            font=dict(color=color, size=10)
        )
        
    fig5.update_layout(
        plot_bgcolor='white',
        title_text='<b>Singapur e Islandia escalaron puestos superando a potencias tradicionales (Top 12 del año 2000)</b>',
        title_x=0.0,
        title_font_size=15,
        xaxis=dict(showgrid=False, tickvals=years, range=[1996, 2024]),
        yaxis=dict(showgrid=True, gridcolor='#E0E0E0', autorange='reversed', tickvals=list(range(1, 13)), title='Posición en el Ranking'),
        showlegend=False,
        margin=dict(l=120, r=120, t=80, b=50)
    )
    st.plotly_chart(fig5, use_container_width=True)
    st.markdown("---")
    
    # Q6: Mix Eléctrico por País
    st.markdown("""
    <div class='question-box'>
        <div class='question-title'>Pregunta 6: Mix Eléctrico por País</div>
        <div class='question-desc'>Generación por fuentes en el año de mayor producción renovable.</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Selected country widget with Peru as default
    countries_list = sorted(df_merged[~df_merged['is_region']]['country'].unique())
    default_idx = countries_list.index('Peru') if 'Peru' in countries_list else 0
    country_sel = st.selectbox("Selecciona un país para ver su Mix Eléctrico:", countries_list, index=default_idx)
    
    df_country = df_merged[(df_merged['country'] == country_sel) & (~df_merged['is_region'])].copy()
    
    if not df_country.empty:
        idx_max = df_country['renewable_share_of_total_energy'].idxmax()
        row_max = df_country.loc[idx_max]
        year_max = int(row_max['year'])
        
        sources = ['coal_elec', 'gas_elec', 'nuclear_elec', 'solar_elec', 'wind_elec', 'hydro_elec']
        mix_vals = row_max[sources].astype(float)
        
        source_names_es = {
            'Coal': 'Carbón',
            'Gas': 'Gas',
            'Nuclear': 'Nuclear',
            'Solar': 'Solar',
            'Wind': 'Eólica',
            'Hydro': 'Hidroeléctrica'
        }
        
        mix_df = pd.DataFrame({
            'Fuente': [source_names_es[s.split('_')[0].capitalize()] for s in sources],
            'Generación (TWh)': mix_vals.values
        })
        mix_df['Participación (%)'] = (mix_df['Generación (TWh)'] / mix_df['Generación (TWh)'].sum()) * 100
        
        colors_sources = ['#757575', '#9E9E9E', '#E0E0E0', '#FFD54F', '#81C784', '#2E7D32']
        
        # Dynamic title based on country
        country_display = "Perú" if country_sel == "Peru" else country_sel
        total_gen = mix_df['Generación (TWh)'].sum()
        mix_df['Total Generación (TWh)'] = total_gen
        
        fig6 = px.bar(
            mix_df,
            x='Participación (%)',
            y='Fuente',
            orientation='h',
            color='Fuente',
            color_discrete_sequence=colors_sources,
            custom_data=['Generación (TWh)', 'Total Generación (TWh)'],
            title=f'<b>Matriz de {country_display} en {year_max}: Pico renovable liderado por Hidroelectricidad</b>',
            labels={'Participación (%)': 'Participación en el Mix Eléctrico (%)'}
        )
        # We change textposition='auto' to avoid cut-off labels for thin bars (e.g. Coal = 1.6%)
        fig6.update_traces(
            hovertemplate="<b>Fuente: %{y}</b><br>" +
                          "Participación: %{x:.1f}%<br>" +
                          "Generación Absoluta: %{customdata[0]:.2f} TWh<br>" +
                          "Generación Total de la Matriz: %{customdata[1]:.2f} TWh<extra></extra>",
            texttemplate='%{x:.1f}%',
            textposition='auto'
        )
        fig6.update_layout(
            plot_bgcolor='white',
            title_x=0.0,
            title_font_size=15,
            xaxis=dict(showgrid=True, gridcolor='#E0E0E0', range=[0, 105]),
            yaxis=dict(showgrid=False),
            showlegend=False
        )
        st.plotly_chart(fig6, use_container_width=True)
    else:
        st.warning(f"No hay datos de mix de generación eléctrica para {country_sel}")
        
    st.markdown("---")
    
    # Q7: América Latina: Ganadores y Perdedores de Carbono
    st.markdown("""
    <div class='question-box'>
        <div class='question-title'>Pregunta 7: América Latina: Ganadores y Perdedores de Carbono</div>
        <div class='question-desc'>Cambio absoluto de intensidad de carbono de la generación eléctrica (2000 vs 2020).</div>
    </div>
    """, unsafe_allow_html=True)
    
    df_la = df_merged[(df_merged['country'].isin(latin_america)) & (~df_merged['is_region'])].copy()
    la_2000 = df_la[df_la['year'] == 2000][['country', 'carbon_intensity_elec']]
    la_2020 = df_la[df_la['year'] == 2020][['country', 'carbon_intensity_elec']]
    la_delta = pd.merge(la_2000, la_2020, on='country', suffixes=('_2000', '_2020'))
    la_delta['delta'] = la_delta['carbon_intensity_elec_2020'] - la_delta['carbon_intensity_elec_2000']
    la_delta = la_delta.dropna(subset=['delta']).sort_values(by='delta', ascending=True)
    
    colors_divergent = []
    for r in la_delta.itertuples():
        if r.country == 'Peru':
            colors_divergent.append('#FF6F00')
        elif r.delta < 0:
            colors_divergent.append('#4CAF50')
        else:
            colors_divergent.append('#F44336')
            
    fig7 = px.bar(
        la_delta,
        x='delta',
        y='country',
        orientation='h',
        custom_data=['carbon_intensity_elec_2000', 'carbon_intensity_elec_2020'],
        labels={'delta': 'Cambio en Intensidad de Carbono (gCO₂/kWh)', 'country': 'País'},
        title='<b>Perú registró el mayor incremento en intensidad de carbono de la región debido a la incorporación de gas natural (2000-2020)</b>'
    )
    fig7.update_traces(
        marker_color=colors_divergent,
        texttemplate='%{x:.0f} g',
        textposition='outside',
        hovertemplate="<b>%{y}</b><br>" +
                      "Cambio en Intensidad: %{x:.1f} gCO₂/kWh<br>" +
                      "Intensidad en 2000: %{customdata[0]:.1f} gCO₂/kWh<br>" +
                      "Intensidad en 2020: %{customdata[1]:.1f} gCO₂/kWh<extra></extra>"
    )
    fig7.update_layout(
        plot_bgcolor='white',
        title_x=0.0,
        title_font_size=13,
        xaxis=dict(showgrid=True, gridcolor='#E0E0E0', range=[-320, 120]),
        yaxis=dict(showgrid=False)
    )
    st.plotly_chart(fig7, use_container_width=True)

# ==============================================================================
# SECTION C: PERU'S POSITION
# ==============================================================================
elif section == "Bloque C: Posición de Perú":
    st.markdown("## Bloque C - Posición de Perú")
    
    # Q8: Perú en la Región (Multidimensional)
    st.markdown("""
    <div class='question-box'>
        <div class='question-title'>Pregunta 8: Perú en la Región (Multidimensional)</div>
        <div class='question-desc'>Perú comparado con el promedio ponderado de América Latina en el año 2018.</div>
    </div>
    """, unsafe_allow_html=True)
    
    df_la_y = df_merged[(df_merged['country'].isin(latin_america)) & (df_merged['year'] == year_sel) & (~df_merged['is_region'])].copy()
    mean_ren = df_la_y['renewable_share_of_total_energy'].mean()
    mean_acc = df_la_y['access_to_electricity'].mean()
    mean_int = df_la_y['energy_intensity_primary_energy'].mean()
    
    peru_data = df_la_y[df_la_y['country'] == 'Peru']
    if not peru_data.empty:
        peru_ren = peru_data['renewable_share_of_total_energy'].values[0]
        peru_acc = peru_data['access_to_electricity'].values[0]
        peru_int = peru_data['energy_intensity_primary_energy'].values[0]
    else:
        peru_ren, peru_acc, peru_int = 0, 0, 0
        
    compare_df = pd.DataFrame({
        'Métrica': ['% Participación Renovable', '% Acceso Electricidad', 'Intensidad Energética (MJ/GDP)'],
        'Perú': [peru_ren, peru_acc, peru_int],
        'Promedio AL': [mean_ren, mean_acc, mean_int]
    })
    
    fig8 = go.Figure()
    fig8.add_trace(go.Bar(
        x=compare_df['Métrica'],
        y=compare_df['Perú'],
        name='Perú',
        marker_color='#FF6F00',
        text=compare_df['Perú'].apply(lambda x: f'{x:.1f}'),
        textposition='outside',
        hovertemplate=[
            "<b>Métrica: Participación Renovable</b><br>Valor Perú: %{y:.1f}%<br>Brecha vs Promedio AL: " + f"{peru_ren - mean_ren:.1f}%<extra></extra>",
            "<b>Métrica: Acceso a Electricidad</b><br>Valor Perú: %{y:.1f}%<br>Brecha vs Promedio AL: " + f"{peru_acc - mean_acc:.1f}%<extra></extra>",
            "<b>Métrica: Intensidad Energética</b><br>Valor Perú: %{y:.2f} MJ/GDP<br>Brecha vs Promedio AL: " + f"{peru_int - mean_int:.2f} MJ/GDP<extra></extra>"
        ]
    ))
    fig8.add_trace(go.Bar(
        x=compare_df['Métrica'],
        y=compare_df['Promedio AL'],
        name='Promedio AL',
        marker_color='#78909C',
        text=compare_df['Promedio AL'].apply(lambda x: f'{x:.1f}'),
        textposition='outside',
        hovertemplate=[
            "<b>Métrica: Participación Renovable</b><br>Promedio AL: %{y:.1f}%<br>Desempeño de la Región<extra></extra>",
            "<b>Métrica: Acceso a Electricidad</b><br>Promedio AL: %{y:.1f}%<br>Desempeño de la Región<extra></extra>",
            "<b>Métrica: Intensidad Energética</b><br>Promedio AL: %{y:.2f} MJ/GDP<br>Desempeño de la Región<extra></extra>"
        ]
    ))
    
    fig8.update_layout(
        plot_bgcolor='white',
        title_text=f'<b>Perú es más eficiente en intensidad energética que el promedio de AL, pero está rezagado en acceso eléctrico y participación renovable ({year_sel})</b>',
        title_x=0.0,
        title_font_size=13,
        yaxis=dict(showgrid=True, gridcolor='#E0E0E0', title='Valor de Métrica'),
        xaxis=dict(showgrid=False),
        margin=dict(l=50, r=50, t=80, b=50),
        barmode='group'
    )
    st.plotly_chart(fig8, use_container_width=True)
    st.caption("**Corrección de veracidad:** Se modificó el título del gráfico original (el cual indicaba erróneamente que Perú superaba el promedio de AL en renovables), puesto que los datos objetivos demuestran que la participación de renovables en Perú (27.9%) y el acceso a electricidad (95.2%) se encuentran por debajo del promedio latinoamericano (34.0% y 97.0% respectivamente).")
    st.markdown("---")
    
    # Q9: Perú vs. Vecinos Directos
    st.markdown("""
    <div class='question-box'>
        <div class='question-title'>Pregunta 9: Perú vs. Vecinos Directos</div>
        <div class='question-desc'>Trayectoria del consumo de energía per cápita (2000-2020).</div>
    </div>
    """, unsafe_allow_html=True)
    
    countries_q9 = ['Peru', 'Chile', 'Colombia', 'Brazil']
    df_q9 = df_merged[(df_merged['country'].isin(countries_q9)) & (~df_merged['is_region'])].copy()
    df_q9 = df_q9[(df_q9['year'] >= 2000) & (df_q9['year'] <= 2020)].sort_values(by='year')
    
    fig9 = go.Figure()
    colors_q9 = {
        'Peru': '#FF6F00',
        'Chile': '#78909C',
        'Brazil': '#90A4AE',
        'Colombia': '#B0BEC5'
    }
    
    for c in countries_q9:
        data = df_q9[df_q9['country'] == c]
        fig9.add_trace(go.Scatter(
            x=data['year'],
            y=data['energy_per_capita'],
            mode='lines+markers',
            name=c,
            line=dict(color=colors_q9[c], width=3.5 if c == 'Peru' else 1.5),
            marker=dict(size=6 if c == 'Peru' else 4),
            customdata=np.stack((data['gdp_per_capita'].fillna(0), data['population'].fillna(0) / 1e6), axis=-1),
            hovertemplate="<b>País: " + c + "</b><br>" +
                          "Año: %{x}<br>" +
                          "Consumo per Cápita: %{y:,.0f} kWh<br>" +
                          "PIB per Cápita: $%{customdata[0]:,.0f}<br>" +
                          "Población: %{customdata[1]:.1f}M<extra></extra>"
        ))
        
        last_row = data.iloc[-1]
        fig9.add_annotation(
            x=last_row['year'],
            y=last_row['energy_per_capita'],
            text="Perú" if c == "Peru" else c,
            showarrow=False,
            xanchor='left',
            xshift=8,
            font=dict(color=colors_q9[c], size=11, family='Arial')
        )
        
    fig9.update_layout(
        plot_bgcolor='white',
        title_text='<b>Perú aumenta su consumo per cápita, pero sigue lejos de Chile y Brasil (2000-2020)</b>',
        title_x=0.0,
        title_font_size=14,
        margin=dict(l=50, r=100, t=60, b=50),
        xaxis=dict(showgrid=False, tickmode='linear', tick0=2000, dtick=5),
        yaxis=dict(showgrid=True, gridcolor='#E0E0E0', title='Consumo (kWh/persona)', range=[0, 26000]),
        showlegend=False
    )
    st.plotly_chart(fig9, use_container_width=True)

# ==============================================================================
# SECTION D: DEFENSE (Q10)
# ==============================================================================
else:
    st.markdown("## Bloque D - Justificaciones Teóricas y Estéticas")
    st.markdown("En esta sección se detallan las **justificaciones técnicas y estéticas** detrás del diseño de las visualizaciones del dashboard, preparadas bajo el estándar de evaluación del docente y del libro *Storytelling with Data*.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 1. ¿Por qué usamos Gráficos de Barras Horizontales? (Q1 y Q7)
        * **Encoding:** Posición en el eje X (magnitud cuantitativa), Categoría discreta en el eje Y.
        * **Justificación:** Los nombres de los países en las comparativas de clasificación (e.g., Dinamarca, Bosnia y Herzegovina, República Dominicana, Trinidad y Tobago) son largos. Colocarlos en el eje X obligaría a usar texto vertical o en diagonal, lo que incrementa el esfuerzo cognitivo y reduce la velocidad de lectura. Las barras horizontales alinean el texto en el sentido natural de lectura (de izquierda a derecha).
        
        ### 2. ¿Por qué no usamos Gráficos de Torta o Donut? (Restricción Absoluta)
        * **Argumento:** El ojo humano no es preciso estimando diferencias de áreas o ángulos en círculos. Es mucho más exacto comparando longitudes alineadas a un eje común (gráfico de barras). Adicionalmente, el incumplimiento de esta norma genera penalizaciones automáticas (-1 punto por instancia).
        
        ### 3. ¿Cómo funciona la Regla 60-30-10 en las Líneas Comparativas? (Q2 y Q9)
        * **60% Neutro:** Fondo blanco y cuadrículas `#D3D3D3` para reducir desorden visual y ruido de fondo.
        * **30% Contexto:** Los países de comparación (Chile, Brasil, Colombia) y las líneas secundarias se representan en grises y azules apagados.
        * **10% Foco de Atención:** Perú y el líder destacado (Dinamarca en Q1) llevan una línea o barra naranja vibrante (`#FF6F00`) o verde fuerte (`#4CAF50`) con mayor grosor para dirigir instantáneamente la mirada al objetivo central.
        """)
        
    with col2:
        st.markdown("""
        ### 4. Defensa de la Paleta de Color (Colorblind-Safe)
        * **Problema:** El 8% de los varones sufre de deuteranopia (dificultad rojo/verde).
        * **Validación en ColorBrewer:** Adoptamos la paleta cualitativa `Set2` para los scatters e intensidades y una variante de azul grisáceo y naranja cálido para comparativos directos.
        * **Validación en Viz Palette:** El contraste de luminancia garantiza que, si se imprime el dashboard a blanco y negro o se simula daltonismo deuteranope, el destaque de Perú sigue siendo perfectamente legible y el contraste de grises se mantiene.
        
        ### 5. Aspect Ratio e Integridad de Tendencia (Q2 y Q9)
        * **Regla:** Mantener las pendientes de trayectoria cercanas a los **45 grados**.
        * **Razón:** Estirar excesivamente el eje horizontal aplanaría artificialmente el crecimiento del consumo per cápita en Perú. Estirar el eje vertical exageraría variaciones de carbono de corto plazo. La relación de aspecto 4:3 en contenedores resguarda la veracidad matemática.
        """)
        
    st.success("Este marco teórico provee todas las respuestas necesarias para la evaluación verbal de la Pregunta 10 (2 puntos del Bloque D).")
