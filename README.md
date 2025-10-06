# Table Monitor System


Instruções básicas:


1. Copie os arquivos para o servidor
2. Configure .env
3. python3 -m venv venv && source venv/bin/activate
4. pip install -r requirements.txt
5. Crie o banco e rode database/schema.sql
6. python -m src.main (ou usar gunicorn)


APIs:
- /api/auth/login
- /api/tables
- /api/vision/start
- /api/robot/connect