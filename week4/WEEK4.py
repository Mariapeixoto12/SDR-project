#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Week 4 - Symbol Alignment
# Author: Maria
# Description: OFDM symbol alignment, cyclic prefix removal and 64-point FFT
# GNU Radio version: 3.10.12.0

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio import blocks
import pmt
from gnuradio import fft
from gnuradio.fft import window
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import ieee802_11
import sip
import threading



class WEEK4(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Week 4 - Symbol Alignment", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Week 4 - Symbol Alignment")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "WEEK4")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)
        self.flowgraph_started = threading.Event()

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 20e6
        self.playback_rate = playback_rate = 1000
        self.nwin = nwin = 48

        ##################################################
        # Blocks
        ##################################################

        self.time_plot = qtgui.time_sink_f(
            768, #size
            samp_rate, #samp_rate
            "Detecao de trama (gravacao Wi-Fi)", #name
            1, #number of inputs
            None # parent
        )
        self.time_plot.set_update_time(0.10)
        self.time_plot.set_y_axis(-0.1, 1.5)

        self.time_plot.set_y_label('Autocorrelacao normalizada', "")

        self.time_plot.enable_tags(False)
        self.time_plot.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.7, 3e-6, 0, "")
        self.time_plot.enable_autoscale(True)
        self.time_plot.enable_grid(True)
        self.time_plot.enable_axis_labels(True)
        self.time_plot.enable_control_panel(False)
        self.time_plot.enable_stem_plot(False)


        labels = ['Correlacao', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.time_plot.set_line_label(i, "Data {0}".format(i))
            else:
                self.time_plot.set_line_label(i, labels[i])
            self.time_plot.set_line_width(i, widths[i])
            self.time_plot.set_line_color(i, colors[i])
            self.time_plot.set_line_style(i, styles[i])
            self.time_plot.set_line_marker(i, markers[i])
            self.time_plot.set_line_alpha(i, alphas[i])

        self._time_plot_win = sip.wrapinstance(self.time_plot.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._time_plot_win)
        self.sum_power = filter.fir_filter_fff(1, [1.0] * nwin)
        self.sum_power.declare_sample_delay(0)
        self.sum_correlation = filter.fir_filter_ccf(1, [1.0] * nwin)
        self.sum_correlation.declare_sample_delay(0)
        self.qtgui_vector_sink_f_0 = qtgui.vector_sink_f(
            64,
            0,
            1,
            'Subcarrier index',
            'Magnitude',
            'FFT Output - OFDM Subcarriers',
            1, # Number of inputs
            None # parent
        )
        self.qtgui_vector_sink_f_0.set_update_time(0.10)
        self.qtgui_vector_sink_f_0.set_y_axis((-140), 10)
        self.qtgui_vector_sink_f_0.enable_autoscale(True)
        self.qtgui_vector_sink_f_0.enable_grid(False)
        self.qtgui_vector_sink_f_0.set_x_axis_units("")
        self.qtgui_vector_sink_f_0.set_y_axis_units("")
        self.qtgui_vector_sink_f_0.set_ref_level(0)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_win = sip.wrapinstance(self.qtgui_vector_sink_f_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_vector_sink_f_0_win)
        self.playback = blocks.throttle( gr.sizeof_gr_complex*1, playback_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * playback_rate) if "auto" == "time" else int(0.1), 1) )
        self.normalize = blocks.divide_ff(1)
        self.multiply = blocks.multiply_vcc(1)
        self.magnitude = blocks.complex_to_mag(1)
        self.instant_power = blocks.complex_to_mag_squared(1)
        #cria se aqui os blocos 
        self.ieee802_11_sync_short_0 = ieee802_11.sync_short(1.0, 16, False, False)
        self.ieee802_11_sync_long_0 = ieee802_11.sync_long(320, False, False)
        self.file_source = blocks.file_source(gr.sizeof_gr_complex*1, 'C:\\Users\\Maria\\Desktop\\MESTRADO\\SDR\\Sample1_20MHz_Channel36.bin', False, 1247600, 1800)
        self.file_source.set_begin_tag(pmt.PMT_NIL)
        self.fft_vxx_1 = fft.fft_vcc(64, True, window.rectangular(64), True, 1)
        self.delay_16_0 = blocks.delay(gr.sizeof_gr_complex*1, 320)
        self.delay_16 = blocks.delay(gr.sizeof_gr_complex*1, 16)
        self.conjugate = blocks.conjugate_cc()
        self.blocks_tag_debug_0_0 = blocks.tag_debug(gr.sizeof_gr_complex*1, "Sync Long", "")
        self.blocks_tag_debug_0_0.set_display(True)
        self.blocks_tag_debug_0 = blocks.tag_debug(gr.sizeof_gr_complex*1, "Sync Short", "")
        self.blocks_tag_debug_0.set_display(True)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, 64)
        self.blocks_file_sink_1 = blocks.file_sink(gr.sizeof_gr_complex*64, 'C:\\Users\\Maria\\Desktop\\MESTRADO\\SDR\\week4_fft_output.bin', False)
        self.blocks_file_sink_1.set_unbuffered(False)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_gr_complex*1, 'C:\\Users\\Maria\\Desktop\\MESTRADO\\SDR\\output_160.bin', False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(64)
        self.avoid_zero = blocks.add_const_ff((1e-8))


        ##################################################
        # Connections
        ##################################################
        self.connect((self.avoid_zero, 0), (self.normalize, 1))
        self.connect((self.blocks_complex_to_mag_0, 0), (self.qtgui_vector_sink_f_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.fft_vxx_1, 0))
        self.connect((self.conjugate, 0), (self.multiply, 1))
        self.connect((self.delay_16, 0), (self.conjugate, 0))
        self.connect((self.delay_16_0, 0), (self.ieee802_11_sync_long_0, 1))
        self.connect((self.fft_vxx_1, 0), (self.blocks_complex_to_mag_0, 0))
        self.connect((self.fft_vxx_1, 0), (self.blocks_file_sink_1, 0))
        self.connect((self.file_source, 0), (self.playback, 0))
        self.connect((self.ieee802_11_sync_long_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.ieee802_11_sync_long_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.ieee802_11_sync_long_0, 0), (self.blocks_tag_debug_0_0, 0))
        self.connect((self.ieee802_11_sync_short_0, 0), (self.blocks_tag_debug_0, 0))
        self.connect((self.ieee802_11_sync_short_0, 0), (self.delay_16_0, 0))
        self.connect((self.ieee802_11_sync_short_0, 0), (self.ieee802_11_sync_long_0, 0))
        self.connect((self.instant_power, 0), (self.sum_power, 0))
        self.connect((self.magnitude, 0), (self.normalize, 0))
        self.connect((self.multiply, 0), (self.sum_correlation, 0))
        self.connect((self.normalize, 0), (self.ieee802_11_sync_short_0, 2))
        self.connect((self.normalize, 0), (self.time_plot, 0))
        self.connect((self.playback, 0), (self.delay_16, 0))
        self.connect((self.playback, 0), (self.ieee802_11_sync_short_0, 0))
        self.connect((self.playback, 0), (self.instant_power, 0))
        self.connect((self.playback, 0), (self.multiply, 0))
        self.connect((self.sum_correlation, 0), (self.ieee802_11_sync_short_0, 1))
        self.connect((self.sum_correlation, 0), (self.magnitude, 0))
        self.connect((self.sum_power, 0), (self.avoid_zero, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "WEEK4")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.time_plot.set_samp_rate(self.samp_rate)

    def get_playback_rate(self):
        return self.playback_rate

    def set_playback_rate(self, playback_rate):
        self.playback_rate = playback_rate
        self.playback.set_sample_rate(self.playback_rate)

    def get_nwin(self):
        return self.nwin

    def set_nwin(self, nwin):
        self.nwin = nwin
        self.sum_correlation.set_taps([1.0] * self.nwin)
        self.sum_power.set_taps([1.0] * self.nwin)




def main(top_block_cls=WEEK4, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()
    tb.flowgraph_started.set()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
