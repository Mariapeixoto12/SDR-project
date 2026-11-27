# Week 1 - deteção de tramas

O ficheiro [week1_frame_detection.grc](week1/week1_frame_detection.grc) lê amostras de uma gravação em banda base e calcula uma correlação normalizada com atraso de 16 amostras. A investigação, a descrição do cálculo e os resultados estão em [WEEK1.md](week1/WEEK1.md).

## Preparação

1. Descompactar `Wifi_Project_Baseband_recordings.tar.gz` e guardar a gravação `Sample1_20MHz_Channel36.bin` no computador.
2. Abrir o ficheiro `.grc` no GNU Radio Companion 3.10, verificar o caminho configurado no File Source e executar com F6. As amostras são interpretadas como valores complexos, com 32 bits para cada componente I/Q.
3. A gravação é grande (aproximadamente 1,6 GB), pelo que não foi incluída no GitHub.

O File Source está configurado para utilizar um excerto da gravação. A variável `samp_rate` corresponde à frequência de amostragem de 20 MS/s, enquanto `playback_rate` controla a velocidade de reprodução do ficheiro.

Para experimentar diferentes janelas de autocorrelação, podemos alterar a variável `nwin` e executar novamente o circuito.

## Reproduzir a comparação

Com Python, NumPy e Matplotlib instalados, executar a partir da pasta principal do repositório:

```text
python experiments/compare_windows.py recordings/Sample1_20MHz_Channel36.bin
```

Este comando pressupõe que a gravação foi colocada na pasta `recordings`, na raiz do projeto.

O script gera o gráfico [compare_windows.png](experiments/compare_windows.png), permitindo comparar os resultados obtidos para diferentes valores de `NWin`.

## Week 2 - Sync Short

Nesta semana, acrescentámos o bloco **WiFi Sync Short** para detetar possíveis inícios de trama a partir da autocorrelação calculada na Week 1.

Testámos diferentes valores de **Threshold** e **Min Plateau**, observando as etiquetas `wifi_start` produzidas pelo bloco.

O circuito está disponível em [week2_sync_short.grc](week2/week2_sync_short.grc).

A montagem, os testes e os resultados encontram-se em [WEEK2.md](week2/WEEK2.md).

As capturas de ecrã estão na pasta [prints/week2](prints/week2/).

## Week 3 - Frequency Offset Correction

Nesta semana, acrescentámos o bloco **WiFi Sync Long** ao circuito da Week 2, para estudar a correção do desvio residual de frequência e o funcionamento da entrada atrasada.

Realizámos experiências com diferentes valores de **Sync Length** e **Delay**, comparando as etiquetas de sincronização e as amostras de saída.

O circuito está disponível em [week3_sync_long.grc](week3/week3_sync_long.grc).

A explicação, as experiências e os resultados encontram-se em [WEEK3.md](week3/WEEK3.md).

As capturas de ecrã estão na pasta [prints/week3](prints/week3/).

## Week 5 - Correção de fase

Comparámos a estimativa de fase do WiFi Frame Equalizer com 0° e +20° de rotação introduzida depois da FFT. A estimativa acompanhou a rotação e a constelação à saída ficou nas duas posições esperadas em BPSK.

O [fluxograma](week5/WEEK5.grc), o [sinal de referência](week5/week5_referencia.bin) e os [resultados](week5/RESULTADOS.md) estão na pasta `week5`.

## Week 6 - Equalização e campo SIGNAL

Estudámos a equalização e a leitura do campo SIGNAL. O [fluxograma](week6/WEEK6.grc) permite observar as etiquetas `encoding` e `frame bytes`; a explicação e a verificação inicial estão em [RESULTADOS.md](week6/RESULTADOS.md).
