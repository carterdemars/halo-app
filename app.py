import streamlit as st
import streamlit.components.v1 as components
import plotly.express as px
from typing import Optional, Tuple
import html
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

		/* Login card styling */
		div[data-testid="stVerticalBlock"] > div[style*="flex-direction: column;"] > div[data-testid="stVerticalBlock"] {
			border: 1px solid rgba(255, 255, 255, 0.1);
			border-radius: 16px;
			padding: 2rem 2.4rem;
			background: rgba(255,255,255,0.07);
			backdrop-filter: blur(12px);
			box-shadow: 0 16px 40px rgba(2,10,30,0.35);
		}
		.st-emotion-cache-uf99v8 {
			background: transparent !important;
		}
		.login-card .centered-title {
			margin: 0 0 1.2rem 0;
		}
		.login-card .centered-title h1 {
			font-size: 2rem;
		}

		/* Dashboard sections */
		.dashboard-section {
			background: transparent;
			padding: 0.3rem 0;
			margin: 6px 0 10px 0;
		}

		.small-muted { color: rgba(230,242,255,0.8); font-size:12px; }

		/* Centered title block for login and dashboard hero area */
		.centered-title {
			text-align: center;
			margin: 0.5rem auto 1.6rem auto;
		}
		.centered-title h1 {
			margin: 0;
			font-size: 2.4rem;
			font-weight: 700;
			letter-spacing: 0.01em;
			color: #e6f2ff;
		}
		.centered-title p {
			margin: 0.35rem 0 0 0;
			color: rgba(230,242,255,0.85);
			font-size: 1rem;
		}

		/* Headings & text colors */
		h1, h2, h3, .stHeader, .css-1d391kg { color: #e6f2ff; }
		.stMarkdown p, .stText { color: rgba(230,242,255,0.9); }
		/* Hide Streamlit anchor links on headings */
		.stMarkdown h1 a,
		.stMarkdown h2 a,
		.stMarkdown h3 a {
			display: none !important;
		}

		/* Make Plotly backgrounds match card */
		.css-1d391kg .element-container, .stPlotlyChart > div {
			background: transparent !important;
		}

		/* Login card primary action */
		.login-card button {
			background: #ffffff !important;
			color: #0f1724 !important;
			border: 1px solid rgba(2,16,36,0.15) !important;
			border-radius: 10px !important;
			box-shadow: 0 6px 14px rgba(2,10,30,0.2) !important;
		}
		.login-card button:hover {
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

		/* Time window buttons styling - Direct CSS targeting */
		/* Target all buttons in the time window section */
		[data-testid="stButton"] button,
		[data-testid="stButton"] button[data-testid="baseButton-secondary"] {
			background: rgba(255,255,255,0.08) !important;
			color: rgba(230,242,255,0.82) !important;
			border: 1px solid rgba(255,255,255,0.15) !important;
			border-radius: 12px !important;
			box-shadow: none !important;
			font-weight: 600 !important;
			font-size: 0.95rem !important;
			padding: 0.55rem 1.2rem !important;
			transition: all 0.2s ease !important;
		}
		[data-testid="stButton"] button:hover {
			border-color: rgba(255,255,255,0.45) !important;
			transform: translateY(-1px) !important;
			box-shadow: 0 6px 18px rgba(2,10,30,0.32) !important;
			background: rgba(255,255,255,0.12) !important;
		}
		/* Primary (selected) button styling */
		[data-testid="stButton"] button[data-testid="baseButton-primary"],
		[data-testid="stButton"] button[kind="primary"] {
			background: #1e7fd9 !important;
			border-color: #1565a0 !important;
			color: #ffffff !important;
			box-shadow: 0 8px 24px rgba(30, 127, 217, 0.35) !important;
		}

		/* Download button styling */
		[data-testid="stDownloadButton"] button {
			background: rgba(255,255,255,0.08) !important;
			color: rgba(230,242,255,0.82) !important;
			border: 1px solid rgba(255,255,255,0.15) !important;
			border-radius: 12px !important;
			box-shadow: none !important;
			font-weight: 600 !important;
			font-size: 0.95rem !important;
			padding: 0.55rem 1.2rem !important;
			transition: all 0.2s ease !important;
		}
		[data-testid="stDownloadButton"] button:hover {
			border-color: rgba(255,255,255,0.45) !important;
			transform: translateY(-1px) !important;
			box-shadow: 0 6px 18px rgba(2,10,30,0.32) !important;
			background: rgba(255,255,255,0.12) !important;
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


def render_centered_title(title: str, subtitle: Optional[str] = None):
	title_html = html.escape(title)
	subtitle_html = f"<p>{html.escape(subtitle)}</p>" if subtitle else ""
	st.markdown(
		f"""
		<div class="centered-title">
			<h1>{title_html}</h1>
			{subtitle_html}
		</div>
		""",
		unsafe_allow_html=True,
	)


def login_page():
	_, col, _ = st.columns([1, 1.5, 1])
	with col:
		with st.container(border=True):
			render_centered_title('HALO - Veterinary Dashboard', 'Please sign in to access the dashboard.')
			with st.form('login_form'):
				username = st.text_input('Username', value='admin', key='login_username')
				password = st.text_input('Password', type='password', value='admin', key='login_password')
				submitted = st.form_submit_button('Sign in', width='stretch')
				if submitted:
					if username.strip() == 'admin' and password == 'admin':
						st.session_state.logged_in = True
						st.session_state.user = username.strip()
						st.rerun()
					else:
						st.error('Invalid username or password')


def dashboard():
	render_centered_title('HALO - Veterinary Dashboard', 'Monitoring canine vitals across temperature, pulse, and respiration.')

	# --- Time Window Setup ---
	time_options = [
		('1h', 1),
		('6h', 6),
		('24h', 24),
		('7d', 168),
	]
	if 'hours' not in st.session_state:
		st.session_state['hours'] = 24 # Default to 24h
	hours = st.session_state['hours']

	# --- Data Loading and Filtering ---
	# Run refresh logic first if the button was clicked
	refresh_col, download_col = st.columns([1,1]) # Placeholders for layout
	if 'full_data' not in st.session_state:
		st.session_state['full_data'] = simulator.simulate_vitals(168)

	# Filter data based on the selected time window
	full_df = st.session_state['full_data'].sort_values('timestamp')
	latest = full_df.iloc[-1]
	cutoff = latest['timestamp'] - pd.Timedelta(hours=hours)
	df = full_df[full_df['timestamp'] >= cutoff].copy()

	# --- Vitals and Charts ---
	stats_container = st.container()
	charts_container = st.container()

	with stats_container:
		st.markdown(
			f"""
			<div class="dashboard-section">
				<div class="vital-summary">
					<div class="vital-card">
						<span class="label">Temperature</span>
						<span class="value">{latest.temperature_C:.1f}</span>
						<span class="unit">°C</span>
					</div>
					<div class="vital-card">
						<span class="label">Pulse</span>
						<span class="value">{latest.pulse_bpm}</span>
						<span class="unit">bpm</span>
					</div>
					<div class="vital-card">
						<span class="label">Respiration</span>
						<span class="value">{latest.respiration_bpm:.1f}</span>
						<span class="unit">bpm</span>
					</div>
				</div>
			</div>
			""",
			unsafe_allow_html=True,
		)

	with charts_container:
		st.markdown('<div class="dashboard-section">', unsafe_allow_html=True)
		c1, c2, c3 = st.columns(3)
		with c1:
			fig_t = plot_time_series(df, 'timestamp', 'temperature_C', 'Temperature (°C)', y_range=(36.5, 41))
			st.plotly_chart(fig_t, key='temp_chart')
		with c2:
			fig_p = plot_time_series(df, 'timestamp', 'pulse_bpm', 'Pulse (BPM)', y_range=(40, 200))
			st.plotly_chart(fig_p, key='pulse_chart')
		with c3:
			fig_r = plot_time_series(df, 'timestamp', 'respiration_bpm', 'Respiration (bpm)', y_range=(6, 80))
			st.plotly_chart(fig_r, key='resp_chart')
		st.markdown('</div>', unsafe_allow_html=True)

	# --- Time Window Controls ---
	def set_hours(h):
		st.session_state['hours'] = h

	_, c1, c2, c3, c4, _ = st.columns([1.5, 1, 1, 1, 1, 1.5])
	button_columns = [c1, c2, c3, c4]

	for col, (label, value) in zip(button_columns, time_options):
		with col:
			is_selected = (value == hours)
			st.button(
				label,
				key=f'tw_{label}',
				on_click=set_hours,
				args=(value,),
				type='primary' if is_selected else 'secondary',
				width='stretch'
			)

	# --- Action Buttons (Refresh & Download) ---
	actions_container = st.container()
	with actions_container:
		_, a1, a2, _ = st.columns([1.5, 1, 1, 1.5])
		with a1:
			if st.button('Refresh Data', width='stretch', key='refresh_data'):
				st.session_state['full_data'] = simulator.simulate_vitals(168)
				st.rerun()
		with a2:
			csv = df.to_csv(index=False)
			b = io.BytesIO()
			b.write(csv.encode())
			b.seek(0)
			st.download_button('Download CSV', b, file_name='vitals.csv', mime='text/csv', width='stretch')


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

