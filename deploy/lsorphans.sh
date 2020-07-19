#!/usr/bin/env bash
set -e

BASE_DIR="."
if [[ -e "$1" ]]; then
  BASE_DIR="$1"
fi

declare -a LINK_SOURCES
LINK_SOURCES=( current env prev prev-env )
declare -a GOOD_TARGETS

for SRC in "${LINK_SOURCES[@]}"; do
  DEST=$(readlink "$BASE_DIR/$SRC" || true)
  if [[ -e "$BASE_DIR/$DEST" ]]; then
    DEST=$(basename "$BASE_DIR/$DEST")
    GOOD_TARGETS+=( "$DEST" )
  fi
done

CMD="ls $BASE_DIR/deploys/"
for TARGET in "${GOOD_TARGETS[@]}"; do
  CMD="$CMD | grep -v $TARGET"
done

eval $CMD
