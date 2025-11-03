import streamlit as st
import plotly.express as px
from datetime import datetime
from typing import Optional, Tuple
import io

import pandas as pd

from simulator import Simulator


simulator = Simulator()


def set_page_style():
	st.set_page_config(page_title="HALO Vet Dashboard", page_icon="🐶", layout="wide")
	st.markdown(
		"""
		<style>
		/* App background: layered blue gradient with subtle diagonal accent */
		.stApp {
			background: linear-gradient(135deg, #021024 0%, #013a63 40%, #0ea5e9 100%);
			color: #e6f2ff;
			font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial;
			background-attachment: fixed;
		}

		/* soft decorative diagonal stripe */
		.stApp:before {
			content: "";
			display: block;
			position: fixed;
			top: 0;
			left: 0;
			width: 100%;
			height: 100%;
			background-image: linear-gradient(120deg, rgba(255,255,255,0.02) 0%, rgba(255,255,255,0.00) 40%);
			pointer-events: none;
			z-index: 0;
		}

		/* Login card styling only */
		.login-card {
			background: rgba(255,255,255,0.06);
			backdrop-filter: blur(6px);
			padding: 1.1rem;
			border-radius: 12px;
			box-shadow: 0 10px 30px rgba(2,10,30,0.35);
			border: 1px solid rgba(255,255,255,0.04);
			z-index: 1;
			margin: 14px 0 18px 0;
		}

		/* Dashboard sections */
		.dashboard-section {
			background: transparent;
			padding: 0.3rem 0;
			margin: 6px 0 10px 0;
		}

		/* Center login card */
		.login-box { max-width:520px; margin:auto; }
		.small-muted { color: rgba(230,242,255,0.8); font-size:12px; }

		/* Headings & text colors */
		h1, h2, h3, .stHeader, .css-1d391kg { color: #e6f2ff; }
		.stMarkdown p, .stText { color: rgba(230,242,255,0.9); }

		/* Make Plotly backgrounds match card */
		.css-1d391kg .element-container, .stPlotlyChart > div {
			background: transparent !important;
		}

		/* Make default buttons white with dark text for readability on blue theme */
		.stButton > button, .stDownloadButton > button {
			background: #ffffff !important;
			color: #0f1724 !important;
			border: 1px solid rgba(2,16,36,0.15) !important;
			border-radius: 10px !important;
			box-shadow: 0 6px 14px rgba(2,10,30,0.2) !important;
		}
		.stButton > button:hover, .stDownloadButton > button:hover {
			background: #f2f6fb !important;
		}

		/* Action buttons container - center and style */
		.action-buttons-container {
			display: flex;
			justify-content: center;
			gap: 1rem;
			margin: 1rem 0;
			flex-wrap: wrap;
		}
		.action-buttons-container .stButton,
		.action-buttons-container .stDownloadButton {
			flex: 0 1 auto;
		}
		.action-buttons-container .stButton > button,
		.action-buttons-container .stDownloadButton > button {
			background: rgba(255,255,255,0.08) !important;
			color: rgba(230,242,255,0.82) !important;
			border: 1px solid rgba(255,255,255,0.15) !important;
			border-radius: 12px !important;
			box-shadow: none;
			font-weight: 600;
			font-size: 1rem;
			padding: 0.55rem 1.3rem !important;
			transition: all 0.18s ease;
		}
		.action-buttons-container .stButton > button:hover,
		.action-buttons-container .stDownloadButton > button:hover {
			border-color: rgba(255,255,255,0.45) !important;
			transform: translateY(-1px);
			box-shadow: 0 6px 18px rgba(2,10,30,0.32) !important;
			background: rgba(255,255,255,0.1) !important;
		}



		/* Metric styling */
		div[data-testid="stMetric"] {
			align-items: center;
			justify-content: center;
			text-align: center;
		}
		div[data-testid="stMetricValue"] { color: #ffffff !important; }
		div[data-testid="stMetricLabel"] p { color: #ffffff !important; }

		/* Vital summaries */
		.vital-summary {
			display: flex;
			justify-content: center;
			gap: 1.2rem;
			margin: 1.1rem 0 1.3rem 0;
			flex-wrap: wrap;
		}
		.vital-card {
			background: rgba(255,255,255,0.08);
			border: 1px solid rgba(255,255,255,0.12);
			border-radius: 14px;
			padding: 1.1rem 1.6rem;
			min-width: 165px;
			text-align: center;
			box-shadow: 0 10px 24px rgba(2,10,30,0.35);
		}
		.vital-card .label {
			display: block;
			font-size: 0.75rem;
			letter-spacing: 0.08em;
			text-transform: uppercase;
			color: rgba(230,242,255,0.72);
			margin-bottom: 0.4rem;
		}
		.vital-card .value {
			display: block;
			font-size: 2.2rem;
			font-weight: 700;
			color: #ffffff;
			line-height: 1.05;
		}
		.vital-card .unit {
			display: block;
			font-size: 0.9rem;
			color: rgba(230,242,255,0.8);
			margin-top: 0.2rem;
		}

		/* Hide Streamlit deploy banner */
		.stDeployButton, div[data-testid="stStatusWidget"] { display: none !important; }
		footer { visibility: hidden; height: 0; }

		/* Time window buttons styling - FINAL (marker-based to survive Streamlit layout) */
		/* Base (unselected) style for time-window buttons. Use general sibling to survive Streamlit wrappers */
		.tw-marker ~ div.stButton > button,
		.tw-marker ~ div .stButton > button {
			background: rgba(255,255,255,0.08) !important;
			color: rgba(230,242,255,0.82) !important;
			border: 1px solid rgba(255,255,255,0.15) !important;
			border-radius: 12px !important;
			box-shadow: none !important;
			font-weight: 600 !important;
			font-size: 0.95rem !important;
			padding: 0.55rem 1.2rem !important;
			transition: all 0.2s ease !important;
			width: 100% !important; /* Make button fill its column */
		}
		.tw-marker ~ div.stButton > button:hover,
		.tw-marker ~ div .stButton > button:hover {
			border-color: rgba(255,255,255,0.45) !important;
			transform: translateY(-1px) !important;
			box-shadow: 0 6px 18px rgba(2,10,30,0.32) !important;
			background: rgba(255,255,255,0.12) !important;
		}
		.tw-marker ~ div.stButton > button:focus,
		.tw-marker ~ div .stButton > button:focus,
		.tw-marker ~ div.stButton > button:active,
		.tw-marker ~ div .stButton > button:active {
			background: #1e7fd9 !important;
			border-color: #1565a0 !important;
			color: #ffffff !important;
			box-shadow: 0 8px 24px rgba(30, 127, 217, 0.35) !important;
		}

		/* Persistently selected state based on marker class */
		.tw-marker.selected ~ div.stButton > button,
		.tw-marker.selected ~ div .stButton > button {
			background: #1e7fd9 !important;
			border-color: #1565a0 !important;
			color: #ffffff !important;
			box-shadow: 0 8px 24px rgba(30, 127, 217, 0.35) !important;
		}
		</style>
		""",
		unsafe_allow_html=True,
	)
