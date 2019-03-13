#!/bin/bash
set -eu

sourcecred_module="$(dirname "$0")""/../sourcecred"
(cd "${sourcecred_module}"; yarn && yarn backend)

sourcecred() {
  (cd "${sourcecred_module}"; node ./bin/sourcecred.js "$@")
}

output_dir="$(dirname "$0")"

load_repo() {
  echo "loading $1/$2"
  sourcecred load "$1"/"$2"
  sourcecred export-graph "$1"/"$2" | jq . >"${output_dir}/$1_$2.json"
}

load_repo "sourcecred" "sourcecred"
load_repo "sourcecred" "research"
load_repo "sourcecred" "pm"
load_repo "sourcecred" "notes"
