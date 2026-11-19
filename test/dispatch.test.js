import test from "node:test";
import assert from "node:assert/strict";
import { assignDriver, distanceKm, findNearestDrivers } from "../src/dispatch.js";

const pickup = { lat: 47.9184, lon: 106.9177 }; // Сүхбаатарын талбай
const drivers = [
  { id: "d1", lat: 47.92, lon: 106.92, status: "available" },
  { id: "d2", lat: 47.95, lon: 106.98, status: "available" },
  { id: "d3", lat: 47.9185, lon: 106.9178, status: "busy" },
  { id: "d4", lat: 47.9180, lon: 106.9170, status: "available" },
];

test("Haversine зай ойролцоогоор зөв", () => {
  const d = distanceKm(pickup, { lat: 47.9284, lon: 106.9177 }); // ~1.1 км
  assert.ok(d > 1.0 && d < 1.3, `expected ~1.1km, got ${d}`);
});

test("зөвхөн чөлөөт, радиус доторх жолоочдыг эрэмбэлнэ", () => {
  const result = findNearestDrivers(drivers, pickup, { radiusKm: 3 });
  assert.deepEqual(
    result.map((d) => d.id),
    ["d4", "d1"],
  );
});

test("хамгийн ойрын жолоочийг оноож, ETA тооцно", () => {
  const assignment = assignDriver(drivers, { pickup });
  assert.equal(assignment.driverId, "d4");
  assert.ok(assignment.etaMinutes >= 1);
});

test("ойр жолооч байхгүй бол null", () => {
  assert.equal(assignDriver(drivers, { pickup, radiusKm: 0.01 }), null);
});
