import pandas as pd
import numpy as np
from datetime import datetime, timedelta


class Simulator:
	"""Generate simulated vital signs for the veterinary dashboard."""

	def simulate_vitals(self, hours: int) -> pd.DataFrame:
		"""Simulate dog vitals for the past `hours` hours.

		Sampling:
		- <=24 hours: 1-minute resolution
		- 7 days: 5-minute resolution
		"""
		now = datetime.now()
		if hours <= 24:
			freq = '1min'
		else:
			freq = '5min'

		start = now - timedelta(hours=hours)
		idx = pd.date_range(start=start, end=now, freq=freq)
		t = np.linspace(0, 2 * np.pi, len(idx))

		temp_base = 38.6 + 0.2 * np.sin(2 * t)
		temp = temp_base + np.random.normal(scale=0.12, size=len(idx))
		spike_idx = np.random.choice(len(idx), size=max(1, len(idx)//1000), replace=False)
		for si in spike_idx:
			span = min(60, len(idx) - si)
			temp[si:si+span] += np.linspace(0.5, -0.2, span)

		# Pulse (BPM)
		pulse_base = 80 + 8 * np.sin(4 * t) + 6 * np.sin(t/2)
		pulse = pulse_base + np.random.normal(scale=6, size=len(idx))
		pulse = np.clip(pulse, 40, 190)

		# Respiration
		resp_base = 18 + 3 * np.sin(3 * t)
		resp = resp_base + np.random.normal(scale=2.0, size=len(idx))
		resp = np.clip(resp, 6, 80)

		df = pd.DataFrame({
			'timestamp': idx,
			'temperature_C': np.round(temp, 2),
			'pulse_bpm': np.round(pulse).astype(int),
			'respiration_bpm': np.round(resp, 1),
		})
		return df
