#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

BINARY="./target/debug/cve-cli"

echo "TEST 1. Empty params:"
EMPTY_PARAMS=$("${BINARY}" | tr -d '[:cntrl:]')

if [[ ${EMPTY_PARAMS} == "[1;31mSomething went wrong, use --help flag[0m" ]]; then
    echo -e "${GREEN}PASSED${NC}"
else
    echo -e "${RED}FAILED${NC}"
fi
