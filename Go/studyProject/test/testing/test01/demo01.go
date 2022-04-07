package main

import (
	"flag"
	"fmt"
)

var name1 = "Tina"

func main() {
	//name1 := flag.String("name", "everyone", "The greeting object.")
	//var name1 = getTheFlag()
	var name1 = "Bob"
	//flag.Parse()
	fmt.Printf("Hello, %s!\n", name1)
}

func getTheFlag() *string {
	return flag.String("name", "everyone", "The greeting object.")
}