def plot_time_series(df: pd.DataFrame, x_col: str, y_col: str, title: str, y_range: Optional[Tuple[float, float]] = None):
	fig = px.line(df, x=x_col, y=y_col)
	fig.update_traces(line=dict(color='white', width=2))

	fig.update_layout(
		plot_bgcolor='rgba(0,0,0,0)',
		paper_bgcolor='rgba(0,0,0,0)',
		margin=dict(l=10, r=10, t=40, b=10),
		hovermode='x unified',
		title=dict(text=title, font=dict(color='white', size=16)),
		title_x=0.5,
	)

	fig.update_xaxes(title='Time', showgrid=False, zeroline=False, tickfont=dict(color='rgba(230,242,255,0.9)'),
					 title_font=dict(color='rgba(230,242,255,0.9)'))
	fig.update_yaxes(title='', gridcolor='rgba(255,255,255,0.06)', tickfont=dict(color='rgba(230,242,255,0.9)'),
					 title_font=dict(color='rgba(230,242,255,0.9)'))
	if y_range:
		fig.update_yaxes(range=y_range)
	return fig


def login_page():
	st.markdown('<div class="login-box login-card">', unsafe_allow_html=True)
	st.header('HALO — Veterinary Monitoring')
	st.write('Please sign in to access the dashboard.')
	st.markdown('### Credentials')
	st.info('Default username: `admin`  — default password: `admin`')
	with st.form('login_form'):
		username = st.text_input('Username', value='admin')
		password = st.text_input('Password', type='password', value='admin')
		submitted = st.form_submit_button('Sign in')
		if submitted:
			if username.strip() == 'admin' and password == 'admin':
				
				st.session_state.logged_in = True
				st.session_state.user = username.strip()
				
				try:
					st.rerun()
				except Exception:
					pass
				return
			else:
				st.error('Invalid username or password')


