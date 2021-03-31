build: 
	docker build -t main .
run:  
	docker run -p 80:80 main 