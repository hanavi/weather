#!/bin/bash

WEATHERFILE=$HOME/.weather
WEATHERSCRIPT=$HOME/weather.py
DELAY=20 # seconds

while true
do
  clear

  if [[ -f $WEATHERFILE && ! $( find $WEATHERFILE -mmin +10 ) ]]
  then
    echo "Weather File ok"
    echo ""
  else
    echo "Updating weather information"
    echo ""
    $WEATHERSCRIPT > $WEATHERFILE
  fi

  cat $WEATHERFILE

  sleep $DELAY

done

