# 🚀 Loja Veloz — Plataforma de Pedidos em Microsserviços

Solução Cloud DevOps de ponta a ponta para modernização da plataforma **Pedidos Veloz**, contemplando desenvolvimento local padronizado com Docker Compose, orquestração em Kubernetes, pipeline CI/CD automatizado, Infraestrutura como Código (Terraform) e observabilidade distribuída.

---

## 🎥 Vídeo Pitch (Demonstração)
* **Link do Vídeo (YouTube):** `[INSERIR_LINK_DO_YOUTUBE_AQUI_APOS_GRAVACAO]`

---

## 🏗️ Arquitetura do Sistema
* **API Gateway (`gateway`):** Ponto único de entrada HTTP (FastAPI).
* **Serviço de Pedidos (`pedidos`):** Gerencia pedidos no PostgreSQL e publica o evento `PedidoCriado`.
* **Serviço de Pagamentos (`pagamentos`):** Consome eventos do RabbitMQ e processa pagamentos de forma assíncrona.
* **Serviço de Estoque (`estoque`):** Consome eventos do RabbitMQ e realiza a baixa de itens.
* **Infraestrutura de Apoio:** PostgreSQL 15 e RabbitMQ 3.

---

## 💻 Como Executar Localmente (Um Único Comando)

### Pré-requisitos
* Docker e Docker Compose instalados.

### Passo a Passo
1. Clone o repositório:
   ```bash
   git clone [https://github.com/Beatriz-Preiraa/Loja-Veloz.git](https://github.com/Beatriz-Preiraa/Loja-Veloz.git)
   cd Loja-Veloz