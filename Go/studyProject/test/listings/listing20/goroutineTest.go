package main

import (
	"fmt"
	"math/rand"
	"sync"
	"time"
)

// wg用来等待程序结束
var wg sync.WaitGroup

func init() {
	rand.Seed(time.Now().UnixNano())
}

// main是所有Go程序的入口
func main() {
	// 创建一个无缓冲的通道
	court := make(chan int)

	// 计数加2， 表示要等待两个goroutine
	wg.Add(2)

	// 启动两个选手
	go player("Nadal", court)
	go player("Djokovic", court)

	// 发球
	court <- 1

	// 等到游戏结束
	wg.Wait()
}

//player模拟一个选手在打网球
func player(name string, court chan int) {
	// 在函数退出时，用Done来通知main函数工作已经完成
	defer wg.Done()

	for {
		// 等待球被击打过来
		ball, ok := <-court
		if !ok {
			// 如果通道被关闭，我们就赢了
			fmt.Printf("Player %s Won\n", name)
			return
		}

		// 随机选数，然后用这个数来判断我们是否丢球
		n := rand.Intn(100)
		if n % 13 == 0 {
			fmt.Printf("Player %s Missed\n", name)

			// 关闭通道，表示我们输了
			close(court)
			return
		}

		// 显示击球数，并将击球数加1
		fmt.Printf("Player %s Hit %d\n", name, ball)
		ball++

		// 将球打向对手
		court <- ball
	}
}
