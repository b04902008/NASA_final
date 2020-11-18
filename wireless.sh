#!/usr/bin/env bash
aveRSSI=0
aveTxRate=0
for i in $(seq 1 10); do
	sleep 1s
	data=$(/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I | tr -s ' ')
	SSID=$(echo $data | cut -f29 -d' ')
	RSSI=$(echo $data | cut -f2 -d' ')
	TxRate=$(echo $data | cut -f15 -d' ')
	#echo "$SSID: $RSSI $TxRate"
	aveRSSI=$(($aveRSSI+$RSSI))
	aveTxRate=$(($aveTxRate+$TxRate))
done

SSID=$(echo $data | cut -f29 -d' ')
echo "$SSID $(($aveRSSI/10)).$((-aveRSSI%10)) $(($aveTxRate/10))"