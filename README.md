# Такси дуудлагын систем — SAD236 · Лаборатори 12

Архитектурын зохиомж, компонент, интерфейс болон CI-ийн жишиг хэрэгжилт.
Сэдэв: **Такси дуудлагын систем** (зорчигч, жолооч, диспетчер).

## Агуулга

| Хавтас / файл | Тайлбар |
| --- | --- |
| `docs/lab12-taxi-architecture.docx` | Лабораторийн тайлан (Алхам 1–6, диаграмм, хүснэгт) |
| `docs/adr-001.md` | Архитектурын шийдвэрийн баримт (ADR-001) |
| `docs/diagrams/` | Гурван түвшинт архитектур ба компонентын диаграмм (PNG) |
| `db/schema.sql` | PostgreSQL + PostGIS схем, индексүүд |
| `src/fare.js` | Тарифын тооцоолол (суурь, км, минут, шөнийн нэмэгдэл, эрэлт) |
| `src/dispatch.js` | Хамгийн ойрын чөлөөт жолоочийг сонгох (Haversine) |
| `src/server.js` | REST API — захиалга, жолооч, тариф (`node:http`) |
| `test/` | `node:test` нэгж тестүүд |
| `.github/workflows/ci.yml` | GitHub Actions CI (npm ci → npm test) |

## Локал ажиллуулах

```bash
npm ci          # сангуй (zero dependency) тул хурдан
npm test        # 9 тест
npm start       # http://localhost:3000
```

### API жишээ

```bash
curl -s -X POST localhost:3000/api/rides \
  -H 'Content-Type: application/json' \
  -d '{"pickup":{"lat":47.9184,"lon":106.9177},"dropoff":{"lat":47.93,"lon":106.95}}'

curl -s "localhost:3000/api/drivers?lat=47.9184&lon=106.9177&radius=3"

curl -s -X POST localhost:3000/api/rides/<rideId>/fare \
  -H 'Content-Type: application/json' \
  -d '{"distanceKm":5,"durationMin":12,"demandLevel":2}'
```

## GitHub-д байршуулах (Алхам 6)

```bash
# 1. GitHub дээр "taxi-dispatch" нэртэй репо үүсгээд (README-гүй) дараахыг ажиллуулна
git init -b main                       # аль хэдийн init хийсэн бол алгасна
git add .
git commit -m "feat: такси дуудлагын системийн архитектур ба CI"
git remote add origin https://github.com/<хэрэглэгч>/taxi-dispatch.git
git push -u origin main
```

2. **Settings → Collaborators** — багийн гишүүд болон багшийг урина.
3. **Settings → Branches → Add branch protection rule** — `main` салбарыг хамгаалж,
   «Require a pull request before merging» ба «Require status checks to pass» (CI) сонгоно.
4. Ажил бүрийг `feature/<нэр>` салбар дээр хийж, pull request-ээр нэгтгэнэ.
5. **Actions** таб дээр CI-ийн ногоон ✓ харагдана.

## Тестийн хамрах хүрээ

- Тариф: өдрийн тариф, шөнийн +15%, эрэлтийн коэффициент 1.5, доод хязгаар 2000₮, буруу өгөгдөл.
- Хуваарилалт: Haversine зай, радиус шүүлт, зөвхөн чөлөөт жолооч, ETA, ойр жолоочгүй тохиолдол.
