@echo off

REM Nome do ambiente virtual
set VENV_NAME=env_pos

REM Criar ambiente virtual
python -m venv %VENV_NAME%

REM Ativar o ambiente virtual
call %VENV_NAME%\Scripts\activate

REM Instalar as bibliotecas
pip install matplotlib numpy pygame
pip install torch torchvision torchaudio

REM Informar que a instalação foi concluída
echo Ambiente virtual criado e bibliotecas instaladas com sucesso!

echo Para ativar o ambiente novamente, use:
echo call %VENV_NAME%\Scripts\activate

echo Para desativar, use:
echo deactivate
