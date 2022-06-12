// fib_test.go
package expample

import "testing"

func BenchmarkFib(b *testing.B) {
	for n := 0; n < b.N; n++ {
		fib(30) // return fib(30) b.N  times
	}
}
