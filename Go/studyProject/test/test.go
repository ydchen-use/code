package main

import (
	"fmt"
	"github.com/goinaction/code/chapter3/words"
	"io/ioutil"
	"os"
	"time"
)

func testSlice() {
	testArray := [5]int{10, 20, 30, 40, 50}
	slice := []int{10, 20, 30, 40, 50}

	newSlice := slice[1:3]

	newSlice[0] = 35

	source := []string{"Apple", "Orange", "Plum", "Banana", "Grape"}

	newSlice1 := source[2:3:3]

	newSlice1 = append(newSlice1, "Kiwi", "Peak")

	fmt.Printf("test_array[0]: %d. \n", testArray[0])

	fmt.Println("test_array: \n", testArray)

	fmt.Println(slice)

	fmt.Println(newSlice1)
}

func sumNum(a int, b int) int {
	var sum int
	sum = a + b
	return sum
}

func testStruct() {
	type Books struct {
		Name 	string
		title 	string
		year  	string
		subject string
	}


}

func testOs() {
	filename := os.Args[0]

	contents, err := ioutil.ReadFile(filename)
	if err != nil {
		fmt.Println(err)
		return
	}

	text := string(contents)

	count := words.CountWords(text)
	fmt.Printf("There are %d words in your text. \n", count)
	fmt.Println("\n")
}

func say(s string) {
	for i := 0; i < 5; i++{
		time.Sleep(100 * time.Millisecond)
		fmt.Println(s)
	}
}

func sum(s []int, c chan int) {
	sum := 0
	for _, v := range s {
		sum += v
	}
	c <- sum // 把sum传到通道c
}

func main() {

	var sumNums int

	a := 25
	b := 35

	sumNums = sumNum(a, b)
	fmt.Println("a + b = ", sumNums)

	testSlice()

	// go goroutine 测试
	go say("world")
	say("hello")

	s := []int{7, 2, 8, -9, 4, 0}

	c := make(chan int)

	go sum(s[len(s)/2:], c)
	go sum(s[:len(s)/2], c)

	x, y := <-c, <-c

	fmt.Println(x, y, x + y)
}