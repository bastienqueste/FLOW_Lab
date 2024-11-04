#!/bin/bash

set +H

printf "\nOutil de test pour le capteur SUNA\n\n"

if [ -z "$1" ]; then
    printf "Argument manquant: port du capteur.\nEx: ./SUNATester \"J5\"\n"
    set -H
    exit
fi


INFO="Vous avez indique le port $1\n"

case "$1" in
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
    "/dev/ttyUSB0")
        printf "$INFO"
        PORT="/dev/ttyUSB0"
        ;;
    *) 
        echo "Veuillez specifier un port valide: J4, J5, J6, J7, J9"
        set -H
        exit
        ;;
esac

write_cmd()
{
    strlength=`echo -n $1|wc -m`
    for i in `seq 1 $strlength`
    do
        printf "${1:i-1:1}" >> $PORT
    done
    printf "\r\n" >> $PORT
}

stty -F $PORT 57600 -parenb -parodd -cmspar cs8 hupcl -cstopb \
                    cread clocal -crtscts ignbrk -brkint -ignpar \
                   -parmrk -inpck -istrip -inlcr -igncr -icrnl \
                    -ixon -ixoff -iuclc -ixany -imaxbel -iutf8 \
                    -opost -olcuc -ocrnl -onlcr -onocr -onlret \
                    -ofill -ofdel nl0 cr0 tab0 bs0 vt0 ff0 -isig \
                    -icanon -iexten -echo -echoe -echok -echonl \
                    -noflsh -xcase -tostop -echoprt -echoctl \
                    -echoke -flusho -extproc

sleep 1

#Wake Up sensor
write_cmd " "
sleep 3

echo -e "Entrez \"q\" pour quitter le tester"

#Infinite loop to read sensor data frames
while true; do

    # Ask one measurement
    echo -e "\nEnvoi de la requête : \"Measure 1\"\nLecture des trames..."
    write_cmd "Measure 1;"

    # Read one line and display it
    read -t 5 INPUT < $PORT
    printf "\e[32m$INPUT\n\n\e[0m"
    read -t 5 INPUT < $PORT
    printf "\e[32m$INPUT\n\n\e[0m"
 
    read -N 1 -t 0.5 pressed
    if [[ $pressed = "q" ]] || [[ $pressed = "Q" ]] 
    then
        break
    fi
done

#Stop sensor acquisition
write_cmd "Sleep"
sleep 3


if [ $1 != "/dev/ttyUSB0" ]; then
    # Power down sensor
    `echo "$1" | tr '[:upper:]' '[:lower:]'` 0
fi

set -H
exit
