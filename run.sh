#!/bin/bash

set -e

abort() {
    echo "$*"; exit 1;
}

usage() {
    abort """Usage: $(basename $0) [-h|--help|--use-proxy] SPIDER $(python sample_input.py 2>&1 | egrep -o '[{].*[}]')
Spider can be one of:

$(scrapy list | sed 's/^/    /')
"""
}

proxy=crawlera
while [ "${1#-}" != "$1" ]; do
    case "$1" in
        -h|--help) usage;;
        --no-proxy) proxy="none";;
        *) usage;;
    esac
    shift
done
[ -n "$1" ] || usage
spider="$1"
item=${2:-chipotle}

mkdir -p tmp

place="$(python sample_input.py $item --spider $spider --proxy $proxy | base64)"
outfile="tmp/${spider}-${item}-out.json"
logfile="tmp/${spider}-${item}-log.txt"

export LOCAL_DEV_ENVIRONMENT=1
RUN_QA_CHECKS=1 scrapy crawl $spider -a place="$place" -o "$outfile"