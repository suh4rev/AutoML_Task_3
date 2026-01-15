# ML Model Monitoring  
**Prometheus + Alertmanager + Telegram**

Небольшой проект для демонстрации мониторинга качества ML-модели.  
Система рассчитывает метрику **F1**, собирает её через **Prometheus**,  
поднимает алерт через **Alertmanager** и отправляет уведомление в **Telegram**.

---

## Состав проекта

- **exporter/** — Python-экспортер метрик (F1) в формате Prometheus  
- **monitoring/** — конфигурация Prometheus, Alertmanager и правила алертов  
- **telegram_webhook/** — Flask-сервис для отправки алертов в Telegram  
- **shared/** — входные батчи с результатами модели:
  - `reference_batch.joblib` — эталонные предсказания  
  - `current_batch.joblib` — текущие (хуже) предсказания  

---

## Требования

- Docker  
- Docker Compose  

---

## Быстрый запуск

```bash
docker compose up --build
```

---

## Проверка работы

1) Метрики экспортера  
http://localhost:8000/metrics  
Проверить `model_f1` и `model_phase`.

2) Prometheus  
http://localhost:9090  
Запрос: `model_f1` → Execute.

3) Alertmanager  
http://localhost:9093  
Алерт `ModelF1TooLow` должен быть активен при F1 < 0.7.

4) Telegram  
Уведомление приходит автоматически через `telegram_webhook`.

---

## Тест Telegram вручную

Можно отправить тестовый алерт:

```bash
curl -X POST http://localhost:5001/alert   -H "Content-Type: application/json"   -d '{"alerts":[{"status":"firing","labels":{"alertname":"TestAlert"},"annotations":{"summary":"Exam","description":"Test notification"}}]}'
```

---

## Как работает алерт

1. Экспортер публикует метрику `model_f1`  
2. Prometheus регулярно собирает данные  
3. В `monitoring/alert.rules.yml` задано правило:

```
model_f1 < 0.7
```

4. Если значение держится ниже порога заданного времени
5. Alertmanager отправляет алерт в `telegram_webhook`  
6. Уведомление приходит в Telegram  

---

## Архитектура

```
Exporter → Prometheus → Alertmanager → Telegram Webhook → Telegram
```
