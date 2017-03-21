#!/bin/bash
docker build -t raceman:latest -t raceman:$(git rev-parse --short HEAD) .