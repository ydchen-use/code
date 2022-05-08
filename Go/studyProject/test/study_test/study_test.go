package main

import (
	"encoding/json"
	"fmt"
	"log"
	"os"
	"sync"
	"testing"
	"time"
)

func Add(a, b int) int {
	return a + b
}

func TestName(t *testing.T) {
	for i := 0; i < 10; i++ {
		Add(4, 5)
	}
}

func TestName1(t *testing.T) {
	for i := 0; i <= 10; i++ {
		fmt.Println(i)
		time.Sleep(1 * time.Second)
	}
}

// channel 简单测试
func TestName2(t *testing.T) {
	ch1 := make(chan int)
	go func() {
		for i := 0; i < 10; i++ {
			ch1 <- i
			time.Sleep(time.Second)
		}
		close(ch1)
	}()

	for range ch1 {
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
func TestName5(t *testing.T) {
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

	//type Website struct {
	//	Name 	string
	//	Url 	string
	//	Course	string
	//}

	// 定义map，解析json文件
	var SnmpMacInfo map[string]interface{}

	// 打开json文件
	jsonFile, err := os.Open(dataFile)

	// 处理错误
	if err != nil {
		fmt.Println(err)
	}

	// 关闭wenjian
	defer jsonFile.Close()

	// 第一种解码方式，创建json解码器
	decoder := json.NewDecoder(jsonFile)
	err = decoder.Decode(&SnmpMacInfo)

	if err != nil {
		fmt.Println("解码失败", err.Error())
	} else {
		fmt.Println("解码成功")
		fmt.Println(SnmpMacInfo)
	}

	// 第二种解码方式
	//byteValue, _ := ioutil.ReadAll(jsonFile)
	//
	//var result map[string]interface{}
	//json.Unmarshal([]byte(byteValue), &result)
	//
	//fmt.Println(string(byteValue))
	//fmt.Println(result)

}

// log 测试
func init() {
	log.SetPrefix("message")
	log.SetFlags(log.Ldate | log.Lmicroseconds | log.Llongfile)
}

func TestName7(t *testing.T) {
	// Println写到标准日志记录器
	log.Println("message")

	//Fatalln 在调用Println()之后会接着调用os.Exit()
	log.Fatalln("Fatal message")

	// Panicln 在调用Println()之后会接着调用panic()
	//log.Panicln("panic message")
}
