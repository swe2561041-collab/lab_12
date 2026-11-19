/**
 * Хуваарилалт (dispatch) — хамгийн ойрын чөлөөт жолоочийг сонгох.
 */

const EARTH_RADIUS_KM = 6371;
const toRad = (deg) => (deg * Math.PI) / 180;

/** Хоёр координатын хоорондох зай (км), Haversine томьёо. */
export function distanceKm(a, b) {
  const dLat = toRad(b.lat - a.lat);
  const dLon = toRad(b.lon - a.lon);
  const h =
    Math.sin(dLat / 2) ** 2 +
    Math.cos(toRad(a.lat)) * Math.cos(toRad(b.lat)) * Math.sin(dLon / 2) ** 2;
  return 2 * EARTH_RADIUS_KM * Math.asin(Math.sqrt(h));
}

/**
 * Чөлөөт жолоочдыг зайгаар эрэмбэлж буцаана.
 * @param {Array<{id:string, lat:number, lon:number, status:string}>} drivers
 * @param {{lat:number, lon:number}} pickup
 * @param {{radiusKm?:number, limit?:number}} [options]
 */
export function findNearestDrivers(
  drivers,
  pickup,
  { radiusKm = 3, limit = 5 } = {},
) {
  return drivers
    .filter((driver) => driver.status === "available")
    .map((driver) => ({ ...driver, distanceKm: distanceKm(pickup, driver) }))
    .filter((driver) => driver.distanceKm <= radiusKm)
    .sort((a, b) => a.distanceKm - b.distanceKm)
    .slice(0, limit);
}

/**
 * Захиалгад жолооч оноох. Ойр жолооч байхгүй бол null.
 * @param {Array<object>} drivers
 * @param {{pickup:{lat:number, lon:number}, radiusKm?:number}} ride
 */
export function assignDriver(drivers, { pickup, radiusKm = 3 }) {
  const [nearest] = findNearestDrivers(drivers, pickup, { radiusKm, limit: 1 });
  if (!nearest) return null;
  return {
    driverId: nearest.id,
    distanceKm: Number(nearest.distanceKm.toFixed(2)),
    etaMinutes: Math.max(1, Math.ceil((nearest.distanceKm / 25) * 60)), // дундаж 25 км/ц
  };
}
