# Week 1 — deteção de tramas

O ficheiro `week1_frame_detection.grc` lê amostras de uma gravação em banda base e calcula uma correlação normalizada com atraso de 16 amostras. A investigação, a descrição do cálculo e os resultados estão em [WEEK1.md](WEEK1.md).

## Preparação

1. Descompactar `Wifi_Project_Baseband_recordings.tar.gz` e colocar `Sample1_20MHz_Channel36.bin` dentro da pasta `recordings`, ao lado do ficheiro `.grc`. Neste computador a gravação já foi colocada nessa pasta.
2. Abrir o `.grc` no GNU Radio Companion 3.10 e executar com F6. O File Source assume amostras complexas de 32 bits por componente I/Q. O nome do ficheiro indica 20 MHz; o formato é uma interpretação plausível, não acompanhada de metadados no arquivo.
3. A gravação é grande (1,6 GB). Não é necessário carregá-la para o GitHub; cada utilizador deve obtê-la a partir da fonte da unidade curricular.

O File Source está configurado para repetir o excerto usado na comparação: **Offset** `1247600` e **Length** `900`. Estes campos contam amostras complexas. A repetição liga artificialmente o fim do excerto ao início e pode gerar artefactos nessa junção. Para percorrer a gravação inteira, alterar ambos os campos para `0` e, se não se quiser repetir o ficheiro, colocar **Repeat** em `No`. A taxa física `samp_rate` é 20 MS/s para o eixo temporal; `playback_rate` limita a velocidade de leitura em ficheiro, sem mudar os intervalos representados no gráfico. O trigger do gráfico usa o limiar visual 0,7: não é uma implementação completa de deteção ou descodificação.

Para experimentar outra janela, alterar a variável `nwin` e voltar a executar. Os dois filtros FIR usam decimação 1 e `nwin` coeficientes iguais a 1 para somar uma janela de amostras, como na Figura 1 do artigo. O sinal normalizado pode ultrapassar 1; ajustar os limites verticais do gráfico quando necessário. O Throttle limita a velocidade de leitura do ficheiro e a carga do computador.

## Reproduzir a comparação

Com Python, NumPy e Matplotlib instalados, executar a partir desta pasta:

```text
python experiments/compare_windows.py recordings/Sample1_20MHz_Channel36.bin
```

O script gera `experiments/compare_windows.png` e apresenta os valores medidos. A figura é um exemplo escolhido da gravação, não uma validação de todas as tramas.
