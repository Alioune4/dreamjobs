#!/bin/sh

# Wait for the database to be ready
sleep 5

# Run the migrations
python3 -m flask db upgrade