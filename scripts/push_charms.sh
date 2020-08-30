#!/bin/bash

set -e

stage=$1

for charm in slurmrestd slurmctld slurmd slurmdbd; do
    s3_loc="s3://omnivector-public-assets/charms/$charm/$stage/$charm.charm"
    echo "Copying $charm.charm to $s3_loc"
    aws s3 cp --acl public-read ./$charm.charm $s3_loc
done
