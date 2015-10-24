#!/usr/bin/env bash

DIR=$(dirname $0)

function logfile {
    PREFIX=$([[ -z $1 ]] && echo "" || echo $1"_")
    SUFFIX=$([[ -z $2 ]] && echo "" || echo "_"$2)
    echo "${DIR}/log/"${PREFIX}$(date "+%Y%m%d_%H%M%S")${SUFFIX}".log"
}

function googlenews_subsection {
    if [[ -z $1 ]]; then
        URL="https://news.google.com"
    else
        URL="https://news.google.com/news/section?topic="$1
    fi
    LOGFILE=$(logfile "provider" $2)
    echo "${DIR}/provider.py ${URL} | xargs -n 2 ${DIR}/parser.py  -l "${LOGFILE}" -o ${DIR}/out/data.json  -i ${DIR}/out/data.idx"
    ${DIR}/provider.py ${URL} | xargs -n 2 ${DIR}/parser.py  -l ${LOGFILE} -o ${DIR}/out/data.json -i ${DIR}/out/data.idx #2> ${LOGFILE}
}


# Main page
googlenews_subsection "" "main"

if [[ $1 != "single" ]]; then

    # "Mundo" news
    googlenews_subsection "w" "mundo"

    # "Brasil" news
    googlenews_subsection "n" "brasil"

    # "Negocios" news
    googlenews_subsection "b" "negocios"

    # "Ciencia e Tecnologia" news
    googlenews_subsection "t" "tech"

    # "Entretenimento" news
    googlenews_subsection "e" "entretenimento"

    # "Esportes" news
    googlenews_subsection "s" "esportes"

    # "Mais" news
    googlenews_subsection "h" "mais"

fi
