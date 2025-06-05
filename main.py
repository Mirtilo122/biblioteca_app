from db import execute_script
from interface import menu_principal

def setup_database():
    print("Iniciando configuração dos scripts do banco de dados...")
    scripts = [
        'sql_scripts/tables.sql',
        'sql_scripts/views.sql',
        'sql_scripts/procedures.sql',        
        'sql_scripts/seed.sql'
    ]
    for script in scripts:
        print("Configurando " + script)
        try:
            execute_script(script)
            print("Configuração de "+ script + " concluída!")
        except Exception as e:
            print(f"Falha na execução do script {script}: {e}")

if __name__ == '__main__':
    print("Configurando banco de dados...")
    setup_database()
    print("Banco configurado! Iniciando a aplicação...\n")
    menu_principal()