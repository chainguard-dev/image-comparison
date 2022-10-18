# image-comparison

Comparison of [Chainguard Images](https://github.com/chainguard-images)
to others

## Overview

Each day for 30 days (from September 15, 2022 to October 14, 2022), we
ran security scans using [Trivy](https://github.com/aquasecurity/trivy)
against the following images:

- `golang:latest`
- `nginx:latest`
- `php:latest`
- `cgr.dev/chainguard/go:latest` (Chainguard)
- `cgr.dev/chainguard/nginx:latest` (Chainguard)
- `cgr.dev/chainguard/php:latest` (Chainguard)

The final results of this process can be found in [`data.csv`](./data.csv).

## Reproducing the results

Each of the images scanned have a "floating" tag (i.e. `latest`),
meaning that the image contents may change from one day to the next.
Chainguard Images, for example, are rebuilt each night.

To ensure that this dataset could be reproduced, we have included a
`digest` field for each entry in the CSV which can be used to locate
the exact version of the image at the exact time that it was scanned.

An image reference with a digest comes in the following form:

```
<image_without_tag>@<digest>
```

For example, for the Chainguard NGINX image scanned on September 12, 2022
(row 15 in the [CSV](./previous/data-aug-sep-2022.csv)), the image reference with a digest would be:

```
cgr.dev/chainguard/nginx@sha256:d08d864569e20105bed1d4f58b852ea3d810e7d26ec0280011dcae1135421f3f
```

To attempt to reproduce the results for a given scan, run `trivy image` pointing to this type of image reference:

```
$ trivy image cgr.dev/chainguard/nginx@sha256:d08d864569e20105bed1d4f58b852ea3d810e7d26ec0280011dcae1135421f3f
```

You can also use `--format json` for machine-readable output.

## A small caveat

It is worth noting that Trivy does a great job of keeping its vulnerability
database updated (~every 6 hours). However, due to this, it can be hard to
truly reproduce these results unless you maintain your own copy of the
database (which Chainguard currently does not).

To resolve this issue long-term, we have opened
[a pull request](https://github.com/aquasecurity/trivy-db/pull/251)
to publish a tagged version of the vulnerability database on each update.
More information on workarounds can be found in the PR description.
You can also see the Trivy documentation on
[air-gapped environments](https://github.com/aquasecurity/trivy/blob/main/docs/docs/advanced/air-gap.md).

This being the case, the number of CVEs reported for a given image should
only increase over time. There are 2 methods in which you could confidently
assert that an image was not vulnerable to a given CVE at the time of
the scan:

1. Follow the URL to the CVE summary and compare the time of the scan to the "Published" date.
2. Compare the time of the scan to the date when a vulnerable package was patched/released.

For example, when running a new Trivy scan on September 21, 2022 against the Chainguard
NGINX image scanned on August 16, 2022 (row 177 in the [CSV](./previous/data-aug-sep-2022.csv)), the following 2 CVEs are detected
which were not previously detected:

```
$ trivy image cgr.dev/chainguard/nginx@sha256:69cbee1dc3bddd1d2dd6e44dd8294f065d1c1cc3a75f7a8c70fbbaf1d827452e

...

Total: 2 (UNKNOWN: 0, LOW: 0, MEDIUM: 0, HIGH: 1, CRITICAL: 1)

┌──────────┬────────────────┬──────────┬───────────────────┬───────────────┬─────────────────────────────────────────────────────────────┐
│ Library  │ Vulnerability  │ Severity │ Installed Version │ Fixed Version │                            Title                            │
├──────────┼────────────────┼──────────┼───────────────────┼───────────────┼─────────────────────────────────────────────────────────────┤
│ libexpat │ CVE-2022-40674 │ CRITICAL │ 2.4.8-r1          │ 2.4.9-r0      │ libexpat before 2.4.9 has a use-after-free in the doContent │
│          │                │          │                   │               │ function i ......                                           │
│          │                │          │                   │               │ https://avd.aquasec.com/nvd/cve-2022-40674                  │
├──────────┼────────────────┼──────────┼───────────────────┼───────────────┼─────────────────────────────────────────────────────────────┤
│ libxml2  │ CVE-2022-2309  │ HIGH     │ 2.9.14-r1         │ 2.10.0-r0     │ lxml: NULL Pointer Dereference in lxml                      │
│          │                │          │                   │               │ https://avd.aquasec.com/nvd/cve-2022-2309                   │
└──────────┴────────────────┴──────────┴───────────────────┴───────────────┴─────────────────────────────────────────────────────────────┘
```

Open each of the URLs provided for more details.

For the first one (CVE-2022-40674), the "Published" date is Sep 14, 2022, which means
this CVE was not even known at the time of the scan (method #1).

For the second one (CVE-2022-2309), the "Published" date is Jul 5, 2022, so we must
try method #2.

Go to [release-monitoring.org](https://release-monitoring.org/) and search for "libxml2".
The search should land you on [this page](https://release-monitoring.org/project/1783/).

In the "Versions" section, look for the "Fixed" version as indicated in the Trivy result
(`2.10.0`). Notice that this version was not released until August 17, 2022.

If we re-run this scan against the the Chainguard NGINX image scanned on August 19, 2022
(row 165 in the CSV) after the patched version of `libxml2` was packaged and
made available on the
[Alpine edge repo](https://pkgs.alpinelinux.org/package/edge/main/x86/libxml2),
CVE-2022-2309 should be gone, and only CVE-2022-40674 should be detected:

```
$ trivy image cgr.dev/chainguard/nginx@sha256:70932f8e4f962129135a4b37585aa296769e72ba637d349a54cd90537900281d

...

Total: 1 (UNKNOWN: 0, LOW: 0, MEDIUM: 0, HIGH: 0, CRITICAL: 1)

┌──────────┬────────────────┬──────────┬───────────────────┬───────────────┬─────────────────────────────────────────────────────────────┐
│ Library  │ Vulnerability  │ Severity │ Installed Version │ Fixed Version │                            Title                            │
├──────────┼────────────────┼──────────┼───────────────────┼───────────────┼─────────────────────────────────────────────────────────────┤
│ libexpat │ CVE-2022-40674 │ CRITICAL │ 2.4.8-r1          │ 2.4.9-r0      │ libexpat before 2.4.9 has a use-after-free in the doContent │
│          │                │          │                   │               │ function i ......                                           │
│          │                │          │                   │               │ https://avd.aquasec.com/nvd/cve-2022-40674                  │
└──────────┴────────────────┴──────────┴───────────────────┴───────────────┴─────────────────────────────────────────────────────────────┘
```
