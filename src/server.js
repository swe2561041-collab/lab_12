/**
 * Такси дуудлагын систем — REST API (жишиг хэрэгжилт).
 * Зөвхөн Node.js стандарт сан ашигласан, сангуй (zero dependency).
 */
import { createServer } from "node:http";
import { randomUUID } from "node:crypto";
import { computeFare } from "./fare.js";
import { assignDriver, findNearestDrivers } from "./dispatch.js";

const rides = new Map();
const drivers = new Map([
  [
    "d1",
    { id: "d1", name: "Бат", lat: 47.9184, lon: 106.9177, status: "available" },
  ],
  [
    "d2",
    { id: "d2", name: "Сарнай", lat: 47.9091, lon: 106.9301, status: "available" },
  ],
  [
    "d3",
    { id: "d3", name: "Тэмүүлэн", lat: 47.9250, lon: 106.9050, status: "busy" },
  ],
]);

const send = (res, status, body) => {
  res.writeHead(status, { "Content-Type": "application/json; charset=utf-8" });
  res.end(JSON.stringify(body));
};

const readJson = (req) =>
  new Promise((resolve, reject) => {
    let raw = "";
    req.on("data", (chunk) => {
      raw += chunk;
      if (raw.length > 1e6) reject(new Error("payload too large"));
    });
    req.on("end", () => {
      if (!raw) return resolve({});
      try {
        resolve(JSON.parse(raw));
      } catch {
        reject(new Error("invalid JSON body"));
      }
    });
    req.on("error", reject);
  });

/** POST /api/rides — захиалга үүсгэх */
function createRide(body) {
  if (!body.pickup || !body.dropoff) {
    return [400, { error: "pickup and dropoff are required" }];
  }
  const ride = {
    id: randomUUID(),
    riderId: body.riderId ?? "anon",
    pickup: body.pickup,
    dropoff: body.dropoff,
    status: "searching",
    driverId: null,
    createdAt: new Date().toISOString(),
  };
  const assignment = assignDriver([...drivers.values()], {
    pickup: ride.pickup,
    radiusKm: body.radiusKm ?? 3,
  });
  if (assignment) {
    ride.driverId = assignment.driverId;
    ride.etaMinutes = assignment.etaMinutes;
    ride.status = "assigned";
    const driver = drivers.get(assignment.driverId);
    driver.status = "busy";
  }
  rides.set(ride.id, ride);
  return [201, ride];
}

const server = createServer(async (req, res) => {
  const url = new URL(req.url, `http://${req.headers.host}`);
  const { pathname } = url;

  try {
    // GET /api/drivers?lat=&lon=&radius=
    if (req.method === "GET" && pathname === "/api/drivers") {
      const pickup = {
        lat: Number(url.searchParams.get("lat") ?? 47.9184),
        lon: Number(url.searchParams.get("lon") ?? 106.9177),
      };
      const radiusKm = Number(url.searchParams.get("radius") ?? 3);
      return send(res, 200, findNearestDrivers([...drivers.values()], pickup, { radiusKm }));
    }

    if (req.method === "POST" && pathname === "/api/rides") {
      const [status, payload] = createRide(await readJson(req));
      return send(res, status, payload);
    }

    const rideMatch = pathname.match(/^\/api\/rides\/([^/]+)$/);
    if (req.method === "GET" && rideMatch) {
      const ride = rides.get(rideMatch[1]);
      return ride ? send(res, 200, ride) : send(res, 404, { error: "ride not found" });
    }

    const fareMatch = pathname.match(/^\/api\/rides\/([^/]+)\/fare$/);
    if (req.method === "POST" && fareMatch) {
      const ride = rides.get(fareMatch[1]);
      if (!ride) return send(res, 404, { error: "ride not found" });
      const body = await readJson(req);
      const fare = computeFare({
        distanceKm: body.distanceKm,
        durationMin: body.durationMin,
        demandLevel: body.demandLevel ?? 1,
      });
      ride.fare = fare;
      return send(res, 200, fare);
    }

    if (req.method === "GET" && pathname === "/health") {
      return send(res, 200, { status: "ok", rides: rides.size });
    }

    send(res, 404, { error: "not found" });
  } catch (error) {
    send(res, 400, { error: error.message });
  }
});

const port = Number(process.env.PORT ?? 3000);
server.listen(port, () => {
  console.log(`Taxi dispatch API listening on http://localhost:${port}`);
});
