#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE TABLE channel (
        id VARCHAR PRIMARY KEY,
        name VARCHAR NOT NULL,
        subscribers INTEGER
    );

    CREATE TABLE videos (
        id VARCHAR PRIMARY KEY,
        title VARCHAR NOT NULL,
        date_created TIMESTAMP,
        channel_id VARCHAR REFERENCES channel(id),
        likes INTEGER,
        comments INTEGER,
        views INTEGER
    );

    CREATE TABLE importtask (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        start_import TIMESTAMP,
        end_import TIMESTAMP,
        status VARCHAR,
        nb_videos_created INTEGER,
        nb_videos_updated INTEGER
    );
EOSQL
