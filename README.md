# image-comparison

Comparison of [Chainguard Images](https://github.com/chainguard-images)
to others

## Overview

We run security scans using [grype]([https://github.com/aquasecurity/trivy](https://github.com/anchore/grype))
against the following images:

- `golang:latest`
- `nginx:latest`
- `php:latest`
- `cgr.dev/chainguard/go:latest` (Chainguard)
- `cgr.dev/chainguard/nginx:latest` (Chainguard)
- `cgr.dev/chainguard/php:latest` (Chainguard)

The final results of this process can be found in [`data.csv`](./data.csv).
This is the last thirty days of results.
