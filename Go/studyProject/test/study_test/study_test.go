package main

import (
	"fmt"
	"testing"
	"time"
)

func Add(a, b int) int {
	return a + b
}

func TestName(t *testing.T)  {
	for i := 0; i < 10; i++{
		Add(4, 5)
	}
}

func TestName1(t *testing.T)  {
	for i := 0; i <= 10; i++ {
		fmt.Println(i)
		time.Sleep(1 * time.Second)
	}
}

func TestName2(t *testing.T)  {
	ch1 := make(chan int)
	go func() {
		for i := 0; i < 10; i++ {
			ch1 <- i
			time.Sleep(time.Second)
		}
		close(ch1)
	}()

	for range ch1{
		//time.Sleep(5 * time.Second)
		v := <-ch1
		fmt.Println("v: ", v)
	}
}

func TestName3(t *testing.T) {
	var a int
	a = 0
	var b string
	b = "China"
	fmt.Println(a)
	fmt.Println(b)

	var array1 [4]int
	array2 := [7]string{"a", "b", "c", "d", "e", "f", "g"}
	array3 := []int{1, 2, 3, 4}

	fmt.Println("array1[0]: ", array1[0])
	fmt.Println("array2[0]: ", array2[0])
	fmt.Println("size of array3: ", len(array3))
}

func TestName4(t *testing.T) {
	
}