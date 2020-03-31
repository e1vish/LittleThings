package main

import (
	"container/list"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"strings"

	"github.com/PuerkitoBio/goquery"
	"github.com/djimenez/iconv-go"
)

func NewWordsScrape(url string, charset string) *list.List {
	l := list.New()
	// Request the HTML page.
	res, err := http.Get(url)
	if err != nil {
		log.Fatal(err)
	}
	defer res.Body.Close()
	if res.StatusCode != 200 {
		log.Fatalf("status code error: %d %s", res.StatusCode, res.Status)
	}

	// Convert the designated charset HTML to utf-8 encoded HTML.
	// `charset` being one of the charsets known by the iconv package.
	utfBody, err := iconv.NewReader(res.Body, charset, "utf-8")
	if err != nil {
		// handler error
	}

	// Load the HTML document
	doc, err := goquery.NewDocumentFromReader(utfBody)
	if err != nil {
		log.Fatal(err)
	}

	// Find the review items
	doc.Find(".list-table .keyword .list-title").Each(func(i int, s *goquery.Selection) {
		// For each item found, get the band and title
		keyword := s.Text()
		l.PushBack(keyword)
	})
	return l
}

func ReadFromFile(fileName string) []byte {
	content, err := ioutil.ReadFile(fileName)
	if err != nil {
		log.Fatal(err)
	}
	return content
}

func WriteToFile(fileName string, words *list.List) {
	// If the file doesn't exist, create it, or append to the file
	f, err := os.OpenFile(fileName, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		log.Fatal(err)
	}
	for i := words.Front(); i != nil; i = i.Next() {
		if _, err := f.WriteString((i.Value).(string) + "\n"); err != nil {
			f.Close() // ignore error; Write error takes precedence
			log.Fatal(err)
		}
	}
	if err := f.Close(); err != nil {
		log.Fatal(err)
	}
}

func ListFilter(content string, words *list.List) *list.List {
	l := list.New()
	for i := words.Front(); i != nil; i = i.Next() {
		if strings.Contains(content, (i.Value).(string)) {

		} else {
			l.PushBack((i.Value).(string))
		}
	}
	return l
}

func main() {
	url := "http://top.baidu.com/buzz?b=396&c=12"
	charset := "GB2312"
	fileName := "new_words.dic"
	words := NewWordsScrape(url, charset)
	content := ReadFromFile(fileName)
	newWords := ListFilter(string(content), words)
	WriteToFile(fileName, newWords)
}
