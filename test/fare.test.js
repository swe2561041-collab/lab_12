import test from "node:test";
import assert from "node:assert/strict";
import { computeFare, FARE_RULES } from "../src/fare.js";

const daytime = new Date("2026-03-10T12:00:00");
const night = new Date("2026-03-10T23:30:00");

test("өдрийн цагийн энгийн тариф", () => {
  const fare = computeFare({ distanceKm: 5, durationMin: 12, startedAt: daytime });
  // 1500 + 6000 + 1800 = 9300
  assert.equal(fare.total, 9300);
  assert.equal(fare.nightSurcharge, 0);
  assert.equal(fare.surgeMultiplier, 1);
});

test("шөнийн цагийн нэмэгдэл 15%", () => {
  const fare = computeFare({ distanceKm: 5, durationMin: 12, startedAt: night });
  // (1500 + 6000 + 1800) + 7500*0.15 = 10425 -> 100₮-өөр дугуйлбал 10400
  assert.equal(fare.nightSurcharge, 1100);
  assert.equal(fare.total, 10400);
});

test("эрэлтийн коэффициент 1.5", () => {
  const fare = computeFare({
    distanceKm: 10,
    durationMin: 25,
    demandLevel: 3,
    startedAt: daytime,
  });
  // 1500 + 12000 + 3750 = 17250 * 1.5 = 25875 -> 25900
  assert.equal(fare.total, 25900);
});

test("доод хязгаар 2000₮ хэрэгжинэ", () => {
  const fare = computeFare({ distanceKm: 0.1, durationMin: 1, startedAt: daytime });
  assert.equal(fare.total, FARE_RULES.minFare);
});

test("буруу өгөгдөлд алдаа шиднэ", () => {
  assert.throws(() => computeFare({ distanceKm: -1, durationMin: 5 }));
  assert.throws(() => computeFare({ distanceKm: 2, durationMin: 5, demandLevel: 9 }));
});
