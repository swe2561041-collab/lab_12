-- Такси дуудлагын систем — PostgreSQL схем (PostGIS шаардлагатай)
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE rider (
  id            uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  phone         text NOT NULL UNIQUE,
  full_name     text,
  created_at    timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE driver (
  id            uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  phone         text NOT NULL UNIQUE,
  full_name     text NOT NULL,
  license_no    text NOT NULL,
  status        text NOT NULL DEFAULT 'offline'
                CHECK (status IN ('offline', 'available', 'busy')),
  rating        numeric(2,1) NOT NULL DEFAULT 5.0,
  created_at    timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE vehicle (
  id            uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  driver_id     uuid NOT NULL REFERENCES driver(id) ON DELETE CASCADE,
  plate_no      text NOT NULL UNIQUE,
  model         text NOT NULL,
  seats         smallint NOT NULL DEFAULT 4
);

-- Жолоочийн сүүлийн байршил (5 секунд тутам шинэчлэгдэнэ)
CREATE TABLE driver_location (
  driver_id     uuid PRIMARY KEY REFERENCES driver(id) ON DELETE CASCADE,
  position      geography(Point, 4326) NOT NULL,
  heading       smallint,
  updated_at    timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX driver_location_gix ON driver_location USING GIST (position);

CREATE TABLE ride (
  id            uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  rider_id      uuid NOT NULL REFERENCES rider(id),
  driver_id     uuid REFERENCES driver(id),
  pickup        geography(Point, 4326) NOT NULL,
  dropoff       geography(Point, 4326) NOT NULL,
  status        text NOT NULL DEFAULT 'searching'
                CHECK (status IN ('searching', 'assigned', 'arrived',
                                  'in_progress', 'completed', 'cancelled')),
  distance_km   numeric(6,2),
  duration_min  smallint,
  fare_total    integer,
  requested_at  timestamptz NOT NULL DEFAULT now(),
  completed_at  timestamptz
);
CREATE INDEX ride_status_requested_idx ON ride (status, requested_at DESC);
CREATE INDEX ride_driver_idx ON ride (driver_id, requested_at DESC);

CREATE TABLE payment (
  id            uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  ride_id       uuid NOT NULL REFERENCES ride(id) ON DELETE CASCADE,
  provider      text NOT NULL,          -- qpay, card, cash
  amount        integer NOT NULL,
  status        text NOT NULL DEFAULT 'pending'
                CHECK (status IN ('pending', 'paid', 'failed', 'refunded')),
  external_id   text,
  paid_at       timestamptz
);

-- Аудитын мөр: захиалгын төлөвийн өөрчлөлт бүр
CREATE TABLE ride_event (
  id            bigserial PRIMARY KEY,
  ride_id       uuid NOT NULL REFERENCES ride(id) ON DELETE CASCADE,
  event_type    text NOT NULL,
  payload       jsonb NOT NULL DEFAULT '{}'::jsonb,
  created_at    timestamptz NOT NULL DEFAULT now()
);
