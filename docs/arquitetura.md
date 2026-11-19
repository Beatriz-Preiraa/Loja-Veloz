# Arquitetura Cloud-Native — Pedidos Veloz

## 1. Fluxo da Aplicação
1. O cliente realiza uma requisição HTTP `POST /api/pedidos` no **API Gateway**.
2. O **API Gateway** valida a entrada e encaminha de forma síncrona para o **Serviço de Pedidos**.
3. O **Serviço de Pedidos** persiste o registro no **PostgreSQL** e publica o evento `PedidoCriado` em uma exchange *fanout* no **RabbitMQ**.
4. Os serviços de **Pagamentos** e **Estoque** consomem o evento de forma assíncrona e independente, garantindo desacoplamento e resiliência durante picos de acesso.

## 2. Estratégia de Deploy (Rolling Update)
Adotamos o **Rolling Update** configurado nos manifestos Kubernetes (`maxSurge: 1` e `maxUnavailable: 0`) aliado a `readinessProbes` no endpoint `/health`. Novos pods só passam a receber tráfego após confirmarem prontidão, eliminando indisponibilidades durante deploys.

## 3. Estratégia de Escalabilidade (HPA)
Configuramos o **Horizontal Pod Autoscaler (HPA)** para os serviços de borda e entrada (`gateway` e `pedidos`), escalando automaticamente de **2 a 8 réplicas** sempre que a utilização média de CPU ultrapassar **70%**, atendendo à demanda elástica de campanhas promocionais.

## 4. Observabilidade (Logs, Métricas e Traces)
- **Logs:** Saída padronizada em `stdout/stderr` (padrão *12-Factor App*) para coleta centralizada no cluster.
- **Métricas:** Coleta via **Prometheus** (latência, taxa de erros HTTP, consumo de CPU/memória e tamanho das filas no RabbitMQ).
- **Tracing Distribuído:** Arquitetura baseada no **OpenTelemetry Collector**, propagando o `trace_id` desde a entrada no API Gateway até o processamento assíncrono nas filas de Pagamentos e Estoque.

## 5. Referência de Mercado
Arquitetura inspirada no projeto de referência oficial **Google Cloud Microservices Demo (Online Boutique)**, aplicando desacoplamento por eventos, conteinerização segura (multi-stage e usuário não-root) e telemetria via OpenTelemetry.