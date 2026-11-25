Week 4 - Symbol Alignment

## Montagem

Partimos do circuito da Week 3 e acrescentámos um **Stream to Vector**, uma **FFT de 64 pontos**, um **Complex to Mag** e um **QT GUI Vector Sink** para observar as magnitudes das subportadoras. Também ligámos um **File Sink** à saída da FFT para guardar os resultados complexos.

Mantivemos a gravação `Sample1_20MHz_Channel36.bin`, com offset **1 247 600**, comprimento **1800 amostras** e `Repeat = No`. O Sync Long continuou configurado com **Sync Length = 320** e **Delay = 320**.

O circuito desta semana está em [WEEK4.grc](WEEK4.grc) e o Python gerado pelo GNU Radio em [WEEK4.py](WEEK4.py).

## Alinhamento dos símbolos

Nesta semana, o objetivo foi perceber como o recetor encontra o início dos símbolos OFDM e prepara as amostras para a FFT (secção 2.4 do artigo).

O **WiFi Sync Long** procura a sequência de treino longa (L-LTF) usando *matched filtering*: compara o sinal recebido com uma sequência que o recetor já conhece. As duas partes úteis da L-LTF repetem-se com uma separação de **64 amostras**, pelo que os picos de correlação ajudam a encontrar a posição correta.

Este método é usado para obter um alinhamento mais preciso. Na deteção inicial, o Sync Short aproveita a repetição da sequência curta através da autocorrelação, sem precisar de localizar exatamente a sequência longa.

Nos símbolos OFDM de dados, cada símbolo tem **80 amostras**: 16 de prefixo cíclico e 64 úteis. O prefixo corresponde a uma cópia das últimas 16 amostras úteis, colocada no início do símbolo. O Sync Long descarta estas 16 amostras nos símbolos seguintes à L-LTF e encaminha as 64 úteis para a próxima etapa.

O **Stream to Vector** agrupa as amostras em vetores de 64, permitindo que a FFT processe um símbolo de cada vez. A FFT transforma o sinal do domínio do tempo para o da frequência, produzindo os valores complexos das 64 posições de subportadora. Usámos `Shift = Yes` para apresentar a posição de DC no centro do vetor.

## Observações

Depois de ligar o Stream to Vector e a FFT, acrescentámos o Complex to Mag e o QT GUI Vector Sink para observar as magnitudes. O File Sink guardou os valores complexos num ficheiro chamado `week4_fft_output.bin`.

![Deteção de trama e saída da FFT](../prints/week4/week4_resultados.png)

*Figura 1 — Autocorrelação normalizada e magnitudes das 64 posições de subportadora na saída da FFT.*

No gráfico superior, continua a observar-se um patamar de autocorrelação próximo de 1, compatível com a sequência curta. No gráfico inferior, as magnitudes são reduzidas nas extremidades e na posição central (índice 32), como esperado para as posições não utilizadas num sinal OFDM com a FFT centrada.

O ficheiro `week4_fft_output.bin` ficou com **5632 bytes**. Como cada valor `complex64` ocupa 8 bytes, obtivemos:

$$
\frac{5632}{8\times64}=11\text{ vetores de 64 valores complexos}
$$

Isto confirma que foram produzidos 11 vetores completos para a FFT. O resultado é compatível com o processamento de símbolos OFDM, mas a observação das magnitudes, por si só, não confirma que os dados da trama tenham sido descodificados corretamente.

## O que vimos no código-fonte

Consultámos o ficheiro [`sync_long.cc`](https://github.com/bastibl/gr-ieee802-11/blob/maint-3.10/lib/sync_long.cc), na branch `maint-3.10`. Nesta implementação:

1. O filtro de correlação utiliza a sequência longa conhecida para procurar os picos da L-LTF.
2. A função `search_frame_start()` procura dois picos separados por aproximadamente **64 amostras**, correspondentes às duas repetições da sequência longa.
3. No estado `COPY`, o bloco mantém as primeiras **128 amostras úteis da L-LTF** e, nos símbolos seguintes, salta as primeiras **16 amostras** de cada grupo de 80, retirando o prefixo cíclico.

No Python gerado pelo GNU Radio, confirmámos também a ligação `Sync Long → Stream to Vector (64) → FFT (64) → File Sink`, com um segundo ramo para o gráfico de magnitudes.

## Repetir a experiência

1. Abrir o ficheiro [WEEK4.grc](WEEK4.grc) no GNU Radio Companion e verificar o caminho da gravação no File Source.
2. Confirmar `Offset = 1247600`, `Length = 1800`, `Repeat = No`, `Sync Length = 320`, `Delay = 320`, `Stream to Vector = 64` e `FFT Size = 64`.
3. Executar o circuito e observar os dois gráficos.
4. Confirmar que o File Sink criou `week4_fft_output.bin` e verificar o tamanho do ficheiro.

## Utilização de IA

O ChatGPT foi utilizado como apoio na interpretação dos blocos e na organização da documentação.
