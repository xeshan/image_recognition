#!/bin/bash

docker build -t pokemon-image-recognition .
docker run -p 8501:8501 pokemon-image-recognition