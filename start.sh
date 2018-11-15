#! /bin/bash
source /opt/sci-scrapy/crawler_env/bin/activate
SHELL_FOLDER=$(cd "$(dirname "$0")";pwd)
cd $SHELL_FOLDER

for i in $(seq 1 200)  
do   
scrapy crawl SAGE$i
done   
