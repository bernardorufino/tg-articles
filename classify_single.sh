#!/usr/bin/env bash

DIR=$(dirname $0)
URL=$1; shift;
OUT="${DIR}/crawler/out/single.json"

rm ${OUT} &> /dev/null
ANS=$(${DIR}/crawler/parser.py undefined ${URL} --ignore-index -o ${OUT} 2>&1)
CODE=$?
if [[ ${CODE} -ne 0 ]]; then
    echo ${ANS}
    exit ${CODE}
fi
sed -E -e 's|},$|}|' -i '' ${OUT}
${DIR}/classifier/classify.py "${DIR}/crawler/out/classifier" ${OUT}