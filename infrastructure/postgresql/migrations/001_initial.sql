-- Initial schema for pet automation tests

CREATE TABLE IF NOT EXISTS pets (
    id BIGINT PRIMARY KEY,
    name TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'available',
    category TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS orders (
    id BIGINT PRIMARY KEY,
    pet_id BIGINT REFERENCES pets(id) ON DELETE CASCADE,
    quantity INT NOT NULL DEFAULT 1,
    status TEXT NOT NULL DEFAULT 'placed',
    complete BOOLEAN DEFAULT FALSE,
    ship_date TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_pets_status ON pets(status);
CREATE INDEX IF NOT EXISTS idx_orders_pet_id ON orders(pet_id);
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);
