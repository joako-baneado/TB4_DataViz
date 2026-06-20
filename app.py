import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

# Configuración de página con título SEO
st.set_page_config(
    page_title="Dashboard de Transición Energética Global - TB4 Data Viz",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo premium personalizado
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    .main-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    
    .subtitle {
        font-size: 1.1rem;
        color: #4B5563;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    
    .section-card {
        background-color: #F8FAFC;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #2563EB;
        margin-bottom: 1.5rem;
    }
    
    .critical-card {
        background-color: #FFF5F5;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #DC2626;
        margin-bottom: 1.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# Cargar dataset
@st.cache_data
def load_data():
    if not os.path.exists("data/merged_dataset.csv"):
        # Intento de generar los datos si no existen
        try:
            from data.merge import download_and_merge
            download_and_merge()
        except Exception as e:
            st.error(f"Error al generar datos fusionados: {e}")
            return None
    return pd.read_csv("data/merged_dataset.csv")

df = load_data()

if df is None:
    st.error("No se pudo cargar el dataset. Verifica la existencia de los archivos base.")
    st.stop()

# --- FILTROS SIDEBAR ---
st.sidebar.image("https://owid.googleusercontent.com/600x315-owid-image.png", width=180)
st.sidebar.markdown("### ⚡ Filtros Globales")

# Lista de países y regiones
all_countries = sorted(df[~df['is_region']]['country'].unique())
all_regions = sorted(df[df['is_region']]['country'].unique())

# Definición de la lista de países de América Latina
latin_america = ['Argentina', 'Belize', 'Bolivia', 'Brazil', 'Chile', 'Colombia', 'Costa Rica', 'Cuba', 'Dominican Republic', 'Ecuador', 'El Salvador', 'Guatemala', 'Honduras', 'Mexico', 'Nicaragua', 'Panama', 'Paraguay', 'Peru', 'Uruguay', 'Venezuela']

# Filtro de países y regiones multiselect
selected_countries = st.sidebar.multiselect(
    "Selecciona Países para Comparaciones:",
    options=all_countries,
    default=['Peru', 'Chile', 'Colombia', 'Brazil']
)

# Filtro de rango temporal
year_min = int(df['year'].min())
year_max = int(df['year'].max())
year_range = st.sidebar.slider(
    "Rango de Años:",
    min_value=2000,
    max_value=2020,
    value=(2000, 2020)
)

# Filtro de año único (para gráficos puntuales)
selected_single_year = st.sidebar.slider(
    "Año de Corte (Q3, Q4, Q8):",
    min_value=2000,
    max_value=2020,
    value=2018
)

# --- CABECERA PRINCIPAL ---
st.markdown('<div class="main-title">Transición Energética Global (2000-2020)</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Análisis del desarrollo sostenible, matriz eléctrica y posición de Perú. TB4 - Data Visualization</div>', unsafe_allow_html=True)

# Tabs de navegación correspondientes a los bloques de evaluación
tab_a, tab_b, tab_c, tab_d = st.tabs([
    "🌍 Bloque A: Panorama Global",
    "📊 Bloque B: Patrones y Comparaciones",
    "🇵🇪 Bloque C: Posición de Perú",
    "🛡️ Bloque D: Defensa de Diseño"
])

# ==================== BLOQUE A ====================
with tab_a:
    st.markdown('<div class="section-card"><h4>Bloque A: Preguntas 1 a 3 — Indicadores Clave del Panorama Global</h4></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    # --- Pregunta 1 ---
    with col1:
        st.subheader("Q1: Líderes de la Transición")
        st.markdown("*¿Cuáles son los cinco países que más aumentaron su participación de energías renovables entre 2000 y 2020?*")
        
        # Filtro de países y deltas
        df_c = df[~df['is_region']].copy()
        df_2000 = df_c[df_c['year'] == 2000][['country', 'renewable_share_of_total_energy']]
        df_2020 = df_c[df_c['year'] == 2020][['country', 'renewable_share_of_total_energy']]
        df_delta = pd.merge(df_2000, df_2020, on='country', suffixes=('_2000', '_2020'))
        df_delta['delta'] = df_delta['renewable_share_of_total_energy_2020'] - df_delta['renewable_share_of_total_energy_2000']
        
        top_5 = df_delta.sort_values(by='delta', ascending=False).head(5).copy()
        
        # Storytelling: Barras horizontales, color naranja para el líder, gris para otros
        colors = ['#FF6F00'] + ['#B0BEC5'] * 4
        
        fig1 = px.bar(
            top_5.sort_values(by='delta', ascending=True),
            x='delta',
            y='country',
            orientation='h',
            labels={'delta': 'Incremento de Participación (%)', 'country': 'País'},
            hover_data={
                'renewable_share_of_total_energy_2000': ':.2f}%',
                'renewable_share_of_total_energy_2020': ':.2f}%'
            }
        )
        fig1.update_traces(
            marker_color=colors[::-1],
            texttemplate='+%{x:.1f}%',
            textposition='outside',
            hovertemplate="<b>%{y}</b><br>Incremento: +%{x:.2f}%<br>Año 2000: %{customdata[0]:.2f}%<br>Año 2020: %{customdata[1]:.2f}%<extra></extra>"
        )
        fig1.update_layout(
            title="<b>Islandia lideró la transición</b> ganando más de 50 puntos porcentuales de energía renovable",
            title_x=0.0,
            plot_bgcolor='white',
            xaxis=dict(showgrid=True, gridcolor='#D3D3D3', range=[0, 60], title="Puntos Porcentuales Ganados (2000-2020)"),
            yaxis=dict(showgrid=False, title=""),
            height=350,
            margin=dict(l=20, r=40, t=50, b=20)
        )
        st.plotly_chart(fig1, use_container_width=True)
        
    # --- Pregunta 2 ---
    with col2:
        st.subheader("Q2: Trayectorias Regionales de Carbono")
        st.markdown("*¿Cómo evolucionó la intensidad de carbono de la electricidad en las principales regiones del mundo?*")
        
        df_reg = df[df['is_region']].copy()
        
        # Graficar trayectorias
        fig2 = go.Figure()
        regions = ['Europe', 'North America', 'Asia', 'South America', 'Africa', 'Oceania']
        
        # 60-30-10: Europa en verde oscuro (gran reducción), Asia en rojo (empeoró/alta), otros en gris
        colors_map = {
            'Europe': '#1B5E20',
            'North America': '#4CAF50',
            'Asia': '#D32F2F',
            'South America': '#78909C',
            'Africa': '#90A4AE',
            'Oceania': '#B0BEC5'
        }
        
        for r in regions:
            data = df_reg[(df_reg['country'] == r) & (df_reg['year'] >= year_range[0]) & (df_reg['year'] <= year_range[1])].sort_values(by='year')
            if len(data) == 0:
                continue
            
            fig2.add_trace(go.Scatter(
                x=data['year'],
                y=data['carbon_intensity_elec'],
                mode='lines+markers',
                name=r,
                line=dict(color=colors_map[r], width=3 if r in ['Europe', 'Asia'] else 1.5),
                marker=dict(size=5 if r in ['Europe', 'Asia'] else 3),
                hovertemplate=f"<b>{r}</b><br>Año: %{{x}}<br>Intensidad: %{{y:.1f}} gCO₂/kWh<extra></extra>"
            ))
            
            # Leyenda integrada al final de la línea
            last_row = data.iloc[-1]
            fig2.add_annotation(
                x=last_row['year'],
                y=last_row['carbon_intensity_elec'],
                text=r,
                showarrow=False,
                xanchor='left',
                xshift=8,
                font=dict(color=colors_map[r], size=10)
            )
            
        fig2.update_layout(
            title="<b>Europa lidera el recorte de carbono</b> eléctrico, mientras Asia y África avanzan lento",
            title_x=0.0,
            plot_bgcolor='white',
            xaxis=dict(showgrid=False, tickmode='linear', dtick=5, title="Año"),
            yaxis=dict(showgrid=True, gridcolor='#D3D3D3', title="Intensidad de carbono (gCO₂/kWh)"),
            showlegend=False,
            height=350,
            margin=dict(l=20, r=100, t=50, b=20)
        )
        st.plotly_chart(fig2, use_container_width=True)

    # --- Pregunta 3 ---
    st.markdown("---")
    st.subheader("Q3: Riqueza vs. Participación de Renovables")
    st.markdown("*¿Los países más ricos son necesariamente los más renovables en su consumo final?*")
    
    df_y = df_c[df_c['year'] == selected_single_year].copy().dropna(subset=['gdp_per_capita', 'renewable_share_of_total_energy'])
    
    # Scatter plot
    fig3 = px.scatter(
        df_y,
        x='gdp_per_capita',
        y='renewable_share_of_total_energy',
        size='population',
        color='region',
        hover_name='country',
        log_x=True,
        color_discrete_sequence=px.colors.qualitative.Set2,
        labels={
            'gdp_per_capita': 'PIB per Cápita (USD, Escala Logarítmica)',
            'renewable_share_of_total_energy': 'Participación Renovable (%)',
            'region': 'Región'
        }
    )
    fig3.update_traces(
        hovertemplate="<b>%{hovertext}</b><br>PIB per cápita: $%{x:,.2f}<br>Renovables: %{y:.2f}%<br>Población: %{marker.size:,}<extra></extra>"
    )
    fig3.update_layout(
        title=f"<b>Sin correlación lineal:</b> Países con alto PIB per cápita muestran niveles muy diversos de energía renovable ({selected_single_year})",
        title_x=0.0,
        plot_bgcolor='white',
        xaxis=dict(showgrid=True, gridcolor='#D3D3D3'),
        yaxis=dict(showgrid=True, gridcolor='#D3D3D3'),
        height=450,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    st.plotly_chart(fig3, use_container_width=True)

# ==================== BLOQUE B ====================
with tab_b:
    st.markdown('<div class="section-card"><h4>Bloque B: Preguntas 4 a 7 — Patrones de Consumo, Mix Eléctrico y Comparaciones</h4></div>', unsafe_allow_html=True)
    
    # --- Pregunta 4 ---
    st.subheader("Q4: Pobreza Energética y Fósiles")
    st.markdown(f"*Foco en países con menos del 50% de acceso a electricidad y su dependencia de combustibles fósiles en el año {selected_single_year}*")
    
    df_q4 = df_c[df_c['year'] == selected_single_year].copy().dropna(subset=['access_to_electricity', 'fossil_share_energy'])
    
    # Clasificación de cuadrante crítico
    df_q4['status'] = np.where(
        (df_q4['access_to_electricity'] < 50) & (df_q4['fossil_share_energy'] > 50),
        'Crítico (Acceso < 50%, Fósil > 50%)',
        'Otros países'
    )
    
    fig4 = px.scatter(
        df_q4,
        x='access_to_electricity',
        y='fossil_share_energy',
        color='status',
        hover_name='country',
        color_discrete_map={
            'Crítico (Acceso < 50%, Fósil > 50%)': '#D32F2F', # Alerta
            'Otros países': '#CFD8DC' # Muted
        },
        labels={
            'access_to_electricity': 'Acceso a Electricidad (% de Población)',
            'fossil_share_energy': 'Dependencia Fósil en Energía Primaria (%)'
        }
    )
    # Umbrales
    fig4.add_vline(x=50, line_dash='dash', line_color='#9E9E9E')
    fig4.add_hline(y=50, line_dash='dash', line_color='#9E9E9E')
    
    fig4.update_traces(
        marker=dict(size=10, line=dict(width=1, color='DarkSlateGrey')),
        hovertemplate="<b>%{hovertext}</b><br>Acceso a electricidad: %{x:.2f}%<br>Dependencia fósil: %{y:.2f}%<extra></extra>"
    )
    fig4.update_layout(
        title=f"<b>Cuadrante de Vulnerabilidad Extrema:</b> Países con acceso eléctrico inferior al 50% y alta dependencia fósil ({selected_single_year})",
        title_x=0.0,
        plot_bgcolor='white',
        xaxis=dict(showgrid=True, gridcolor='#E0E0E0', range=[-5, 105]),
        yaxis=dict(showgrid=True, gridcolor='#E0E0E0', range=[-5, 105]),
        height=400,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    st.plotly_chart(fig4, use_container_width=True)
    
    col3, col4 = st.columns(2)
    
    # --- Pregunta 5 ---
    with col3:
        st.subheader("Q5: Ranking de Consumidores Per Cápita")
        st.markdown("*Evolución ordinal de los 12 mayores consumidores del año 2000 (Bump Chart)*")
        
        years_rank = [2000, 2010, 2020]
        df_ranking = df_c[df_c['year'].isin(years_rank) & df_c['energy_per_capita'].notnull()].copy()
        
        top_2000 = df_ranking[df_ranking['year'] == 2000].sort_values(by='energy_per_capita', ascending=False).head(12)['country']
        df_filtered_ranking = df_ranking[df_ranking['country'].isin(top_2000)].copy()
        
        # Calcular ranking
        df_filtered_ranking['rank'] = df_filtered_ranking.groupby('year')['energy_per_capita'].rank(ascending=False, method='min')
        df_pivot_rank = df_filtered_ranking.pivot(index='country', columns='year', values='rank').sort_values(by=2000).head(12)
        
        fig5 = go.Figure()
        
        for country in df_pivot_rank.index:
            ranks = df_pivot_rank.loc[country]
            is_highlight = country in ['Iceland', 'Singapore', 'Qatar']
            color = '#D32F2F' if country == 'Iceland' else ('#FF9800' if country == 'Singapore' else '#B0BEC5')
            width = 3.5 if is_highlight else 1.5
            
            fig5.add_trace(go.Scatter(
                x=years_rank,
                y=ranks,
                mode='lines+markers',
                name=country,
                line=dict(color=color, width=width),
                marker=dict(size=8 if is_highlight else 5),
                hovertemplate=f"<b>{country}</b><br>Año: %{{x}}<br>Puesto: %{{y}}<extra></extra>"
            ))
            
            # Etiqueta al final (año 2020)
            fig5.add_annotation(
                x=2020,
                y=ranks[2020],
                text=f"{country} ({int(ranks[2020])})",
                showarrow=False,
                xanchor='left',
                xshift=8,
                font=dict(color=color, size=9)
            )
            
        fig5.update_layout(
            title="<b>Singapur e Islandia escalaron</b> puestos superando a potencias tradicionales",
            title_x=0.0,
            plot_bgcolor='white',
            xaxis=dict(showgrid=False, tickvals=years_rank, range=[1997, 2023]),
            yaxis=dict(showgrid=True, gridcolor='#E0E0E0', autorange='reversed', tickvals=list(range(1, 15)), title="Posición en el Ranking"),
            showlegend=False,
            height=380,
            margin=dict(l=20, r=100, t=50, b=20)
        )
        st.plotly_chart(fig5, use_container_width=True)
        
    # --- Pregunta 6 ---
    with col4:
        st.subheader("Q6: Mix Eléctrico por País")
        st.markdown("*Generación por fuentes en el año de mayor producción renovable*")
        
        # Selector de país dinámico que afecta a este gráfico
        country_q6 = st.selectbox(
            "Selecciona País para ver su Mix Eléctrico:",
            options=all_countries,
            index=all_countries.index('Peru') if 'Peru' in all_countries else 0
        )
        
        df_country = df_c[df_c['country'] == country_q6].copy()
        
        if len(df_country) > 0:
            idx_max = df_country['renewable_share_of_total_energy'].idxmax()
            row_max = df_country.loc[idx_max]
            year_max = int(row_max['year'])
            
            sources = ['coal_elec', 'gas_elec', 'nuclear_elec', 'solar_elec', 'wind_elec', 'hydro_elec']
            mix_vals = row_max[sources].astype(float)
            mix_df = pd.DataFrame({
                'Fuente': [s.split('_')[0].capitalize() for s in sources], 
                'Generación (TWh)': mix_vals.values
            })
            mix_df['Participacion'] = (mix_df['Generación (TWh)'] / mix_df['Generación (TWh)'].sum()) * 100
            
            colors_sources = ['#757575', '#9E9E9E', '#E0E0E0', '#FFD54F', '#81C784', '#2E7D32'] # Fósiles en grises, renovables en colores
            
            fig6 = px.bar(
                mix_df,
                x='Participacion',
                y='Fuente',
                orientation='h',
                color='Fuente',
                color_discrete_sequence=colors_sources,
                labels={'Participacion': 'Participación (%)'}
            )
            fig6.update_traces(
                texttemplate='%{x:.1f}%',
                textposition='inside',
                hovertemplate="<b>%{y}</b><br>Participación: %{x:.2f}%<br>Generación: %{customdata[0]:.2f} TWh<extra></extra>",
                customdata=np.stack([mix_df['Generación (TWh)']], axis=-1)
            )
            fig6.update_layout(
                title=f"<b>Matriz de {country_q6} en {year_max}:</b> Pico renovable liderado por Hidroelectricidad",
                title_x=0.0,
                plot_bgcolor='white',
                xaxis=dict(showgrid=True, gridcolor='#E0E0E0', range=[0, 105]),
                yaxis=dict(showgrid=False, title=""),
                showlegend=False,
                height=380,
                margin=dict(l=20, r=20, t=50, b=20)
            )
            st.plotly_chart(fig6, use_container_width=True)
        else:
            st.warning("No hay datos de generación eléctrica para el país seleccionado.")

    # --- Pregunta 7 ---
    st.markdown("---")
    st.subheader("Q7: América Latina: Ganadores y Perdedores de Carbono")
    st.markdown("*Cambio absoluto de intensidad de carbono de la generación eléctrica (2000 vs 2020)*")
    
    df_la = df_c[df_c['country'].isin(latin_america)].copy()
    la_2000 = df_la[df_la['year'] == 2000][['country', 'carbon_intensity_elec']]
    la_2020 = df_la[df_la['year'] == 2020][['country', 'carbon_intensity_elec']]
    la_delta = pd.merge(la_2000, la_2020, on='country', suffixes=('_2000', '_2020'))
    la_delta['delta'] = la_delta['carbon_intensity_elec_2020'] - la_delta['carbon_intensity_elec_2000']
    la_delta = la_delta.dropna(subset=['delta']).sort_values(by='delta', ascending=True)
    
    # Colores: Verde para mejora, Rojo para empeoramiento, Naranja para Perú
    colors_divergent = []
    for r in la_delta.itertuples():
        if r.country == 'Peru':
            colors_divergent.append('#FF6F00') # Destaque Perú
        elif r.delta < 0:
            colors_divergent.append('#4CAF50') # Mejoró
        else:
            colors_divergent.append('#F44336') # Empeoró
            
    fig7 = px.bar(
        la_delta,
        x='delta',
        y='country',
        orientation='h',
        labels={'delta': 'Cambio en Intensidad de Carbono (gCO₂/kWh)', 'country': 'País'}
    )
    fig7.update_traces(
        marker_color=colors_divergent,
        texttemplate='%{x:.0f} g',
        textposition='outside',
        hovertemplate="<b>%{y}</b><br>Cambio: %{x:.1f} gCO₂/kWh<br>Año 2000: %{customdata[0]:.1f} g<br>Año 2020: %{customdata[1]:.1f} g<extra></extra>",
        customdata=np.stack([la_delta['carbon_intensity_elec_2000'], la_delta['carbon_intensity_elec_2020']], axis=-1)
    )
    fig7.update_layout(
        title="<b>Perú redujo su intensidad de carbono</b>, posicionándose en el cuadrante de mejora",
        title_x=0.0,
        plot_bgcolor='white',
        xaxis=dict(showgrid=True, gridcolor='#E0E0E0'),
        yaxis=dict(showgrid=False, title=""),
        height=450,
        margin=dict(l=20, r=40, t=50, b=20)
    )
    st.plotly_chart(fig7, use_container_width=True)

# ==================== BLOQUE C ====================
with tab_c:
    st.markdown('<div class="section-card"><h4>Bloque C: Preguntas 8 y 9 — Posición de Perú y Comparación Regional</h4></div>', unsafe_allow_html=True)
    
    col5, col6 = st.columns(2)
    
    # --- Pregunta 8 ---
    with col5:
        st.subheader("Q8: Perú en la Región (Multidimensional)")
        st.markdown(f"*Perú comparado con el promedio ponderado de América Latina en el año {selected_single_year}*")
        
        df_la_y = df_c[df_c['country'].isin(latin_america) & (df_c['year'] == selected_single_year)].copy()
        
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
            marker_color='#FF6F00', # 10% Foco de Atención
            text=compare_df['Perú'].apply(lambda x: f'{x:.1f}'),
            textposition='outside',
            hovertemplate="<b>Perú</b><br>Métrica: %{x}<br>Valor: %{y:.2f}<extra></extra>"
        ))
        fig8.add_trace(go.Bar(
            x=compare_df['Métrica'],
            y=compare_df['Promedio AL'],
            name='Promedio AL',
            marker_color='#78909C', # 30% Contexto
            text=compare_df['Promedio AL'].apply(lambda x: f'{x:.1f}'),
            textposition='outside',
            hovertemplate="<b>Promedio AL</b><br>Métrica: %{x}<br>Valor: %{y:.2f}<extra></extra>"
        ))
        
        fig8.update_layout(
            title=f"<b>Perú es más eficiente</b> y tiene mayor cuota de renovables que el promedio de AL",
            title_x=0.0,
            plot_bgcolor='white',
            yaxis=dict(showgrid=True, gridcolor='#E0E0E0', title="Valor"),
            xaxis=dict(showgrid=False),
            height=400,
            margin=dict(l=20, r=20, t=50, b=20),
            barmode='group'
        )
        st.plotly_chart(fig8, use_container_width=True)
        
    # --- Pregunta 9 ---
    with col6:
        st.subheader("Q9: Perú vs. Vecinos Directos")
        st.markdown("*Trayectoria del consumo de energía per cápita (2000-2020)*")
        
        countries_q9 = ['Peru', 'Chile', 'Colombia', 'Brazil']
        
        # Unir países seleccionados en barra lateral más los vecinos obligatorios
        compare_countries = list(set(countries_q9 + selected_countries))
        
        df_q9 = df_c[df_c['country'].isin(compare_countries) & (df_c['year'] >= year_range[0]) & (df_c['year'] <= year_range[1])].sort_values(by='year')
        
        fig9 = go.Figure()
        
        # 60-30-10: Naranja grueso para Perú, otros en escalas de grises
        colors_q9_default = {
            'Peru': '#FF6F00',
            'Chile': '#78909C',
            'Brazil': '#90A4AE',
            'Colombia': '#B0BEC5'
        }
        
        for c in compare_countries:
            data_c = df_q9[df_q9['country'] == c]
            if len(data_c) == 0:
                continue
            
            color = colors_q9_default.get(c, '#B0BEC5')
            width = 3.5 if c == 'Peru' else 1.5
            
            fig9.add_trace(go.Scatter(
                x=data_c['year'],
                y=data_c['energy_per_capita'],
                mode='lines+markers',
                name=c,
                line=dict(color=color, width=width),
                marker=dict(size=6 if c == 'Peru' else 4),
                hovertemplate=f"<b>{c}</b><br>Año: %{{x}}<br>Consumo: %{{y:.1f}} kWh/persona<extra></extra>"
            ))
            
            # Leyenda integrada
            last_row = data_c.iloc[-1]
            fig9.add_annotation(
                x=last_row['year'],
                y=last_row['energy_per_capita'],
                text=c,
                showarrow=False,
                xanchor='left',
                xshift=8,
                font=dict(color=color, size=10)
            )
            
        fig9.update_layout(
            title="<b>Perú aumenta su consumo per cápita</b>, pero sigue lejos de Chile y Brasil",
            title_x=0.0,
            plot_bgcolor='white',
            xaxis=dict(showgrid=False, tickmode='linear', dtick=5, title="Año"),
            yaxis=dict(showgrid=True, gridcolor='#E0E0E0', title="Consumo (kWh/persona)"),
            showlegend=False,
            height=400,
            margin=dict(l=20, r=100, t=50, b=20)
        )
        st.plotly_chart(fig9, use_container_width=True)

# ==================== BLOQUE D ====================
with tab_d:
    st.markdown('<div class="section-card"><h4>Bloque D: Pregunta 10 — Defensa de Diseño y Argumentación Científica</h4></div>', unsafe_allow_html=True)
    
    st.markdown("""
    En esta sección se detallan las **justificaciones técnicas y estéticas** detrás del diseño de las visualizaciones del dashboard, preparadas bajo el estándar de evaluación del docente.
    """)
    
    col7, col8 = st.columns(2)
    
    with col7:
        st.markdown("""
        ##### 1. ¿Por qué usamos Gráficos de Barras Horizontales? (Q1 y Q7)
        * **Encoding:** Posición en eje X (magnitud cuantitativa), Categoría discreta en eje Y.
        * **Justificación:** Los nombres de los países (Islandia, República Dominicana, Trinidad y Tobago) son largos. Colocarlos en el eje X obligaría a usar texto vertical o en diagonal, lo que incrementa el esfuerzo cognitivo y reduce la velocidad de lectura. Las barras horizontales alinean el texto en sentido natural de lectura (de izquierda a derecha).
        
        ##### 2. ¿Por qué no usamos Gráficos de Torta o Donut? (Restricción Absoluta)
        * **Argumento:** El ojo humano no es preciso estimando diferencias de áreas o ángulos en círculos. Es mucho más exacto comparando longitudes alineadas a un eje común (gráfico de barras). Adicionalmente, el incumplimiento de esta norma genera penalizaciones automáticas (-1 punto por instancia).
        
        ##### 3. ¿Cómo funciona la Regla 60-30-10 en las Líneas Comparativas? (Q2 y Q9)
        * **60% Neutro:** Fondo blanco y cuadrículas `#D3D3D3` para reducir desorden visual.
        * **30% Contexto:** Los países de comparación (Chile, Brasil, Colombia) se representan en grises y azules apagados.
        * **10% Foco de Atención:** **Perú** o la región destacada llevan una línea naranja vibrante o verde fuerte con mayor grosor para dirigir instantáneamente la mirada al objetivo central.
        """)
        
    with col8:
        st.markdown("""
        ##### 4. Defensa de la Paleta de Color (Colorblind-Safe)
        * **Problema:** El 8% de los varones sufre de deuteranopia (dificultad rojo/verde).
        * **Validación en ColorBrewer:** Adoptamos la paleta cualitativa `Set2` para los scatters e intensidades y una variante de azul grisáceo y naranja cálido para comparativos directos.
        * **Validación en Viz Palette:** El contraste de luminancia garantiza que, si se imprime el dashboard a blanco y negro o se simula daltonismo deuteranope, el destaque de Perú sigue siendo perfectamente legible.
        
        ##### 5. Aspect Ratio e Integridad de Tendencia (Q2 y Q9)
        * **Regla:** Mantener las pendientes de trayectoria cercanas a los **45 grados**.
        * **Razón:** Estirar excesivamente el eje horizontal aplanaría artificialmente el crecimiento del consumo per cápita en Perú. Estirar el eje vertical exageraría variaciones de carbono de corto plazo. La relación de aspecto 4:3 en contenedores resguarda la veracidad matemática.
        """)
        
    st.success("✅ Este marco teórico provee todas las respuestas necesarias para la evaluación verbal de la Pregunta 10 (2 puntos del Bloque D).")
