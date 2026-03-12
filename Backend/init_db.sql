-- ============================================================
-- CureTrace — Reference SQL Schema (PostgreSQL / Neon)
-- Run via: Neon Console → SQL Editor, or psql
-- Alembic is the preferred migration tool; this is for reference.
-- ============================================================

-- Required for gen_random_uuid() on PostgreSQL < 13
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ── patients ────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS patients (
    id          UUID         PRIMARY KEY DEFAULT gen_random_uuid(),
    full_name   VARCHAR(255) NOT NULL,
    dob         DATE         NOT NULL,
    gender      VARCHAR(10),
    blood_type  VARCHAR(5),
    phone       VARCHAR(20),
    email       VARCHAR(255) UNIQUE,
    address     TEXT,
    created_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

-- ── medical_records ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS medical_records (
    id           UUID         PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id   UUID         NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    record_date  DATE,
    doctor_name  VARCHAR(255),
    diagnosis    TEXT,
    prescription TEXT,
    notes        TEXT,
    attachments  JSONB        NOT NULL DEFAULT '[]',
    created_at   TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_medical_records_patient
    ON medical_records(patient_id);

-- ── health_cards ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS health_cards (
    id              UUID         PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id      UUID         NOT NULL UNIQUE REFERENCES patients(id) ON DELETE CASCADE,
    token           TEXT         NOT NULL UNIQUE,
    qr_image_path   VARCHAR(512),
    is_active       BOOLEAN      NOT NULL DEFAULT TRUE,
    issued_at       TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    expires_at      TIMESTAMPTZ
);
