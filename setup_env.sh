#!/bin/bash

# Nome do ambiente virtual
VENV_NAME="env_pos"

# Criar ambiente virtual
python3 -m venv $VENV_NAME

# Ativar o ambiente virtual
source $VENV_NAME/bin/activate

# Update pip
pip install --upgrade pip

# Instalar as bibliotecas
pip install matplotlib numpy pygame
pip install torch torchvision torchaudio

# Informar que a instalação foi concluída
echo "Ambiente virtual criado e bibliotecas instaladas com sucesso!"

echo "Para ativar o ambiente novamente, use:"
echo "source $VENV_NAME/bin/activate"

echo "Para desativar, use:"
echo "source deactivate"
