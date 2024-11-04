#!/bin/bash

set +H

if [ -z "$3" ]; then
    printf "Argument manquant: Taper la commande avec les arguments suivants:\n"
    printf "\t\"./SensorTester SENSORNAME JX  BAUDRATE\" \n"
    printf "\tExemple: \"./SensorTester FLBBCD J5 19200\" \n"
    set -H
    exit
fi

printf "===============================================================\n"
printf "|                                                             |\n"
printf "|                     Outil de test capteur                   |\n"
printf "|                                                             |\n"
printf "===============================================================\n"

INFO="\n\tCapteur: \t$1\n\tPort: \t\t$2\n\tVitesse: \t$3b\n\n"
case "$2" in
    "J4") 
        printf "$INFO"
        PORT="/dev/ttyS1"
        j4 1
        ;;
    "J5")
        printf "$INFO"
        PORT="/dev/ttyS2"
        j5 1
        ;;
    "J6")
        printf "$INFO"
        PORT="/dev/ttyS3"
        j6 1
        ;;
    "J7")
        printf "$INFO"
        PORT="/dev/ttyS5"
        j7 1
        ;;
    "J9")
        printf "$INFO"
        PORT="/dev/ttyS6"
        j9 1
        ;;
    *) 
        printf "\nErreur:\tVeuillez specifier un port valide (J4, J5, J6, J7, J9)\n"
        set -H
        exit
        ;;
esac

printf "\nVeuillez patienter pendant l'allumage du capteur...\n\n"

stty -F $PORT $3 -parenb -parodd -cmspar cs8 hupcl -cstopb \
                    cread clocal -crtscts ignbrk -brkint -ignpar \
                   -parmrk -inpck -istrip -inlcr -igncr -icrnl \
                    -ixon -ixoff -iuclc -ixany -imaxbel -iutf8 \
                    -opost -olcuc -ocrnl -onlcr -onocr -onlret \
                    -ofill -ofdel nl0 cr0 tab0 bs0 vt0 ff0 -isig \
                    -icanon -iexten -echo -echoe -echok -echonl \
                    -noflsh -xcase -tostop -echoprt -echoctl \
                    -echoke -flusho -extproc

sleep 2

echo "Lecture des trames du capteur..."
echo "Entrez \"q\" to quit"

#Infinite loop to read sensor data frames
while true; do

    # Read one line and display it
    read INPUT < $PORT
    printf "\e[32m$INPUT\n\n\e[0m"

    read -N 1 -t 0.01 pressed
    if [[ $pressed = "q" ]] || [[ $pressed = "Q" ]] 
    then
        break
    fi
done


# Power down sensor
`echo "$2" | tr '[:upper:]' '[:lower:]'` 0
set -H
exit
