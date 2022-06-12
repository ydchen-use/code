package main

import (
	"encoding/json"
	"fmt"
	"log"
	"os"
	"reflect"
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

//字符串中文存储
func TestName8(t *testing.T) {
	str1 := "Golang"
	str2 := "Go语言"
	fmt.Println(reflect.TypeOf(str2[2]).Kind())
	fmt.Println(str1[2], string(str1[2]))
	fmt.Printf("%d %c\n", str2[2], str2[2])
	fmt.Println("len(str2): ", len(str2)) // len(str2): 8 语言2字占6字节

	// 将str2转为 rune, rune可以正确处理中文
	runeArr := []rune(str2)
	fmt.Println(reflect.TypeOf(runeArr[2]).Kind())
	fmt.Println(runeArr[2], string(runeArr[2]))
	fmt.Println("len(runeArr): ", len(runeArr))
}

//指针的使用
func add(num int) {
	num += 1
}

func realAdd(num *int) {
	*num += 1
}

func TestName9(t *testing.T) {
	num := 100
	add(num)
	fmt.Println(num)

	realAdd(&num)
	fmt.Println(num)
}

// 错误捕获， defer 和 recover
func get(index int) (ret int) {
	defer func() {
		if r := recover(); r != nil {
			fmt.Println("Some error happened!", r)
			ret = -1
		}
	}()
	arr := [3]int{2, 3, 4}
	return arr[index]
}

func TestName10(t *testing.T) {
	fmt.Println(get(5))
	fmt.Println("finished!")
}

//结构体使用
type Student struct {
	name string
	age  int
}

func (stu *Student) hello(person string) string {
	return fmt.Sprintf("hello %s, I am %s", person, stu.name)
}

func TestName11(t *testing.T) {
	stu := &Student{
		name: "Tom",
	}
	msg := stu.hello("Jack")
	fmt.Println(msg) // hello Jack, I am Tom
}

// 接口interface使用
type Person interface {
	getName() string
}

func (stu *Student) getName() string {
	return stu.name
}

func TestName12(t *testing.T) {
	// 强制类型转换，实例化Student后， 转换为接口类型
	var p Person = &Student{
		name: "Tom",
		age:  18,
	}

	fmt.Println(p.getName()) // Tom

	// 空接口
	m := make(map[string]interface{})
	m["name"] = "Tom"
	m["age"] = 18
	m["score"] = [3]int{98, 99, 85}
	fmt.Println(m) // map[age:18 name:Tom score:[98 99 85]]
}

// 并发编程
// sync

var wg sync.WaitGroup

func download(url string) {
	fmt.Println("start to download", url)
	time.Sleep(time.Second) // 模拟耗时操作
	wg.Done()
}

func TestName13(t *testing.T) {
	for i := 0; i < 3; i++ {
		wg.Add(1)
		go download("a.com/")
	}
	wg.Wait()
	fmt.Println("Done!")
}

// 字符串的高效拼接
