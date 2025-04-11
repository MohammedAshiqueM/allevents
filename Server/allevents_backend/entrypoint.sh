#!/bin/bash
set -e  # Exit on error

mkdir -p /app/media/artist_images
chown -R 1000:1000 /app/media  # Match the user in compose file
chmod -R 755 /app/media

echo "Waiting for PostgreSQL to be ready..."
until pg_isready -h db -p 5432 -U postgres; do
    echo "PostgreSQL not ready yet, waiting..."
    sleep 2
done

echo "Running database migrations..."
python manage.py migrate


echo "Importing artist data..."
python manage.py import_all_artists --limit 100 --download-images

echo "Waiting for Elasticsearch to be ready..."
until curl -s http://elasticsearch:9200/_cluster/health; do
    echo "Elasticsearch not ready yet, waiting..."
    sleep 2
done

echo "Rebuilding Elasticsearch index..."
python manage.py search_index --rebuild -f

echo "Starting the Django application..."
exec gosu 1000:1000 "$@"