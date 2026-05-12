#!/bin/bash

# ==========================================================
# CONFIGURAÇÕES DE DNA (NÃO ALTERAR PARA MANTER ATIVAÇÃO)
# ==========================================================
VM_NAME="Diagbox_PSA"
UUID="5f5f7363-6172-796d-6973-74616b655f5f"
MAC="000C2965F5F5"

# Detectar o caminho real da pasta (mesmo rodando como root)
BASE_DIR=$(dirname "$(readlink -f "$0")")
DISK_PATH="$BASE_DIR/Diagbox9.91_64Bits_VM_PSA-DIAGBOX.COM.BR_(Rev.05)/HDD_9.91.vdi"

echo "[*] Iniciando configuração da VM no VirtualBox..."

# Verificar se o disco existe
if [ ! -f "$DISK_PATH" ]; then
    echo "[!] ERRO: Disco não encontrado em: $DISK_PATH"
    exit 1
fi

# Remover VM antiga se existir para evitar conflitos
vboxmanage unregistervm "$VM_NAME" --delete 2>/dev/null

# 1. Criar a VM
echo "[*] Criando máquina virtual..."
vboxmanage createvm --name "$VM_NAME" --ostype "Windows7_64" --register

# 2. Configurar Hardware, DNA e Ativação
echo "[*] Aplicando DNA de ativação e configurações de hardware..."
vboxmanage modifyvm "$VM_NAME" \
    --memory 4096 \
    --vram 128 \
    --cpus 2 \
    --graphicscontroller vmsvga \
    --hardware-uuid "$UUID" \
    --macaddress1 "$MAC" \
    --usb-ehci on \
    --mouse usbtablet \
    --rtc-use-utc off

# 3. Configurar Armazenamento (IDE é mais compatível com VMs legadas da PSA)
echo "[*] Configurando controladores de disco..."
vboxmanage storagectl "$VM_NAME" --name "IDE Controller" --add ide
vboxmanage storageattach "$VM_NAME" --storagectl "IDE Controller" --port 0 --device 0 --type hdd --medium "$DISK_PATH"

echo ""
echo "[+] SUCESSO! A VM '$VM_NAME' foi criada com o DNA original."
echo "[!] DICA PARA O SCANNER:"
echo "    Abra o VirtualBox (GUI), vá em Configurações > USB e adicione"
echo "    o filtro para o seu scanner (103a:f008) para que ele seja capturado."
echo ""
echo "Agora você pode abrir o VirtualBox e iniciar a VM 'Diagbox_PSA'."
