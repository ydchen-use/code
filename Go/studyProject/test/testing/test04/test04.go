package main

import (
	"fmt"
	"time"
)

func producer(p chan <- int) {
	for i := 0; i < 10; i++ {
		p <- i
		fmt.Println("Send:", i)
	}
}

func consumer(c <-chan int) {
	for i := 0; i < 10; i++ {
		v := <- c
		fmt.Println("Received:", v)
	}
}

func main() {
	ch := make(chan int, 10)
	go producer(ch)
	go consumer(ch)
	time.Sleep(1 * time.Second)
}