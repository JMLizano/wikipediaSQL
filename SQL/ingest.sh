DB_ENDPOINT=${1}
USERNAME=${2}
PASSWORD=${3}
DB_NAME=${4}

PAGES_URL=https://dumps.wikimedia.org/simplewiki/20181101/simplewiki-20181101-page.sql.gz
CATEGORIES_URL=https://dumps.wikimedia.org/simplewiki/20181101/simplewiki-20181101-categorylinks.sql.gz
PAGELINKS_URL=https://dumps.wikimedia.org/simplewiki/20181101/simplewiki-20181101-pagelinks.sql.gz

TO_DOWNLOAD=( ${PAGES_URL} ${CATEGORIES_URL} ${PAGELINKS_URL} )

for f in "${TO_DOWNLOAD[@]}"
do
  wget -c ${f}
  gunzip ${f##*/}
  UNZIPPED=$(basename "${f##*/}" .gz)
  mysql -h ${DB_ENDPOINT} -u ${USERNAME} -p${PASSWORD} ${DB_NAME} <  ${UNZIPPED}
done

mysql -h ${DB_ENDPOINT} -u ${USERNAME} -p${PASSWORD} ${DB_NAME} < clean_data.sql