package main

import (
	"fmt"
	"log"
	"os"

	_"github.com/goinaction/code/chapter2/sample/matchers"
	"github.com/goinaction/code/chapter2/sample/search"
)

// init 在 main之前调用
func init() {
	// 将日志输出到标准输出
	log.SetOutput (os.Stdout)
}

// main是整个函数的入口
func main()  {
	// 使用特定的项做搜索
	search.Run("president")
	fmt.Println("hello world")
}
