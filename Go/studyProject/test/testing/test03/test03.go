package main

import (
	"fmt"
)

func chanTest(ch chan <- int) {
	ch <- 1
	ch <- 2
	ch <- 3
}

func main() {
	numChan := make(chan int)
	go func() {
		for i := 0; i <= 5; i++{
			numChan <- i
		}
		close(numChan)
	}()


	//for value, ok := <- numChan {
	//	if !ok{
	//		close(numChan)
	//	}
	//	fmt.Printf("The element received from channel numChan: %v\n", value)
	//}

	//close(numChan)

	for value := range numChan{
		fmt.Printf("The element received from channel numChan: %v\n", value)
	}
	//time.Sleep(2 * time.Second)
}