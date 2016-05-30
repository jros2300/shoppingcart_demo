package main

import (
	"fmt"
	"time"
	"encoding/json"
	"math/rand"
	"math"
	"flag"
	"sync"
	"strconv"
	"strings"
	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/firehose"
	"github.com/agoussia/godes"
)

const productAdded = "productAdded"
const productRemoved = "productRemoved"
const cartBuy = "cartBuy"
const cartDiscard = "cartDiscard"
const login = "login"

const percentRemove = 30

const streamName = "ShoppingCart"

var uniformRand *godes.UniformDistr = godes.NewUniformDistr(false)
var normalRand *godes.NormalDistr = godes.NewNormalDistr(false)
var generator = rand.New(rand.NewSource(GetCurComputerTime()))

var curTime int64
func GetCurComputerTime() int64 {
	ct := time.Now().UnixNano()
	if ct > curTime {
		curTime = ct
		return ct
	} else if ct == curTime {
		curTime = ct + 1
		return curTime
	} else {
		curTime++
		return curTime
	}
}

type GenericEvent interface {}

type Event struct {
	EventType string `json:"type"`
	Timestamp int64 `json:"timestamp"`
	Customer int `json:"customer"`
	Cart int `json:"cart"`
	Product int `json:"product"`
	ProductList string `json:"productlist"`
}

func toJson(i interface{}) []byte {
	data, err := json.Marshal(i)
	if err != nil {
		panic(err)
	}

	return data
}

func isRemove() bool {
	if generator.Intn(100) < percentRemove {
		return true
	}
	return false
}

func isDiscard(cartProducts []int) bool {
	if len(cartProducts) == 0 {
		return true
	}
	nProductsBelow := 0
	for _, product := range cartProducts {
		if product < 9000 {
			nProductsBelow++
		}
	}
	if nProductsBelow > (len(cartProducts)/2) {
		return true
	}
	
	return false
}

func contains(s []int, e int) bool {
    for _, a := range s {
        if a == e {
            return true
        }
    }
    return false
}

func generateCartProcess() []GenericEvent {
	var events []GenericEvent
	var cartProducts []int
	var typeEvent string

	customer := generator.Intn(5000)
	cart := generator.Int()

	nItems := int(uniformRand.Get(3,25))

	currentTime := time.Now().Unix() + generator.Int63n(300)

	events = append(events, Event{login, currentTime, customer, cart, 0, ""})

	for ; nItems > 0; nItems-- {
		var typeEvent string
		var newProduct int

		currentTime += generator.Int63n(180)
		if len(cartProducts) > 0 && isRemove() {
			typeEvent = productRemoved
			pos := generator.Intn(len(cartProducts))
			newProduct = cartProducts[pos]
			cartProducts = append(cartProducts[:pos], cartProducts[pos+1:]...)
		} else {
			typeEvent = productAdded
			for {
				newProduct = int(math.Abs(normalRand.Get(10000, 2000)))
				if !contains(cartProducts, newProduct) {
					break
				}
			}
			cartProducts = append(cartProducts, newProduct)
		}
		
		newEvent := Event{typeEvent, currentTime, customer, cart, newProduct, ""}
		events = append(events, newEvent)
	}

	if isDiscard(cartProducts) {
		typeEvent = cartDiscard
	} else {
		typeEvent = cartBuy
	}

	var cartProductsText []string

	for i := range cartProducts {
		cartProductsText = append(cartProductsText, strconv.Itoa(cartProducts[i]))
	}

	events = append(events, Event{typeEvent, time.Now().Unix(), customer, cart, 0, strings.Join(cartProductsText, "-")})

	return events
}

var wg sync.WaitGroup

func uploadEvents(nevents int) {
	defer wg.Done()
	fh := firehose.New(session.New(&aws.Config{Region: aws.String("eu-west-1")}))
	
	for i:=0; i<nevents; i++ {
		carts := generateCartProcess()
		for _, event := range carts {
			params := &firehose.PutRecordInput{
				DeliveryStreamName: aws.String(streamName),
				Record: &firehose.Record{
					Data: []byte(string(toJson(event)) + "\n"),
				},
			}
			_, err := fh.PutRecord(params)
				if err != nil {
				fmt.Println("Error sending record: ", err)
			}
			//_, _ = fh, params
		}
	}
}

func main() {
	var threads int
	var nevents int
	flag.IntVar(&threads, "threads", 10, "Number of threads to run")
	flag.IntVar(&nevents, "events", 100, "Number of events per thread")
	flag.Parse()

	wg.Add(threads)
	for i:=0; i<threads; i++ {
		go uploadEvents(nevents)
	}

	wg.Wait()

	fmt.Println(threads * nevents)
	
	fmt.Println("Events generated")
}