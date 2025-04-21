python3 src/main.py 
diditwork=$?

if [ $diditwork != 0 ]; then 
	echo "Something went wrong in the pythong";
	exit 1 
fi

cd public && python3 -m http.server 8888