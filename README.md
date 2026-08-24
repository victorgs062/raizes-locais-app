# Raízes Locais 🌱

**Raízes Locais** é uma plataforma que conecta pequenos agricultores locais diretamente aos consumidores, promovendo sustentabilidade, compras conscientes e a redução da pegada de carbono. O aplicativo facilita o encontro de produtos frescos e orgânicos na sua região.

Este repositório contém as duas partes principais do projeto:
1. **Backend**: Uma API desenvolvida em Python com Flask, seguindo práticas de Clean Architecture e SOLID. Responsável pelo controle de usuários, estoque de produtos, e cálculos de rotas de sustentabilidade.
2. **Frontend**: Um aplicativo móvel desenvolvido em Flutter, estruturado com componentes reutilizáveis, gerenciamento de estado via Provider e conectividade em tempo real com a API.

---

## 🛠 Pré-requisitos

Para rodar este projeto localmente, você precisará ter instalado na sua máquina:
- **Python** (3.8 ou superior)
- **Flutter SDK** (3.10 ou superior)
- **Git** para clonagem do repositório

---

## 🚀 Como Executar o Backend (API Flask)

1. Abra seu terminal e navegue até a pasta do backend:
   ```bash
   cd backend
   ```

2. Crie e ative um ambiente virtual (recomendado):
   ```bash
   # No Windows:
   python -m venv .venv
   .venv\Scripts\activate

   # No Linux/Mac:
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Instale as dependências do projeto:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure as variáveis de ambiente:
   - Certifique-se de que existe um arquivo chamado `.env` dentro da pasta `backend/`. Caso não exista, crie um com as variáveis de email para recuperação de senhas (opcional para rodar localmente, mas necessário para a feature completa):
     ```env
     EMAIL_SENDER=seu_email@gmail.com
     EMAIL_PASSWORD=sua_senha_de_app
     ```

5. Inicialize o servidor local:
   ```bash
   python run.py
   ```
   > A API ficará disponível em `http://127.0.0.1:5000` ou `http://localhost:5000`.

6. Acesse a documentação Swagger da API:
   - O projeto possui documentação interativa gerada automaticamente.
   - Com o servidor rodando, abra o navegador e acesse: `http://localhost:5000/swagger-ui`
   - Lá você poderá testar todas as rotas e visualizar os schemas dos dados.

---

## 📱 Como Executar o Frontend (App Flutter)

1. Abra um novo terminal e navegue até a pasta do frontend:
   ```bash
   cd frontend
   ```

2. Instale as dependências do Flutter:
   ```bash
   flutter pub get
   ```

3. Configure o host da API:
   - Por padrão, o aplicativo procura a API no arquivo `frontend/lib/services/api_service.dart`.
   - Se você for rodar em um Emulador/Web, o padrão configurado (`localhost:5000` ou `10.1.1.125`) já cobrirá grande parte das situações. Certifique-se de alterar o IP `10.1.1.125` pela rede local (IPv4) da sua máquina caso pretenda debugar o app num celular físico.

4. Execute o aplicativo:
   ```bash
   flutter run
   ```
   > Você pode escolher rodar no emulador Android/iOS, navegador Web, ou em um dispositivo físico conectado via USB.
