[ -f /tmp/running.pid ] && {
	cat /tmp/running.pid | while read x
	do
		kill -9 "$x"
	done
} || {
	echo "Соме шит хаппенед! \xf0\x9f\x92\xa9"
	echo "Не могу завершить, дёрните рубильник! \xf0\x9f\x95\xb9"
}