#!/bin/bash
DIR="$(cd $(dirname ${BASH_SOURCE[0]})/.. && pwd)"
FILES="$(ls ${DIR} | grep '\.py') README.md LICENSE animations"

## Generate the tarball
echo tar -czf dc26-fur-scripts.tar.gz -C ${DIR} ${FILES}
tar -czf dc26-fur-scripts.tar.gz -C ${DIR} ${FILES}
