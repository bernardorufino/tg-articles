#!/usr/bin/env bash

DIR=$(dirname $0)

rm ${DIR}/out/data.idx 2> /dev/null
rm ${DIR}/out/data.json 2> /dev/null
rm ${DIR}/log/* 2> /dev/null
exit 0
