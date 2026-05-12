import os
import subprocess
import sys

# ==========================================================
# CONFIGURAÇÕES DE DNA (NÃO ALTERAR PARA MANTER ATIVAÇÃO)
# ==========================================================
VM_UUID = "5f5f7363-6172-796d-6973-74616b655f5f"
VM_MAC = "00:0c:29:65:f5:f5"
# Caminho absoluto baseado na localização do script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VM_DISK = os.path.join(BASE_DIR, "Diagbox9.91_64Bits_VM_PSA-DIAGBOX.COM.BR_(Rev.05)/HDD_9.91.vmdk")

# ID detectado do seu scanner
PSA_VENDOR = "103a"
PSA_PRODUCT = "f008"

def run_vm():
    if not os.path.exists(VM_DISK):
        print(f"[!] Erro: Disco não encontrado em {VM_DISK}")
        return

    # Comando base otimizado
    cmd = [
        "qemu-system-x86_64",
        "-enable-kvm",
        "-m", "4G",
        "-smp", "2",
        "-cpu", "host,hv_relaxed,hv_spinlocks=0x1fff,hv_vapic,hv_time",
        "-drive", f"file={VM_DISK},format=vmdk,if=ide",
        "-net", f"nic,model=e1000,macaddr={VM_MAC}",
        "-net", "user",
        "-uuid", VM_UUID,
        "-vga", "qxl",
        "-rtc", "base=localtime",  # Sincroniza relógio para evitar erros de licença
        "-device", "qemu-xhci,id=usb", # Controlador USB 3.0 (mais estável)
        "-device", "usb-tablet",       # Mouse mais preciso
    ]

    # Verifica se o scanner está plugado
    output = subprocess.check_output(["lsusb"]).decode()
    if f"{PSA_VENDOR}:{PSA_PRODUCT}" in output.lower():
        print(f"[+] Scanner PSA detectado ({PSA_VENDOR}:{PSA_PRODUCT}). Conectando...")
        cmd.extend(["-device", f"usb-host,vendorid=0x{PSA_VENDOR},productid=0x{PSA_PRODUCT}"])
    else:
        print("[!] Scanner NÃO detectado no USB. A VM iniciará, mas o Diagbox não verá o scanner.")

    print("\n[>>>] INICIANDO DIAGBOX VM...")
    print("Se a tela ficar preta, aguarde o carregamento do Windows.")
    
    try:
        subprocess.run(cmd)
    except Exception as e:
        print(f"[!] Erro ao iniciar QEMU: {e}")

if __name__ == "__main__":
    run_vm()
