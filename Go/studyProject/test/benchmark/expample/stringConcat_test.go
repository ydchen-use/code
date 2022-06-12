package expample

import (
	"bytes"
	"fmt"
	"math/rand"
	"strings"
	"testing"
)

// 创建随机字符串函数
const letterBytes = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

func randomString(n int) string {
	b := make([]byte, n)
	for i := range b {
		b[i] = letterBytes[rand.Intn(len(letterBytes))]
	}
	return string(b)
}

// 拼接字符串的方式
// use +
func plusConcat(n int, str string) string {
	var s string
	for i := 0; i < n; i++ {
		s += str
	}
	return s
}

//使用 fmt.Sprintf
func sprintfConcat(n int, str string) string {
	var s string
	for i := 0; i < n; i++ {
		s = fmt.Sprintf("%s%s", s, str)
	}
	return s
}

// 使用 strings.Builder
func builderConcat(n int, str string) string {
	var bulider strings.Builder
	for i := 0; i < n; i++ {
		bulider.WriteString(str)
	}
	return bulider.String()
}

// 使用 []byte
func byteConcat(n int, str string) string {
	buf := make([]byte, 0)
	for i := 0; i < n; i++ {
		buf = append(buf, str...)
	}
	return string(buf)
}

// 使用 bytes.Buffer
func bufferConcat(n int, s string) string {
	buf := new(bytes.Buffer)
	for i := 0; i < n; i++ {
		buf.WriteString(s)
	}
	return buf.String()
}

// 如果长度已知， 那么创建 []byte时，可以指定切片的容量
func preByteConcat(n int, str string) string {
	buf := make([]byte, 0, n*len(str))
	for i := 0; i < n; i++ {
		buf = append(buf, str...)
	}
	return string(buf)
}

func benchmark(b *testing.B, f func(int, string) string) {
	var str = randomString(10)
	for i := 0; i < b.N; i++ {
		f(10000, str)
	}
}

func BenchmarkPlusConcat(b *testing.B) {
	benchmark(b, plusConcat)
}

func BenchmarkSprintfConcat(b *testing.B) {
	benchmark(b, sprintfConcat)
}

func BenchmarkBuilderConcat(b *testing.B) {
	benchmark(b, builderConcat)
}

func BenchmarkBufferConcat(b *testing.B) {
	benchmark(b, bufferConcat)
}

func BenchmarkByteConcat(b *testing.B) {
	benchmark(b, byteConcat)
}

func BenchmarkPreByteConcat(b *testing.B) {
	benchmark(b, preByteConcat)
}
