package main

import (
	"fmt"
)

var container = []string{"zero", "one", "two"}

func main() {
	container := map[int]string{0: "zero", 1: "one", 2: "two"}
	fmt.Printf("The element is %q.\n", container[1])
	value, ok := interface{}(container).([]string)
	if !ok {
		return
	}
	fmt.Printf("The container is :", value)
}
