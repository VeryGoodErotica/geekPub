#!/bin/bash

# This script assumes a RECENT version of FFmpeg (tested with 3.4.2) compiled with
# --enable-libfdk-aac and --enable-libx264 and --enable-libvpx and --enable-libopus
#
# This script assumes sox is installed. It is used to normalize the audio volume
# and audio specification to 16-bit 48kHz.
#
# This script assumes the input video is 16:9 aspect ratio
#
# If you do not want the WebM version generated, you can
# comment out the line near the bottom that reads
#
#  webmencode ${ORIG} 32
#
# If you think the video quality of the resulting 720p MP4 is too low,
# then change the 25 in the line
#
#  mp4encode ${ORIG} 25
#
# to 24 and try again. If quality still too low, try 24, and so on
# until you get a quality you like. But note that each time you
# decrease that number to increase quality, you increase the file
# size.
#
# If you think the video quality of the resulting WebM is too low,
# do a similar thing - decrease the 32 by one and try again and
# so on.
#
# The MP4 encoding is tuned for film. You may want to change the
#
#  -tune film
#
# option in the mp4encode function if not encoding a film. See the
# FFmpeg documentation.

INPUT=$1

FOO="`basename ${INPUT}`"
#sanitize FOO
FOO="`echo ${FOO} |sed -e s?[^\.A-Za-z0-9\-]?"_"?g`"

ORIG="`echo "${FOO}" |sed -e s?"\.[^\.]*$"?".tmp"?`"
if [ `echo "${ORIG}" |grep -c "\.tmp$"` -eq 0 ]; then
  ORIG="${ORIG}.tmp"
fi

CWD="`pwd`"
TMP="`mktemp -d transcode.XXXXXXXX`"
cp -p "${INPUT}" "${TMP}"/${ORIG}
pushd "${TMP}"

function mp4encode {
  IN=$1
  Q=$2
  OUT="`basename -s ".tmp" ${IN}`-720p.mp4"

  ffmpeg -i ${IN} -i master.wav -map 0:v:0 -map 1:0 \
  -vf scale=1280:720 -c:v libx264 -preset veryslow -tune film -crf ${Q} \
  -pix_fmt yuv420p \
  -profile:v baseline -level 3.0 \
  -c:a libfdk_aac -b:a 64k \
  -movflags +faststart \
  ${OUT}
  if [ ! -f ${OUT} ]; then
    echo "Failure creating ${OUT}"
  fi
}

function webmencode {
  IN=$1
  Q=$2
  OUT="`basename -s ".tmp" ${IN}`-720p.webm"

  ffmpeg -y -i ${IN} -map 0:v:0 \
  -vf scale=1280:720 -b:v 1024k -minrate 512k -maxrate 1485k \
  -threads 8 \
  -crf ${Q} -c:v libvpx-vp9 \
  -an \
  -pass 1 -f webm /dev/null

  ffmpeg -i ${IN} -i master.wav -map 0:v:0 -map 1:0 \
  -vf scale=1280:720 -b:v 1024k -minrate 512k -maxrate 1485k \
  -threads 8 \
  -crf ${Q} -c:v libvpx-vp9 \
  -c:a libopus -b:a 48k \
  -pass 2 ${OUT}
  if [ ! -f ${OUT} ]; then
    echo "Failure creating ${OUT}"
  fi
}

# extract and adjust audio
ffmpeg -i ${ORIG} -map 0:a:0 -acodec pcm_s16le -ac 2 pre.wav
ffmpeg-normalize pre.wav -o tmp.wav
sox tmp.wav -b 16 master.wav rate 48000 dither -s

mp4encode ${ORIG} 25
webmencode ${ORIG} 32

mv *.mp4 "${CWD}"/
mv *.webm "${CWD}"/

popd
rm -f "${TMP}"/*
rmdir "${TMP}"
