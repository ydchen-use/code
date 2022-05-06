package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"sync"
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

// channel 简单测试
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

// 类型声明
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

// 获取字典长度
func TestName4(t *testing.T) {
	ret := map[string]int{
		"a": 1,
		"b": 2,
		"c": 3,
	}
	fmt.Println(len(ret))
}

// sync.Map 测试
func TestName5(t *testing.T)  {
	var m sync.Map
	// 1. 写入
	m.Store("qcrao", 18)
	m.Store("stefno", 20)

	// 2. 读取
	age, _ := m.Load("qcrao")
	fmt.Println(age.(int))

	// 3. 遍历
	mapLen := 0
	m.Range(func(key, value interface{}) bool {
		name := key.(string)
		age := value.(int)
		fmt.Println(name, age)
		mapLen += 1
		fmt.Println(mapLen)
		return true
	})

	// 4. 删除
	m.Delete("qcrao")
	age, ok := m.Load("qcrao")
	fmt.Println(age, ok)

	// 5. 读取或写入
	m.LoadOrStore("stefno", 100)
	age, _ = m.Load("stefno")
	fmt.Println(age)
}

// 读取 json 文件
func TestName6(t *testing.T) {
	const dataFile = "files/snmp_mac_port.json"

	// 打开json文件
	jsonFile, err := os.Open(dataFile)

	// 处理错误
	if err != nil {
		fmt.Println(err)
	}

	// 关闭wenjian
	defer jsonFile.Close()

	byteValue, _ := ioutil.ReadAll(jsonFile)
	fmt.Println(string(byteValue))

}