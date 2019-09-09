#!/bin/bash

EPUBCHECK="${HOME}/java/epubcheck-4.2.2"

OPERATION="java -jar ${EPUBCHECK}/epubcheck.jar"
OPTIONS="$@"

exec ${OPERATION} ${OPTIONS}
