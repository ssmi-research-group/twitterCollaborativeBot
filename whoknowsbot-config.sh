#!/bin/bash

if [[ `lsb_release -rs` != "18.04" ]]
then
	echo "A versão do UBUNTU deve ser 18.04!.."
else
	echo "Iniciando atualização de pacotes..."
	sudo apt update

	echo "Iniciando instalação do Python3.6..."
	sudo apt install python3.6

	echo "Iniciando instalação do gerenciador de pacotes pip..."
	sudo apt install python3-pip

	echo "Iniciando instalação das dependências do projeto..."

	echo "Iniciando instalação do setuptools..."
	sudo python3 -m pip install setuptools

	echo "Iniciando instalação do python-twitter..."
	sudo python3 -m pip install python-twitter

	echo "Iniciando instalação do nltk..."
	sudo python3 -m pip install nltk

	echo "Iniciando instalação do wordcloud..."
	sudo python3 -m pip install wordcloud

	echo "Iniciando instalação do backoff..."
	sudo python3 -m pip install backoff

fi
