import db

execute = db.initialize()
execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
execute('DROP TABLE track;')
execute('CREATE TABLE track (time TIMESTAMP, provider UUID, state TEXT, latitude SMALLINT, longitude SMALLINT);')
