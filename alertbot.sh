#!/bin/bash
initCount=0
msg_caption="/tmp/telecaption.txt"

bot_token="7542860081:AAGNGt8TFy9jGu-tzZJdSL0-qg6zunCl1eo"
chat_id="-4558952820"
snort_log="/home/evan/sti.txt"

sendTele()
{
	curl -s -F chat_id="$chat_id" -F text="$caption" https://api.telegram.org/bot$bot_token/sendMessage #> /dev/null 2&>1
}

while true 
do
	lastCount=$(wc -c $snort_log | awk '{print $1}')
	if (($(($lastCount))>$initCount));
		then
		msg=$(tail -n 2 $snort_log)
		echo -e "Snort Alert\n\nServer Time : $(date +"%d %b %Y %T")\n\n"$msg > $msg_caption
		caption=$(<$msg_caption)
		sendTele
		echo "Alert Sent"
		initCount=$lastCount
		rm -f $msg_caption
		sleep 1
	fi
	sleep 2
done
