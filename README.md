# Test Task 3D
A Python tool for computing distances between voxel points in medical images using SimpleITK.

## Overview
This module provides functionality for transforming voxel indices to world coordinates and computing minimum and maximum distances between sets of points extracted from two medical images. It's specifically useful in medical imaging applications where accurate spatial measurements are required.


## Prerequisites
### For Containerized Runs
- Docker

### For Local Runs
- Python >= 3.14
- [uv](https://github.com/astral-sh/uv) package manager

## Docker
- Build the image:
  ```shell
  make docker-build
  ```

- Run the container:
  ```shell
  make docker-run
  ```

## Quickstart
- Install dependencies:
  ```shell
  make install
  ```

- Run the application locally:
  ```shell
  make run-local
  ```
