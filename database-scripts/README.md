# 📦 Instalação e Configuração do Banco de Dados

Este repositório contém os scripts necessários para criar o banco de dados utilizado no projeto.
Siga as etapas abaixo para configurar o ambiente corretamente.

---

## ✅ **Pré-requisitos**

Antes de iniciar, instale:

* **MariaDB 10.6**
* **HeidiSQL** (geralmente já vem junto com o instalador do MariaDB)

---

## 🛠️ **Como importar o banco de dados**

1. **Abra o HeidiSQL**
   
   Após instalar o MariaDB, abra o HeidiSQL normalmente.

3. **Acesse o menu de importação**
   
   No canto superior esquerdo, clique em:

   **Arquivo → Executar arquivo SQL**
   *(equivalente a “File → Run SQL File”)*
   

   ![Imagem do WhatsApp de 2025-11-16 à(s) 18 04 30_0c450dc6](https://github.com/user-attachments/assets/1f44c387-a562-46cc-94c7-5b7a493d5fac)

   ![Imagem do WhatsApp de 2025-11-16 à(s) 18 05 28_03bab19e](https://github.com/user-attachments/assets/37bafcf3-a275-48f9-9e4b-7e41494b7f89)

4. **Selecione o arquivo do banco**
   
   Quando a janela do Windows abrir, escolha o arquivo: ``` weatherdb.sql ```
   
   ![Imagem do WhatsApp de 2025-11-16 à(s) 18 06 37_7fffcd01](https://github.com/user-attachments/assets/476c3e96-27ee-460f-a247-18fbd87dd8d4)

6. **Execute a importação**
   
   Clique em **Avançar/Executar** e aguarde a finalização.

8. **Atualize a instância**
   
   No painel esquerdo do HeidiSQL, clique com o botão direito sobre a instância e selecione:

   **Atualizar**
   (como se estivesse atualizando uma página)
   
   ![Imagem do WhatsApp de 2025-11-16 à(s) 18 07 48_dd8bdd2c](https://github.com/user-attachments/assets/98be540d-867e-4526-8964-b3e5395ce0d9)

10. **Verifique se o banco apareceu**

   O banco de dados deve surgir com o nome: ```weatherdb```
   
   ![Imagem do WhatsApp de 2025-11-16 à(s) 18 08 05_7b16cde1](https://github.com/user-attachments/assets/9e246e3a-5d33-4034-bd0d-eeab4754bbfc)

---

## ✔️ Pronto!

Seu banco foi instalado com sucesso e já está disponível para uso no projeto.

