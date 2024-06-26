CREATE TABLE PERIODIC_TASK (
  id SERIAL PRIMARY KEY,
  name VARCHAR (50) NOT NULL,
  interval_seconds INTEGER NOT NULL,
  arg VARCHAR (50) NOT NULL
);
CREATE TABLE GATE (
  id INTEGER PRIMARY KEY,
  closed BOOLEAN NOT NULL,
  open_permission VARCHAR (50) NOT NULL
);
CREATE TABLE GATE_SWITCH (
  id SERIAL PRIMARY KEY,
  gate_id INTEGER REFERENCES GATE(id),
  value BOOLEAN NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);