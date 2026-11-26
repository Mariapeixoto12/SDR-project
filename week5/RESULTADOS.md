# Week 5 — resultados

## Sinal de referência

Na Week 5 queríamos verificar se o recetor consegue estimar uma rotação de fase conhecida. A gravação das semanas anteriores já contém os efeitos da transmissão real. Por isso criámos um sinal em simulação e usámos o mesmo ficheiro nas duas execuções, a 0° e a +20°. Assim, a única alteração entre ensaios foi a rotação que inserimos depois da FFT.

Partimos do [exemplo `wifi_loopback.grc`](https://github.com/bastibl/gr-ieee802-11/blob/maint-3.10/examples/wifi_loopback.grc), que gera tramas Wi-Fi. Ligámos um **File Sink** do tipo **Complex** à saída do **Packet Pad2**, que acrescenta amostras a zero antes de cada trama. O sinal foi captado antes do **Channel Model**, onde o exemplo introduz ruído. Ao executar o loopback, o File Sink guardou as amostras em [week5_referencia.bin](week5_referencia.bin). Esse é o ficheiro que o recetor da Week 5 lê no **File Source**.

![Ramo do Packet Pad2 para o File Sink, antes de configurar o caminho do ficheiro](../prints/week5/captura_referencia.png)

*Montagem do ramo de captura, antes de preencher o caminho no File Sink.*

## Estimativa de fase

No [fluxograma da Week 5](WEEK5.grc), o **Fast Multiply Const** fica entre a FFT e o **WiFi Frame Equalizer**. Usámos a constante `1` para 0° e `0.9396926208+0.3420201433j` para +20°. Esta segunda constante tem módulo 1 e roda os valores complexos, incluindo os pilotos, sem alterar as suas magnitudes.

O equalizador usa os quatro pilotos para estimar a rotação e aplica o ângulo inverso, `−beta`, aos 64 valores de cada símbolo. O **Tag Debug** mostra o `beta` estimado para o símbolo SIGNAL, em radianos. [Código do equalizador](https://github.com/bastibl/gr-ieee802-11/blob/maint-3.10/lib/frame_equalizer_impl.cc)

| Rotação que introduzimos | Rotação estimada pelo recetor (`beta`) |
|---:|---:|
| 0° | `3.32614e-08 rad` (praticamente 0°) |
| +20° | `0.349066 rad` (aproximadamente +20°) |

Em cada ensaio, as 24 etiquetas mostraram o mesmo valor. A diferença entre as duas medições correspondeu aos +20° introduzidos.

![Fast Multiply Const entre a FFT e o equalizador, com leitura do beta a +20°](../prints/week5/beta_20graus.png)

## Constelação após a correção e a equalização

Nos dois ensaios, observámos os pontos perto de **(−1, 0)** e **(+1, 0)**, as duas posições esperadas em BPSK. O `beta` mostrou que o recetor acompanhou a rotação introduzida. A constelação mostra o resultado à saída, depois da correção de fase e da equalização.

![Constelação BPSK à saída do equalizador no ensaio a +20°](../prints/week5/constelacao_20graus.png)

![Constante unitária, leitura do beta e constelação BPSK no ensaio a 0°](../prints/week5/constelacao_0graus.png)
