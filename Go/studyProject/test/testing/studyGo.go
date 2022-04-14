package main

import (
	"fmt"
)

// notifier 是一个定义了
// 通知类行为的接口
type notifier interface {
	notify()
}

// user 在程序中定义一个用户类型
type user struct {
	name 	string
	email	string
}

// notify 是使用指针接收者实现的方法
func (u *user) notify() {
	fmt.Printf("Sending user email to %s<%s>\n",
		u.name,
		u.email)
}

// admin定义了程序的管理员
type admin struct {
	user	// 嵌入类型
	level	string
}

// notify 是使用指针接收者实现的方法
func (a *admin) notify() {
	fmt.Printf("Sending admin email to %s<%s>\n",
		a.name,
		a.email)
}

// main是应用程序的入口
func main() {
	// 创建一个user类型的值，并发送通知
	//bill := user{"Bill", "bill@email.com"}
	//
	//sendNotification(&bill)

	// ./listing36.go:32: 不能将u（类型是user）作为
	// 					  sendNotification的参数类型notifier
	//	user类型并没有实现notifier
	//						（notifier方法使用指针接收者声明）

	// 创建一个user类型的值，并发送通知
	ad := admin{
		user: user{
			name: 	"john smith",
			email: 	"john@yahoo.com",
		},
		level: "super",
	}

	//给admin用户发送一个通知
	//接口的嵌入的内部类型的实现并没有提升到
	//外部类型
	sendNotification(&ad)

	// 我们可以直接访问内部类型的方法
	ad.user.notify()

	// 内部类型的方法也可以被提升到外部类型
	ad.notify()
	//sendNotification(&lisa)
}

// sendNotification接受一个实现了notifier接口的值
// 并发送通知
func sendNotification(n notifier) {
	n.notify()
}