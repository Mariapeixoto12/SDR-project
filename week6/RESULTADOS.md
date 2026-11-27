# Week 6 — equalização e campo SIGNAL

## O que faz o equalizador?

Depois da FFT, as subportadoras recebidas podem apresentar diferenças de amplitude e de fase. O equalizador usa uma estimativa do canal para compensar essas alterações antes de decidir quais foram os símbolos transmitidos. No nosso circuito, o bloco chama-se **WiFi Frame Equalizer**.

Com o algoritmo **LS**, a implementação atual usa os dois símbolos de treino longo (L-LTF) para estimar a resposta do canal. Em seguida, divide cada subportadora de dados pela respetiva estimativa. O bloco também corrige a fase, como vimos na Week 5, e seleciona **48 subportadoras de dados** das 64 posições da FFT, excluindo os quatro pilotos, a posição central e as posições de guarda. [Código do algoritmo LS](https://github.com/bastibl/gr-ieee802-11/blob/ad0598e4a874f4b8e1f391a1e0323e80df2b34ff/lib/equalizer/ls.cc)

## Porque é que o artigo fala apenas em BPSK e QPSK?

O artigo de 2013 explica que a equalização da amplitude usava uma aproximação que não correspondia igualmente bem a todos os emissores. Isso limitava o recetor descrito pelos autores a BPSK e QPSK. Em 16-QAM e 64-QAM, a informação depende também da amplitude, pelo que uma equalização imprecisa pode dificultar a identificação dos pontos. Esta era uma limitação da implementação descrita no artigo, não da norma Wi-Fi. [Artigo, secção 2.6](https://www.ccs-labs.org/bib/bloessl2013ofdmreceiver/bloessl2013ofdmreceiver.pdf)

O código atual prevê BPSK, QPSK, 16-QAM e 64-QAM. A presença destas opções no código não é, por si só, um teste de receção com todas elas. [Modulações na implementação atual](https://github.com/bastibl/gr-ieee802-11/blob/ad0598e4a874f4b8e1f391a1e0323e80df2b34ff/include/ieee802_11/mapper.h#L27-L36)

## Como é delimitada a trama?

O preâmbulo contém sequências conhecidas que ajudam o recetor a detetar e alinhar o início da transmissão. Depois do treino, o campo **SIGNAL** indica o comprimento da trama e como os dados seguintes foram codificados. O comprimento ajuda o recetor a saber quantos dados deve processar. A trama MAC contém informação como os endereços, os dados e um campo de verificação de erros.

## O que é o SIGNAL?

O SIGNAL é enviado depois do treino longo e antes dos dados. O recetor precisa da sua informação para saber como interpretar o resto da trama.

No formato estudado, tem **24 bits**: 4 de RATE, 1 reservado, 12 de LENGTH, 1 de paridade e 6 de tail. Os bits são codificados com código convolucional de taxa **1/2**, entrelaçados e transmitidos em **BPSK** num símbolo OFDM. O recetor conhece este formato e consegue ler o SIGNAL antes de saber qual é a modulação escolhida para os dados seguintes. [Construção do SIGNAL no código](https://github.com/bastibl/gr-ieee802-11/blob/ad0598e4a874f4b8e1f391a1e0323e80df2b34ff/lib/signal_field_impl.cc)

Na versão atual do módulo, a leitura do SIGNAL está integrada no **WiFi Frame Equalizer**. Quando o campo é descodificado e aceite, o bloco publica etiquetas como `encoding` e `frame bytes`. A primeira identifica a modulação e a taxa de codificação através de um número interno da implementação. A segunda dá o comprimento da trama indicado no SIGNAL, em bytes. [Descodificação e etiquetas](https://github.com/bastibl/gr-ieee802-11/blob/ad0598e4a874f4b8e1f391a1e0323e80df2b34ff/lib/frame_equalizer_impl.cc#L211-L255)

## Experiência

Preparámos [WEEK6.grc](WEEK6.grc) a partir do circuito da Week 5. O recetor lê a mesma gravação simulada, com o Fast Multiply Const configurado para `1`. Acrescentámos dois Tag Debug à saída do equalizador para observar `encoding` e `frame bytes`.

Numa **verificação automática do circuito**, apareceram 8 etiquetas `encoding` com valor `0` e 8 etiquetas `frame bytes` com valor `38`. O valor `0` corresponde a BPSK com taxa de codificação 1/2 na enumeração interna desta implementação; não é o valor bruto dos bits RATE. Os 38 bytes incluem 24 bytes de cabeçalho MAC, 10 bytes de mensagem e 4 bytes de verificação FCS. O tamanho indicado pelo SIGNAL não é apenas o da mensagem útil. Estes valores foram verificados pelo assistente e ainda devem ser observados pelo grupo no GNU Radio. [Construção da trama MAC](https://github.com/bastibl/gr-ieee802-11/blob/ad0598e4a874f4b8e1f391a1e0323e80df2b34ff/lib/mac.cc)

## Utilização de IA

O ChatGPT e o Codex foram usados para ajudar a interpretar o guião, o artigo e o código, preparar o circuito e organizar o texto. Os resultados experimentais serão identificados conforme forem observados.
