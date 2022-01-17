#!/bin/bash 
#SCRIPT=$(readlink -f "$0")
SCRIPT=$(readlink "$0")
SCRIPTPATH=$(dirname "$SCRIPT")
echo $SCRIPTPATH
cd $SCRIPTPATH
scrapy crawl woninglabel_business > Debug_Business.txt 2<&1
scrapy crawl woninglabel_private > Debug_Private.txt 2<&1