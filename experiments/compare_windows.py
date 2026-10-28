"""Compare correlation window lengths for a short section of Sample1.

Example: python experiments/compare_windows.py recordings/Sample1_20MHz_Channel36.bin
The input is interpreted as interleaved little-endian float32 I/Q (complex64).
"""
import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

DELAY = 16
WINDOWS = (16, 48, 96)
START, STOP = 1_247_600, 1_248_500  # sample indices, stop excluded
THRESHOLD = 0.75
EPSILON = 1e-8
FS = 20e6


def metric(x, window):
    """Causal |sum(x[n] * conj(x[n-16]))| / (sum(|x[n]|^2) + eps)."""
    products = x[DELAY:] * np.conj(x[:-DELAY])
    power = np.abs(x[DELAY:]) ** 2
    corr_sum = np.r_[0j, np.cumsum(products, dtype=np.complex128)]
    power_sum = np.r_[0., np.cumsum(power, dtype=np.float64)]
    return np.abs(corr_sum[window:] - corr_sum[:-window]) / (
        power_sum[window:] - power_sum[:-window] + EPSILON
    )


def longest_run(mask):
    edges = np.diff(np.r_[0, mask.astype(np.int8), 0])
    starts, ends = np.flatnonzero(edges == 1), np.flatnonzero(edges == -1)
    if not len(starts):
        return 0, None, None
    i = np.argmax(ends - starts)
    return int(ends[i] - starts[i]), int(starts[i]), int(ends[i])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('recording', type=Path)
    parser.add_argument('--output', type=Path, default=Path('experiments/compare_windows.png'))
    args = parser.parse_args()
    origin = START - DELAY - max(WINDOWS) + 1
    with args.recording.open('rb') as recording:
        recording.seek(origin * 8)
        x = np.fromfile(recording, dtype='<c8', count=STOP - origin)
    if len(x) != STOP - origin:
        raise ValueError('Recording too short for selected interval')
    indices = np.arange(START, STOP)
    fig, (ax_power, ax_metric) = plt.subplots(2, 1, sharex=True, figsize=(10, 6), constrained_layout=True)
    ax_power.plot(indices, np.abs(x[START-origin:STOP-origin]) ** 2, lw=0.8)
    ax_power.set_ylabel('Potência |x|²')
    ax_power.grid(alpha=.25)
    for n in WINDOWS:
        all_values = metric(x, n)
        first_index = origin + DELAY + n - 1
        values = all_values[START-first_index:STOP-first_index]
        run, begin, end = longest_run(values > THRESHOLD)
        print(f'N={n}: máximo={values.max():.3f}; maior sequência > {THRESHOLD} = {run} amostras'
              + (f' [{START+begin}, {START+end})' if begin is not None else ''))
        ax_metric.plot(indices, values, label=f'N = {n}', lw=1)
    ax_metric.axhline(THRESHOLD, color='black', ls='--', lw=.8, label=f'Limiar ilustrativo = {THRESHOLD}')
    ax_metric.set(xlabel='Índice da amostra', ylabel='Correlação normalizada', ylim=(0, 1.5))
    ax_metric.grid(alpha=.25)
    ax_metric.legend(loc='upper right', ncol=2)
    fig.suptitle('Sample1 — comparação da janela (atraso = 16 amostras)')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output, dpi=160)
    print(f'Intervalo: [{START}, {STOP}), {len(indices)/FS*1e6:.1f} µs a 20 MHz')
    print(f'Gráfico: {args.output}')


if __name__ == '__main__':
    main()
