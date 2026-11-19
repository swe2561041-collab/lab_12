/**
 * Тарифын тооцоолол — Такси дуудлагын систем.
 * Энэ модуль нь зөвхөн дүрэм тооцоолдог (side-effectгүй), тиймээс тестлэхэд хялбар.
 */

export const FARE_RULES = {
  base: 1500, // суух төлбөр, ₮
  perKm: 1200, // ₮/км
  perMinute: 150, // ₮/мин
  minFare: 2000, // доод хязгаар, ₮
  nightSurcharge: 0.15, // 22:00-06:00 хооронд +15%
  nightFromHour: 22,
  nightToHour: 6,
  surgeByDemand: { 1: 1.0, 2: 1.25, 3: 1.5 }, // эрэлтийн түвшин
  rounding: 100, // 100₮-өөр дугуйлна
};

const roundTo = (value, step) => Math.round(value / step) * step;

export function isNightTime(date) {
  const hour = date.getHours();
  const { nightFromHour, nightToHour } = FARE_RULES;
  return hour >= nightFromHour || hour < nightToHour;
}

/**
 * @param {{distanceKm:number, durationMin:number, demandLevel?:1|2|3, startedAt?:Date}} ride
 * @returns {{base:number, distance:number, time:number, nightSurcharge:number, surgeMultiplier:number, total:number}}
 */
export function computeFare({
  distanceKm,
  durationMin,
  demandLevel = 1,
  startedAt = new Date(),
}) {
  if (!Number.isFinite(distanceKm) || distanceKm < 0) {
    throw new Error("distanceKm must be a non-negative number");
  }
  if (!Number.isFinite(durationMin) || durationMin < 0) {
    throw new Error("durationMin must be a non-negative number");
  }
  const surgeMultiplier = FARE_RULES.surgeByDemand[demandLevel];
  if (surgeMultiplier === undefined) {
    throw new Error(`unknown demandLevel: ${demandLevel}`);
  }

  const nightSurcharge =
    (FARE_RULES.base + FARE_RULES.perKm * distanceKm) *
    (isNightTime(startedAt) ? FARE_RULES.nightSurcharge : 0);

  const distance = FARE_RULES.perKm * distanceKm;
  const time = FARE_RULES.perMinute * durationMin;

  const raw =
    (FARE_RULES.base + distance + time + nightSurcharge) * surgeMultiplier;
  const total = roundTo(Math.max(raw, FARE_RULES.minFare), FARE_RULES.rounding);

  return {
    base: FARE_RULES.base,
    distance: roundTo(distance, FARE_RULES.rounding),
    time: roundTo(time, FARE_RULES.rounding),
    nightSurcharge: roundTo(nightSurcharge, FARE_RULES.rounding),
    surgeMultiplier,
    total,
  };
}