def dashboard():
	st.title('HALO — Veterinary Dashboard')
	st.markdown('Monitoring canine vitals across temperature, pulse, and respiration.')

	# Determine window selection from session state
	hours_map = {'1h': 1, '6h': 6, '24h': 24, '7d': 168}
	if 'hours' not in st.session_state or st.session_state['hours'] not in hours_map.values():
		st.session_state['hours'] = 24
	hours = st.session_state['hours']

	# Data for current selection
	df = simulator.simulate_vitals(hours)
	latest = df.iloc[-1]

	# Present vitals in summary cards
	temp_val = f"{latest.temperature_C:.1f}"
	pulse_val = f"{latest.pulse_bpm}"
	resp_val = f"{latest.respiration_bpm:.1f}"
	st.markdown(
		f"""
		<div class="dashboard-section">
			<div class="vital-summary">
				<div class="vital-card">
					<span class="label">Temperature</span>
					<span class="value">{temp_val}</span>
					<span class="unit">°C</span>
				</div>
				<div class="vital-card">
					<span class="label">Pulse</span>
					<span class="value">{pulse_val}</span>
					<span class="unit">bpm</span>
				</div>
				<div class="vital-card">
					<span class="label">Respiration</span>
					<span class="value">{resp_val}</span>
					<span class="unit">bpm</span>
				</div>
			</div>
		</div>
		""",
		unsafe_allow_html=True,
	)

	# Charts
	st.markdown('<div class="dashboard-section">', unsafe_allow_html=True)
	c1, c2, c3 = st.columns(3)
	with c1:
		fig_t = plot_time_series(df, 'timestamp', 'temperature_C', 'Temperature (°C)', y_range=(36.5, 41))
		st.plotly_chart(fig_t, use_container_width=True)
	with c2:
		fig_p = plot_time_series(df, 'timestamp', 'pulse_bpm', 'Pulse (BPM)', y_range=(40, 200))
		st.plotly_chart(fig_p, use_container_width=True)
	with c3:
		fig_r = plot_time_series(df, 'timestamp', 'respiration_bpm', 'Respiration (bpm)', y_range=(6, 80))
		st.plotly_chart(fig_r, use_container_width=True)
	st.markdown('</div>', unsafe_allow_html=True)

	# History window control below charts
	st.markdown('<div class="dashboard-section">', unsafe_allow_html=True)
	_, c1, c2, c3, c4, _ = st.columns([1.5, 1, 1, 1, 1, 1.5])

	def set_hours(h):
		st.session_state['hours'] = h

	with c1:
		st.markdown(f'<span class="tw-marker {"selected" if hours == 1 else ""}"></span>', unsafe_allow_html=True)
		st.button('1h', key='tw_1h', on_click=set_hours, args=(1,), use_container_width=True)
	with c2:
		st.markdown(f'<span class="tw-marker {"selected" if hours == 6 else ""}"></span>', unsafe_allow_html=True)
		st.button('6h', key='tw_6h', on_click=set_hours, args=(6,), use_container_width=True)
	with c3:
		st.markdown(f'<span class="tw-marker {"selected" if hours == 24 else ""}"></span>', unsafe_allow_html=True)
		st.button('24h', key='tw_24h', on_click=set_hours, args=(24,), use_container_width=True)
	with c4:
		st.markdown(f'<span class="tw-marker {"selected" if hours == 168 else ""}"></span>', unsafe_allow_html=True)
		st.button('7d', key='tw_7d', on_click=set_hours, args=(168,), use_container_width=True)
	st.markdown('</div>', unsafe_allow_html=True)
	
	# Action buttons - Refresh Data and Download CSV (centered)
	_, a1, a2, _ = st.columns([1, 0.5, 0.5, 1])
	with a1:
		if st.button('Refresh Data', use_container_width=True):
			st.session_state['last_refresh'] = datetime.now().timestamp()
	with a2:
		csv = df.to_csv(index=False)
		b = io.BytesIO()
		b.write(csv.encode())
		b.seek(0)
		st.download_button('Download CSV', b, file_name='vitals.csv', mime='text/csv', use_container_width=True)


def main():
	set_page_style()
	if 'logged_in' not in st.session_state:
		st.session_state.logged_in = False

	if not st.session_state.logged_in:
		login_page()
	else:
		dashboard()


if __name__ == '__main__':
	main()

