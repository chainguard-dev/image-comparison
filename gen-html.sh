#!/usr/bin/env bash

# A simple script that reads from rumble data, gets extra info
# about the latest scanned image (size and build time), then
# uses this data to create the image-comparison-*.html files

set -ex

function epoch {
    ts="$(echo "${1}" | cut -d. -f1 | sed 's|Z||')"
    python3 -c "from datetime import datetime as dt; t = dt.strptime('${ts}', '%Y-%m-%dT%H:%M:%S'); print(int((t - dt(1970, 1, 1)).total_seconds() * 1000))"
}

function epoch_now {
    python3 -c "from datetime import datetime as dt; t = dt.now(); print(int((t - dt(1970, 1, 1)).total_seconds() * 1000))"
}

# Inspired by https://gist.github.com/imjasonh/ce437a40160acab17030d024d4680fd2
function image_size {
    size="$(crane manifest $1 --platform ${2:-linux/amd64} | jq '.config.size + ([.layers[].size] | add)' | numfmt --to=iec)"
    echo "${size}" | sed 's|K| KB|' | sed 's|M| MB|' | sed 's|G| GB|' | sed 's|T| TB|'
}

function main {
    for combo in \
        "go|Go|cgr.dev/chainguard/go:latest|golang:latest" \
        "nginx|Nginx|cgr.dev/chainguard/nginx:latest|nginx:latest" \
        "php|PHP|cgr.dev/chainguard/php:latest|php:latest"; do

        image_key="$(echo "${combo}" | cut -d\| -f1)"
        image_name="$(echo "${combo}" | cut -d\| -f2)"

        ours_ref="$(echo "${combo}" | cut -d\| -f3)"
        ours_cves_num="$(cat data.csv | grep ",${ours_ref}" | head -1 | cut -d, -f12)"
        
        theirs_ref="$(echo "${combo}" | cut -d\| -f4)"
        theirs_cves_num="$(cat data.csv | grep ",${theirs_ref}" | head -1 | cut -d, -f12)"

        ours_size="$(image_size "${ours_ref}")"
        ours_crane_resp="$(crane config "${ours_ref}")"
        ours_timestamp="$(epoch "$(echo "${ours_crane_resp}" | jq -r '.created')")"

        theirs_size="$(image_size "${theirs_ref}")"
        theirs_crane_resp="$(crane config "${theirs_ref}")"
        theirs_timestamp="$(epoch "$(echo "${theirs_crane_resp}" | jq -r '.created')")"

        ours_size_num="$(echo "${ours_size}" | awk '{print $1}')"
        ours_size_unit="$(echo "${ours_size}" | awk '{print $2}')"
        theirs_size_num="$(echo "${theirs_size}" | awk '{print $1}')"
        theirs_size_unit="$(echo "${theirs_size}" | awk '{print $2}')"

        generated_at_timestamp="$(epoch_now)"

        cat html/image-comparison.template.html | \
            sed "s|{{imageName}}|${image_name}|g" | \
            sed "s|{{oursCvesNum}}|${ours_cves_num}|g" | \
            sed "s|{{oursSizeNum}}|${ours_size_num}|g" | \
            sed "s|{{oursSizeUnit}}|${ours_size_unit}|g" | \
            sed "s|{{oursTimestamp}}|${ours_timestamp}|g" | \
            sed "s|{{theirsCvesNum}}|${theirs_cves_num}|g" | \
            sed "s|{{theirsSizeNum}}|${theirs_size_num}|g" | \
            sed "s|{{theirsSizeUnit}}|${theirs_size_unit}|g" | \
            sed "s|{{theirsTimestamp}}|${theirs_timestamp}|g" | \
            sed "s|{{generatedAtTimestamp}}|${generated_at_timestamp}|g" > \
                "html/image-comparison-${image_key}.html"
    done
}

main
